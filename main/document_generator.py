import pdfkit
import base64
import uuid

def generate_pdf(query, text):
    with open("logo.jpg", "rb") as image_file:

        encoded_string = base64.b64encode(image_file.read()).decode()

    img_src = f"data:image/jpg;base64,{encoded_string}"

    paragraphs = ['<p>{}</p>'.format(p) for p in text.split('\n') if p.strip() != '']

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                margin: 0px;
                padding: 20px;
            }
            .header {
                display: flex;
                justify-content: space-between;
            }
            .logo {
                float: left;
            }
            .info {
                text-align: right;
            }
            .line {
                height: 2px;
                background-color: black;
                width: calc(100%);
                margin-top:40px;
            }
            .content {
                padding-top: 20px;
            }
            .content p {
                text-indent: 30px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <img class="logo" src="{img_src}" alt="Logo" style="height: 140px;">
            <div class="info">
                <h2>Law GPT</h2>
                <h3>Version 3.0</h3>
            </div>
        </div>
        <hr class="line">
        <div class="content">
            <h1>{heading}</h1>
            {paragraphs}
        </div>
    </body>
    </html>
    """

    html = html.replace("{img_src}", img_src).replace("{paragraphs}", '\n'.join(paragraphs)).replace("{heading}", query)

    document_path = f"workspace/{str(uuid.uuid4())}.pdf"
    
    pdfkit.from_string(html, document_path)

    return document_path
