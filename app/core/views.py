import os
from flask import render_template, send_file, request, redirect, url_for
from flask_login import current_user
from . import core

from .forms import FieldsForms, NekretnineForms
from ..models import Tax

from app import db
import io
import pdfrw
from pdfrw import PageMerge
from reportlab.pdfgen import canvas




@core.route('/')
def index():


    return render_template('index.html')



@core.route('/pregled_pr', methods=['POST', 'GET'])
def pregled_pr():
    """ Reading the pdf , to get all the forms , save them to a list of dictionaries and use it to generate dynamic
    flask_wtf fields because some of PDF's have more than 50 fields..."""


    # PDF handling , simply finding the right pdf that matches this route.
    file_pdf= os.path.abspath(os.path.dirname('app/static/img/pdf/prvi.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'prvi.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)


    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    forom = []
    for page in template_pdf.Root.Pages.Kids:
        print(page)
        for field in page.Annots:
            label = field.T
            forom.append({'name' : field.T })


   # Due to lack of back-end representation in the actuall PDF rendering on "core.render" , of data will be stored in
   # manner to not match the PDF form fields so i can hardcode some of those strings on the PDF rendering.
    if forom[0]['name'] == '(2 JIBJMB)':
        forom[0]['name'] = "JMBG Korisnika -" + " " + str(current_user.jmbg)

    if forom[23]['name'] == '(1 Prezime i ime vlasnika imovine)':
        forom[23]['name'] = "{} {}".format(current_user.ime, current_user.prezime)


    # Using FormFieldList to generate exact amount of fields that this pdf holds , so user can submit data for pdf.
    form = FieldsForms(fields=forom)

    # Still trying to figure out how can i make all the fields validate , but for now i just submit it .
    if request.method == 'POST' and form.submit():
        data = form.data['fields']

        # Simple dict comperhension so that my KEYS in db.json_object match the KEYS on PDF FORMs , threfore
        my_dict = dict((k['name'], v['name'] if v else '') for k, v in zip(forom, data))
        new = Tax(json_data=my_dict)
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
    file_pdf= os.path.abspath(os.path.dirname('app/static/img/pdf/drugi.pdf'))
    pdf_to_read = os.path.join(file_pdf, 'drugi.pdf')
    template_pdf = pdfrw.PdfReader(pdf_to_read)


    # Generating the list of dict that will be used for dynamic flask_wtf forms.
    # Beware this form contains absurd amount of forms , most of them wont be used for anything.
    forom = []

    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            forom.append({'name' : field.T })


    if request.method == "POST":
        all = request.form
        print(all)
    form = NekretnineForms(fields=forom)
    if request.method == 'POST' and form.validate_on_submit():
        print(request.form['string1'])

        return redirect (url_for('core.prijava_razrez_im'))


    return render_template('porezi/pr-1.html', form=form)



@core.route('/render/<int:id>')
def render(id):
    file_pdf = '/home/dariok/Desktop/flask_apps/porez_app/app/static/img/pdf/prvi.pdf'

    all = Tax.query.filter_by(id=id).first()

    all = all.json_data


    template_pdf = pdfrw.PdfReader(file_pdf)

    user = current_user

    data = io.BytesIO()
    overlay_io = io.BytesIO()

    karina = '0611991181961'

    presist = [all['(3 Porezna godina)'], all['(6 Porezni period)'], all['(do)']]
    exclude = ['(3 Porezna godina)', '(6 Porezni period)', '(do)',]

    for i in exclude:
        if all[i]:
            all.pop(i)


    print(presist)

    pdf = canvas.Canvas(data)
    for page in template_pdf.Root.Pages.Kids:
        for field in page.Annots:
            label = field.T
            side = field.Rect
            left = min(side[0], side[2])
            bottom = min(side[1], side[3])
            value = all.get(label, '')
            pdf.drawString(x=float(left), y=float(bottom), text=value)
            pdf.drawString(x=216.96, y=609.12, charSpace=9, text=karina)
            pdf.drawString(x=479, y=610, text=presist[0], charSpace=9)
            pdf.drawString(x=459, y=583, text=presist[1], charSpace=9)
            pdf.drawString(x=507, y=583, text=presist[2], charSpace=9)
            pdf.drawString(x=72, y=608, text='{} {}'.format(current_user.ime, current_user.prezime))

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

        # for page, data in zip(template_pdf.pages, overlay.pages):
        #     overlay = pdfrw.PageMerge().add(data)[0]
        #     pdfrw.PageMerge(page).add(overlay).render()
        #     pdfrw.PdfWriter().write(overlay_io, template_pdf)
        #
        #     overlay_io.seek(0)

    return send_file(overlay_io, as_attachment=True,
                         attachment_filename='a_file.pdf',
                         mimetype='application/pdf')


@core.route('/porez', methods=['POST', 'GET'])
def porez():

    return render_template('porez.html')














