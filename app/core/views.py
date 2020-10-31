import os
from flask import render_template, send_file, request, redirect, url_for, session, jsonify, flash
from flask_login import current_user
from . import core

from .forms import FieldsForms, NekretnineForms
from ..models import Tax

from app import db
import io
import pdfrw
from pdfrw import PageMerge
from reportlab.pdfgen import canvas
import csv

from functools import wraps


def checkjmbg(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.jmbg:
            flash ('Molimo Vas unesite JMBG')
            return redirect(url_for("users.jmbg"))

        return f(*args, **kwargs)

    return decorated_function

@core.route('/')
def index():

    return render_template('index.html')

@core.route('/porez', methods=['POST', 'GET'])
@checkjmbg
def porez():

    return render_template('porez.html')

@core.route('/pregled_pr', methods=['POST', 'GET'])
def pregled_pr():
    """ Reading the pdf , to get all the forms , save them to a list of dictionaries and use it to generate dynamic
    flask_wtf fields because some of PDF's have more than 50 fields..."""

    # PDF handling , simply finding the right pdf that matches this route.
    file_pdf= os.path.abspath(os.path.dirname('app/static/img/pdf/prim_1054.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'prim_1054.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)


    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    forom = []
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            forom.append({'name' : field.T })


   # Due to lack of back-end representation in the actuall PDF rendering on "core.render" , of data will be stored in
   # manner to not match the PDF form fields so i can hardcode some of those strings on the PDF rendering.
    if forom[0]['name'] == '(2 JIBJMB)':
        forom[0]['name'] = "JMBG Korisnika -" + " " + str(current_user.jmbg)

    if forom[23]['name'] == '(1 Prezime i ime vlasnika imovine)':
        forom[23]['name'] = "{} {}".format(current_user.ime, current_user.prezime)
    

    # Formating data for select field
    csv_to_read = os.path.join(file_pdf, 'lista.csv')
    select = []
    with open(csv_to_read) as csv_doc:
        reader = csv.reader(csv_doc, delimiter=',')
        for row in reader:
            select.append((row[2], row[1]))
    


    # Using FormFieldList to generate exact amount of fields that this pdf holds , so user can submit data for pdf.
    form = FieldsForms(fields=forom)
    form.select.choices = select

    # Still trying to figure out how can i make all the fields validate , but for now i just submit it .
    if request.method == 'POST' and form.submit():
        data = form.data['fields']
        # Simple dict comperhension so that my KEYS in db.json_object match the KEYS on PDF FORMs , threfore
        my_dict = dict((k['name'], v['name'] if v else '') for k, v in zip(forom, data))
        my_dict['(koja se iznajmljuje)'] = form.select.data
        new = Tax(json_data=my_dict, tip='PRIM-1054', user_id=current_user.id)
        db.session.add(new)
        db.session.commit()

        return redirect (url_for('users.profile'))

    return render_template('porezi/prim-1054.html', form=form)


@core.route('/prijava_razrez_im', methods=['POST', 'GET'])
def prijava_razrez_im():
    """ Just like in view '/porez_po_odbitku' we are going to use premade pdf form , in order to automatise this process
    we will need to read the pdf file once again. Most forms are going to be generated , but still we will have to use
    some Jquery to complete the pdf filling logic because this form consist more than 150 forms , wich is obnoxious number
    to fill out , and is really slim chances one user is going to use all of the possible field submisions. Certain
    dropdown select field will help to organise logic behind the automation of this process."""


    # PDF handling , simply finding the right pdf that matches this route.
    file_pdf= os.path.abspath(os.path.dirname('app/static/img/pdf/pr_1.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'pr_1.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)


    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    # Beware this form contains absurd amount of forms , most of them wont be used for anything.
    forom = []

    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            forom.append({'name' : field.T })

    form = NekretnineForms(fields=forom)


    #Im using 'step_1' object in seasson wich is saved from ajax call in this view , check the pr_js. to see ajax call
    #It is pretty much straight forward just sending data as user clicks on next button.
    if form.validate_on_submit():
        if 'step_1' in session:
            session['step_1']['(godina)'] = form.kal_godina.data
            session['step_1']['(adresa)'] = form.adresa.data
            session['step_1']['(kanton)'] = form.kanton.data
            session['step_1']['(racun)'] = form.racun.data
            session['step_1']['(banka)'] = form.banka.data
            tax = Tax(json_data=session['step_1'], tip='PR-1', user_id=current_user.id)
            db.session.add(tax)
            db.session.commit()
            session.pop('step_1', None)
            return redirect(url_for('users.profile'))

    return render_template('porezi/pr-1.html', form=form)

@core.route('/step_1', methods=['POST'])
def step_1():
    """This is middle step in prijava_razrez_im because amount of fields depends on user needs. So this is a way to store
    data from ajax call that happens inside pr_1.js"""
    if request.method == "POST" and request.json:
        if 'step_1' in session:
            session['step_1'] = request.json
        else:
            session['step_1'] = request.json
    return 'sucess'


@core.route('/render_1054/<int:id>')
def render_1054(id):
    """Note that all rendering views have same "core" inside and that is the for loop we use over pdf.Annots . With this
    for loop we extract the form-field names so as locations of fields. Once we have all the names we can use our Tax
    database model and its json_data column that contains exact same keys as pdf-form. I am going to leave some commets
     after each important step , but PDFRW doc is the key to understand parts of this script. Despite all efforts
     a lot of things are still hard coded , because pdf is simply stupid format."""


    #Finding the right form of pdf
    file_pdf = os.path.abspath(os.path.dirname('app/static/img/pdf/prim_1054.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'prim_1054.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)

    #Query for selected data input
    all = Tax.query.filter_by(id=id).first()
    all = all.json_data


    #Creating two bytes object to store new canvs and final pdf in memory
    data = io.BytesIO()
    overlay_io = io.BytesIO()

    #Excluding the data we are going to automate
    presist = [all['(3 Porezna godina)'][2:], all['(6 Porezni period)'], all['(do)']]
    exclude = ['(3 Porezna godina)', '(6 Porezni period)', '(do)',]

    for i in exclude:
        if all[i]:
            all.pop(i)

    pdf = canvas.Canvas(data)
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:

            #The main loop of view , we are going to extract all the neccessary data from page.Annots
            #Label names and rect positions.
            label = field.T
            side = field.Rect
            left = min(side[0], side[2])
            bottom = min(side[1], side[3])
            value = all.get(label, '')

            pdf.drawString(x=float(left), y=float(bottom), text=value)
            pdf.drawString(x=216.96, y=609.12, charSpace=9, text=str(current_user.jmbg))
            pdf.drawString(x=479, y=610, text=presist[0], charSpace=9)
            pdf.drawString(x=459, y=583, text=presist[1], charSpace=9)
            pdf.drawString(x=507, y=583, text=presist[2], charSpace=9)
            pdf.drawString(x=72, y=608, text='{} {}'.format(current_user.ime, current_user.prezime))


        pdf.showPage()
        pdf.save()
        data.seek(0)

        #Creating overlay
        overlay = pdfrw.PdfReader(data)
        mark = overlay.pages[0]

        for page in range(len(template_pdf.pages)):
            merger = PageMerge(template_pdf.pages[page])
            merger.add(mark).render()

        pdfrw.PdfWriter().write(overlay_io, template_pdf)
        overlay_io.seek(0)

        # for page, data in zip(template_pdf.pages, overlay.pages):
        #     overlay = pdfrw.PageMerge().add(data)[0]
        #     pdfrw.PageMerge(page).add(overlay).render()
        #     pdfrw.PdfWriter().write(overlay_io, template_pdf)
        #
        #     overlay_io.seek(0)

    return send_file(overlay_io, as_attachment=True,
                         attachment_filename='a_file.pdf',
                         mimetype='application/pdf')



@core.route('/render_razrez/<int:id>')
def render_razrez(id):
    """Everything explained in first render function. The only difference here is that there is a lot of hardcoding
    to draw the data on canvas"""
    file_pdf = os.path.abspath(os.path.dirname('app/static/img/pdf/pr_1.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'pr_1.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)

    all = Tax.query.filter_by(id=id).first()
    all = all.json_data


    data = io.BytesIO()
    overlay_io = io.BytesIO()

    pdf = canvas.Canvas(data)
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            side = field.Rect
            left = min(side[0], side[2])
            bottom = min(side[1], side[3])
            value = all.get(label, '')
            #Matching the len of list in order to have more back end representation logic on this one.
            if len(value) == 5:
                pdf.drawString(x=float(left), y=float(bottom), text=value[0])
                pdf.drawString(x=float(left) + 140, y=float(bottom), text=value[1])
                pdf.drawString(x=float(left) + 190, y=float(bottom), text=value[2])
                pdf.drawString(x=float(left) + 240, y=float(bottom), text=value[3])
                pdf.drawString(x=float(left) + 340, y=float(bottom), text=value[3])
            #Everything had to be hardcoded here due to formation inside the database..
            pdf.drawString(x=128.5, y=725, text=str(current_user.jmbg), charSpace=5)
            pdf.drawString(x=260, y=702, text='{} {}'.format(current_user.ime, current_user.prezime))
            pdf.drawString(x=425, y=727, text=all['(godina)'])
            pdf.drawString(x=135, y=650, text=all['(kanton)'])
            pdf.drawString(x=170, y=675, text=all['(adresa)'])
            pdf.drawString(x=190, y=611, text=all['(racun)'])
            pdf.drawString(x=415, y=611, text=all['(banka)'])

        pdf.showPage()

        pdf.save()
        data.seek(0)

        overlay = pdfrw.PdfReader(data)
        mark = overlay.pages[0]

        for page in range(len(template_pdf.pages)):
            merger = PageMerge(template_pdf.pages[page])
            merger.add(mark).render()

        pdfrw.PdfWriter().write(overlay_io, template_pdf)
        overlay_io.seek(0)

        return send_file(overlay_io, as_attachment=True,
                         attachment_filename='a_file.pdf',
                         mimetype='application/pdf')

