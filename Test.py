import pdfkit

pdfkit.from_file('test.html', 'output1.pdf')
# # # or from a string:
# # html = '<html><body><h1>Hello</h1></body></html>'
# # pdfkit.from_string(html, 'out.pdf')


# from weasyprint import HTML

# # Convert HTML file to PDF
# HTML("test.html").write_pdf("output.pdf")
