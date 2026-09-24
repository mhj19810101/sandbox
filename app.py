from flask import Flask, request, send_file, send_from_directory
from docxtpl import DocxTemplate
from docx2pdf import convert

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "CRS.html")

@app.route("/generate-datasheet", methods=["POST"])
def generate_datasheet():
    data = request.json
    doc = DocxTemplate("datasheet_template.docx")

    context = {
        "V_rate": data.get("V_rate", "1200"),
        "I_rate": data.get("I_rate", "120")
}
    doc.render(context)
    doc.save("output.docx")
    convert("output.docx", "output.pdf")

    return send_file(
        "output.pdf",
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)