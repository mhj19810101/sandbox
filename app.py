from flask import Flask, request, send_file, send_from_directory
from docxtpl import DocxTemplate

import os
import json

app = Flask(__name__)
RECORD_FOLDER = "record"

@app.route("/")
def index():
    return send_from_directory(".", "CRS.html")

@app.route("/certificates/<path:filename>")
def certificates(filename):
    return send_from_directory("certificates", filename)

@app.route("/generate-datasheet", methods=["POST"])
def generate_datasheet():
    data = request.json
    product_name = data.get("Product_Name", "NSSF080CM1K2ESAF")

# Save JSON record
    json_filename = os.path.join(RECORD_FOLDER,f"{product_name}.json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Save docx record
    doc = DocxTemplate("datasheet_template.docx")
    context = data
    doc.render(context)
    docx_filename = os.path.join(RECORD_FOLDER,f"{product_name}.docx")
    doc.save(docx_filename)

    return send_file(docx_filename,as_attachment=True,download_name=f"{product_name}.docx")

if __name__ == "__main__":
    app.run(debug=True)
