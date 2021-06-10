import os
from flask import render_template, send_file, request, redirect, url_for, session, jsonify, flash
from flask_login import current_user
from flask_login.utils import login_required
from . import core

from .forms import FieldsForms, NekretnineForms, DeleteTax
from ..models import Tax

from app import db

import io
import pdfrw
from pdfrw import PageMerge
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus.flowables import TopPadder


import csv

from functools import wraps

from typing import List


def checkjmbg(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.jmbg:
            flash('Molimo Vas unesite JMBG')
            return redirect(url_for("users.jmbg"))

        return f(*args, **kwargs)

    return decorated_function


@core.route('/')
def index():

    return render_template('index.html')


@core.route('/porezne-prijave', methods=['POST', 'GET'])
@checkjmbg
def porez():

    return render_template('porez.html')


@core.route('/prim_1054', methods=['POST', 'GET'])
@login_required
def prim_1054():
    """ 
    Reading the pdf , to get all the forms , save them to a list of dictionaries and use it to generate dynamic
    flask_wtf fields because some of PDF's have more than 50 fields...
    """

    # PDF handling , simply finding the right pdf that matches this route.
    file_pdf = os.path.abspath(os.path.dirname(
        'app/static/img/pdf/prim_1054.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'prim_1054.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)

    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    forom = []
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            forom.append({'name': field.T})

    # Formating data for select field
    csv_to_read = os.path.join(file_pdf, 'lista.csv')
    select = []
    with open(csv_to_read) as csv_doc:
        reader = csv.reader(csv_doc, delimiter=',')
        for row in reader:
            select.append((row[2], row[1]))

    # Using FormFieldList to generate exact amount of fields that this pdf holds , so user can submit data for pdf.
    form = FieldsForms(fields=enumerate([e for e in forom]))
    form.select.choices = select

    # Still trying to figure out how can i make all the fields validate , but for now i just submit it .
    if request.method == 'POST' and form.submit():
        data = form.data['fields']
        # Simple dict comperhension so that my KEYS in db.json_object match the KEYS on PDF FORMs , threfore
        my_dict = dict((k['name'], v['name'] if v else '')
                       for k, v in zip(forom, data))
        my_dict['(koja se iznajmljuje)'] = '{} - {}'.format(form.select.data,
                                                            form.address.data)
        new = Tax(json_data=my_dict, tip='PRIM-1054', user_id=current_user.id)
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('users.profile'))

    return render_template('porezi/prim-1054.html', form=form, current_user=current_user)


@core.route('/edit-1054/<int:form_id>', methods=['POST', 'GET'])
@login_required
def edit_1054(form_id):
    """ 
    So far this route exposed all weaknesses in my code , trying to overatomate the filling of pdf
    didnt scale really well with editing the same data , the key problem is that forms inside the
    PDF are not placed in same order like the data in my database. I am creating a list where i store
    all the differences between the first list 'forom' that contains PDF forms , and the same fields
    from my database model Tax . I compare them with keys and check if there is any value inside
    if so i send it back to the form so that once submited data is shown to user.
    """
    tax_form = db.session.query(Tax).filter(Tax.id == form_id).first()
    if current_user.id != tax_form.author.id:
        return "ERROR 403"

    file_pdf = os.path.abspath(os.path.dirname(
        'app/static/img/pdf/prim_1054.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'prim_1054.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)

    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    forom = []
    to_fill = []
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            # list that is used to store data in db
            forom.append({'name': field.T})
            # a list that i use to display data
            to_fill.append({'name': field.T})

    # Getting the values from my database so i can display it back to user
    for val in forom:
        for k, v in tax_form.json_data.items():
            if val['name'] == k:
                to_fill[to_fill.index(val)] = {'name': tax_form.json_data[k]}

    # I have to find a way to fetch this CSV from client side !
    csv_to_read = os.path.join(file_pdf, 'lista.csv')
    select = []
    with open(csv_to_read) as csv_doc:
        reader = csv.reader(csv_doc, delimiter=',')
        for row in reader:
            select.append((row[2], row[1]))

    form = FieldsForms(fields=to_fill)
    form.select.choices = select

    if request.method == 'POST' and form.submit():
        data = form.data['fields']
        # Simple dict comperhension so that my KEYS in db.json_object match the KEYS on PDF FORMs , threfore
        my_dict = dict((k['name'], v['name'] if v else '')
                       for k, v in zip(forom, data))
        my_dict['(koja se iznajmljuje)'] = '{} - {}'.format(form.select.data,
                                                            form.address.data)
        tax_form.json_data = my_dict
        db.session.commit()
        flash('Uspjesno ste izvršilu izmjenu vase PRIM-1054 prijave !')

        return redirect(url_for('users.profile'))

    return render_template('porezi/edit-1054.html', form=form, tax_form=tax_form)


@core.route('/pr_1)', methods=['POST', 'GET'])
def pr_1():
    """ 
    Just like in view '/porez_po_odbitku' we are going to use premade pdf form , in order to automatise this process
    we will need to read the pdf file once again. Most forms are going to be generated , but still we will have to use
    some Jquery to complete the pdf filling logic because this form consist more than 150 forms , wich is obnoxious number
    to fill out , and is really slim chances one user is going to use all of the possible field submisions. Certain
    dropdown select field will help to organise logic behind the automation of this process.
    """

    # PDF handling , simply finding the right pdf that matches this route.
    file_pdf = os.path.abspath(os.path.dirname('app/static/img/pdf/pr_1.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'pr_1.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)

    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    # Beware this form contains absurd amount of forms , most of them wont be used for anything.
    forom = []

    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            forom.append({'name': field.T})

    form = NekretnineForms(fields=forom)



    # Im using 'step_1' object in seasson wich is saved from ajax call in this view , check the pr_js. to see ajax call
    # It is pretty much straight forward just sending data as user clicks on next button.
    if form.validate_on_submit():
        if 'step_1' in session:
            session['step_1']['(godina)'] = form.kal_godina.data
            session['step_1']['(adresa)'] = form.adresa.data
            session['step_1']['(kanton)'] = form.kanton.data
            session['step_1']['(racun)'] = form.racun.data
            session['step_1']['(banka)'] = form.banka.data
            tax = Tax(json_data=session['step_1'],
                      tip='PR-1', user_id=current_user.id)
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
@login_required
def render_1054(id):
    """
    Note that all rendering views have same "core" inside and that is the for loop we use over pdf.Annots . With this
    for loop we extract the form-field names so as locations of fields. Once we have all the names we can use our Tax
    database model and its json_data column that contains exact same keys as pdf-form. I am going to leave some commets
     after each important step , but PDFRW doc is the key to understand parts of this script. Despite all efforts
     a lot of things are still hard coded , because pdf is simply stupid format.
     """
    all = Tax.query.filter_by(id=id).first()
    if current_user.id != all.author.id:
        return "ERROR 403"

    # Finding the right form of pdf
    file_pdf = os.path.abspath(os.path.dirname(
        'app/static/img/pdf/prim_1054.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'prim_1054.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)

    # Query for selected data input
    all = all.json_data

    # Creating two bytes object to store new canvs and final pdf in memory
    data = io.BytesIO()
    overlay_io = io.BytesIO()

    # Excluding the data we are going to automate
    presist = [all['(3 Porezna godina)'][2:],
               all['(6 Porezni period)'], all['(do)']]
    exclude = ['(3 Porezna godina)', '(6 Porezni period)', '(do)', ]

    for i in exclude:
        if all[i]:
            all.pop(i)

    pdf = canvas.Canvas(data)
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:

            # The main loop of view , we are going to extract all the neccessary data from page.Annots
            # Label names and rect positions.
            label = field.T
            side = field.Rect
            left = min(side[0], side[2])
            bottom = min(side[1], side[3])
            value = all.get(label, '')

            pdf.drawString(x=float(left), y=float(bottom), text=value)
            pdf.drawString(x=216.96, y=609.12, charSpace=9,
                           text=str(current_user.jmbg))
            pdf.drawString(x=479, y=610, text=presist[0], charSpace=9)
            pdf.drawString(x=459, y=583, text=presist[1], charSpace=9)
            pdf.drawString(x=507, y=583, text=presist[2], charSpace=9)
            pdf.drawString(x=72, y=608, text='{} {}'.format(
                current_user.ime, current_user.prezime))

        pdf.showPage()
        pdf.save()
        data.seek(0)

        # Creating overlay
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
                     attachment_filename='prim1054.pdf',
                     mimetype='application/pdf')

@core.route('/render_pr1/<int:id>', methods=['POST', 'GET'])
def render_pr1(id):

    file_pdf = os.path.abspath(os.path.dirname('app/static/img/pdf/pr_1.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'pr_1.pdf')

    q = db.session.query(Tax).filter(Tax.id==id).first()

    buffer = io.BytesIO()
    overlay_io = io.BytesIO()
    template_pdf = pdfrw.PdfReader(pdf_to_read)
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    styles = getSampleStyleSheet()


    data = [
        [''
        ,'Vrsta imovine \n        (a)','Lokacija imovine \n            (b)',
        'Jedinica mjere      \n            (c)', 
        'Broj jedinica mjere \n               (d)',
         '     Porez po \n jedinici mjere \n            (f)',
         'Iznos Poreza \n         (g)'
         ],
        ]

    right = [
        'kuca', 'Kuca, zgrada\n ili stan',
        'poslovni', 'Poslovni prostor',
        'garaza', 'Garaza koja se \n izdaje',
        'parking', 'Parking prostor',
        'vozilo', 'Putnicko vozilo',
        'tvozilo', 'Teretno vozilo',
        'plovni', 'Plovni objekat',
        'letljelica', 'Letljelica',
        'stol', 'Stol u kazinu',
        'automat', 'Automat za \n zabavne igre',
        
        ]

    index_v = 1
    final_sum = 0
    for k, v in q.json_data.items():
        if isinstance(q.json_data[k], List):
            if k[-2].isdigit():
                k = ''.join([i for i in k if not i.isdigit()])
            key_pair = right.index(k) + 1
            if k in right:
                v.pop(0)
                v.insert(0,  index_v)
                v.insert(1, right[key_pair])
                data.append(v)
                final_sum += int(v[-1])
                index_v += 1
    data.append(['', 'UKUPNO', '', '', '', '', final_sum])

    def calc_h(num_lines, extended):
        start = (2, 520)
        e_start = 520 - (extended * 11.5) 
        result = num_lines - start[0]
        position = e_start - (result*18)
        return position

    table = Table(data,colWidths=(0.7*cm, 2.5*cm, None, None, None, None, None))
    table.setStyle(TableStyle([
        ('ALIGN',(1,1), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0,0), (6,0), 10),
        ('FONTSIZE', (1,1), (6, 20), 8),
        ('FONTNAME', (0, 0), (6,0),'Times-Bold'),
        ('BOX', (0,0), (-1,-1), 0.75, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
        ]))

    table.wrapOn(pdf_canvas, width, height)
    table.drawOn(pdf_canvas, 40, calc_h(len(data), len([len(e[1]) for e in data if len(e[1]) >= 22])))
    pdf_canvas.drawString(x=128.5, y=725, text=str(
        current_user.jmbg), charSpace=4.5)
    pdf_canvas.drawString(x=260, y=702, text='{} {}'.format(
        current_user.ime, current_user.prezime))
    pdf_canvas.drawString(x=425, y=727, text=q.json_data['(godina)'])
    pdf_canvas.drawString(x=135, y=650, text=q.json_data['(kanton)'])
    pdf_canvas.drawString(x=170, y=675, text=q.json_data['(adresa)'])
    pdf_canvas.drawString(x=190, y=611, text=q.json_data['(racun)'])
    pdf_canvas.drawString(x=415, y=611, text=q.json_data['(banka)'])

    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)


    overlay = pdfrw.PdfReader(buffer)
    mark = overlay.pages[0]

    for page in range(len(template_pdf.pages)):
        merger = PageMerge(template_pdf.pages[page])
        merger.add(mark).render()

    pdfrw.PdfWriter().write(overlay_io, template_pdf)
    overlay_io.seek(0)

    return send_file(overlay_io, as_attachment=True,
                     attachment_filename='pr-1.pdf',
                     mimetype='application/pdf')

@core.route('/editpr-1/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_pr1(id):

    doc = db.session.query(Tax).filter(Tax.id==id).first()
    data = doc.json_data

    form = NekretnineForms()

    if form.validate_on_submit():
        if 'step_1' in session:
            print(session['step_1'])
            session['step_1']['(godina)'] = form.kal_godina.data
            session['step_1']['(adresa)'] = form.adresa.data
            session['step_1']['(kanton)'] = form.kanton.data
            session['step_1']['(racun)'] = form.racun.data
            session['step_1']['(banka)'] = form.banka.data
            doc.json_data=session['step_1']
            db.session.commit()
            session.pop('step_1', None)
            return redirect(url_for('users.profile'))

    return render_template('/porezi/editpr-1.html', form=form, data=data)


@core.route('/delete/<int:form_id>', methods=['POST', 'GET'])
@login_required
def delete_tax(form_id):

    tax_form = db.session.query(Tax).filter(Tax.id == form_id).first()
    if current_user.id != tax_form.author.id:
        return "ERROR 403"

    form = DeleteTax()

    if form.validate_on_submit():
        db.session.delete(tax_form)
        db.session.commit()
        flash('Uspjesno ste izbrisali poresku prijavu !')

        return redirect(url_for('users.profile'))

    return render_template('delete.html', form=form)


@core.route('/fetchcity', methods=['POST', 'GET'])
def fetchcity():

    file_csv = os.path.abspath(os.path.dirname(
        'app/static/img/pdf/lista.csv'))

    csv_to_read = os.path.join(file_csv, 'lista.csv')
    select = []
    with open(csv_to_read) as csv_doc:
        reader = csv.reader(csv_doc, delimiter=',')
        for row in reader:
            select.append((row[2], row[1], row[3]))

    
    return jsonify(select)






