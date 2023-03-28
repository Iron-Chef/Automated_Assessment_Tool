import pdfkit

@app.route('/export_to_pdf')
def export_to_pdf():
    # get the table of results from your database or form submission
    results = get_results()

    rendered_template = render_template('your_results.html', results=results)

    # create the pdf page view
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    # convert the HTML template to PDF using pdfkit
    pdf = pdfkit.from_string(rendered_template, False, options=options)

    # send the PDF file as a response to the user
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=results.pdf'
    return response
