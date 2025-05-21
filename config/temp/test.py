# from playwright.sync_api import sync_playwright

# def convert_html_to_pdf(html_path: str, output_pdf_path: str,landScapeMode:bool):
#     abs_html_path = html_path  # Your local server HTML
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()

#         # Set viewport large enough to accommodate wide table
#         page.set_viewport_size({"width": 1920, "height": 1080})

#         # Load page
#         page.goto(abs_html_path, wait_until='networkidle')


#         # Generate landscape PDF
#         page.pdf(
#             path=output_pdf_path,
#             format="A4",
#             landscape=landScapeMode,
#             print_background=True,
#             margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"},
#             scale=0.75  # Optional: shrink content to fit page
#         )

#         browser.close()

# # Call the function
# convert_html_to_pdf('http://127.0.0.1:5501/config/temp/htmlContent.html', "report_landscape1.pdf",True)
# convert_html_to_pdf('http://127.0.0.1:5501/config/temp/htmlContent2.html', "report_landscape2.pdf",False)


# from playwright.sync_api import sync_playwright
# from weasyprint import HTML

# def extract_inlined_html(url: str) -> str:
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)

#         page = browser.new_page()
#         page.goto(url, wait_until='networkidle')

#         print("Satrt")

#         # Inline all computed styles
#         page.add_script_tag(content="""
#             function inlineAllStyles() {
#                 const elements = document.querySelectorAll('*');
#                 for (const el of elements) {
#                     const computed = getComputedStyle(el);
#                     let style = '';
#                     for (const prop of computed) {
#                         style += `${prop}:${computed.getPropertyValue(prop)};`;
#                     }
#                     el.setAttribute('style', style);
#                 }
#             }
#             inlineAllStyles();
#         """)


#         # Give time for script to apply
#         page.wait_for_timeout(500)

#         print("wait jere")

#         # Extract final HTML with inline styles
#         content = page.content()
#         print("Dne")
#         browser.close()
#         return content

# def convert_to_pdf_with_weasy(html_string: str, output_pdf: str):
#     HTML(string=html_string).write_pdf(output_pdf)

# # Example usage
# url = 'http://127.0.0.1:5501/config/temp/htmlContent.html'
# rendered_html = extract_inlined_html(url)
# convert_to_pdf_with_weasy(rendered_html, 'final_report.pdf')


import pdfkit

options = {
    "javascript-delay": 3000,  # wait 3 seconds for JS charts to render
    "enable-local-file-access": None,  # Needed if reading local HTML file with local scripts
}

pdfkit.from_file("config/temp/htmlContent2.html", "report.pdf", options=options)
