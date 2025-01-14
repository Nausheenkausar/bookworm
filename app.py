from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

# Global variable to store the extracted text
pdf_text = ""

# Serve the index.html file
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to upload a PDF
@app.route('/upload', methods=['POST'])
def upload_pdf():
    global pdf_text
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_file = request.files['pdf']
    pdf_text = extract_text_from_pdf(pdf_file)

    if pdf_text:
        return jsonify({"message": "PDF uploaded and processed successfully!"})
    else:
        return jsonify({"error": "Failed to process PDF"}), 500

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

# Endpoint to search the PDF text
@app.route('/search', methods=['POST'])
def search_text():
    global pdf_text
    if not pdf_text:
        return jsonify({"error": "No PDF has been uploaded yet"}), 400

    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Find paragraphs with the query
    results = [para.strip() for para in pdf_text.split("\n\n") if query.lower() in para.lower()]

    if results:
        return jsonify({"results": results})
    else:
        return jsonify({"message": "No matching text found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
