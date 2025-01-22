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
    #new line of code
from flask import Flask, render_template, request
import os
import re
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

app = Flask(__name__)

# Ensure the upload and static image folders exist
UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'static/images'

for folder in [UPLOAD_FOLDER, IMAGE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to extract text from the PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text() + " "
    return text
def search_for_keyword_in_pdf(query, file_path, context_window=2):
    import re
    text = extract_text_from_pdf(file_path)
    query = query.lower()
    results = []
    
    # Split the PDF text into paragraphs
    paragraphs = re.split(r'\n\s*\n', text)  # Split by blank lines

    for paragraph in paragraphs:
        # Check if any word from the query exists in the paragraph
        if any(word in paragraph.lower() for word in query.split()):
            # Extract the lines around the keyword for better context
            lines = paragraph.split('\n')
            matched_lines = []
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in query.split()):
                    # Add surrounding lines for context
                    start = max(0, i - context_window)
                    end = min(len(lines), i + context_window + 1)
                    matched_lines.extend(lines[start:end])
            
            # Join lines and format result
            formatted_result = "\n".join(matched_lines).strip()
            formatted_result = formatted_result.replace("", "←").replace("", "•")
            if formatted_result not in results:  # Avoid duplicates
                results.append(f"<pre>{formatted_result}</pre>")

    return results if results else ["No relevant answers found."]


# Enhanced function to search for keywords in the PDF text
def search_for_keyword_in_pdf(keyword, file_path, context_window=2):
    text = extract_text_from_pdf(file_path)
    keyword = keyword.lower()
    results = []
    
    # Split into paragraphs or sections
    paragraphs = re.split(r'\n\s*\n', text)  # Split by blank lines
    
    for paragraph in paragraphs:
        if keyword in paragraph.lower():
            # Extract the lines around the keyword for better context
            lines = paragraph.split('\n')
            matched_lines = []
            for i, line in enumerate(lines):
                if keyword in line.lower():
                    # Add surrounding lines for context
                    start = max(0, i - context_window)
                    end = min(len(lines), i + context_window + 1)
                    matched_lines.extend(lines[start:end])
            
            # Join lines and format result
            formatted_result = "\n".join(matched_lines).strip()
            formatted_result = formatted_result.replace("", "←").replace("", "•")
            if formatted_result not in results:  # Avoid duplicates
                results.append(f"<pre>{formatted_result}</pre>")

    return results if results else ["No relevant answers found."]

# Function to extract images from the PDF
def extract_images_from_pdf(file_path, output_folder=IMAGE_FOLDER):
    doc = fitz.open(file_path)
    extracted_images = []

    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"{output_folder}/page{i+1}_img{img_index+1}.{image_ext}"
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            extracted_images.append(image_path)
    
    return extracted_images

# Route to render the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle search
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    pdf_file = request.files['pdf']
    
    # Save the uploaded PDF file
    pdf_path = os.path.join(UPLOAD_FOLDER, "uploaded_pdf.pdf")
    pdf_file.save(pdf_path)
    
    # Search for keywords and extract images
    search_results = search_for_keyword_in_pdf(query, pdf_path)
    extracted_images = extract_images_from_pdf(pdf_path)
    
    # Render results on the page
    return render_template('index.html', results=search_results, images=extracted_images)

if __name__ == '__main__':
    app.run(debug=True)

--------------------------------------------------------------update-----------------------------------------------------------------------------------------------
from flask import Flask, render_template, request
import os
import re
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

app = Flask(__name__)

# Ensure the upload and static image folders exist
UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'static/images'

for folder in [UPLOAD_FOLDER, IMAGE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to extract text from the PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text() + " "
    return text

# Improved function to search for a query in the PDF
def search_for_keyword_in_pdf(query, file_path, context_window=1):
    """
    Searches for a query in a PDF and extracts relevant sentences with context.
    :param query: The keyword or question to search for.
    :param file_path: Path to the PDF file.
    :param context_window: Number of sentences before and after the match to include.
    :return: List of search results with context.
    """
    text = extract_text_from_pdf(file_path)
    query = query.lower()
    results = []

    # Split text into sentences for granular search
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for i, sentence in enumerate(sentences):
        if query in sentence.lower():  # Match the query in the sentence
            # Add context: sentences before and after the match
            start = max(0, i - context_window)
            end = min(len(sentences), i + context_window + 1)
            matched_context = " ".join(sentences[start:end])
            matched_context = matched_context.strip().replace("", "←").replace("", "•")

            if matched_context not in results:  # Avoid duplicates
                results.append(f"<pre>{matched_context}</pre>")

    # Return the matched results or a default message if none found
    return results if results else ["No relevant answers found."]

# Function to extract images from the PDF
def extract_images_from_pdf(file_path, output_folder=IMAGE_FOLDER):
    doc = fitz.open(file_path)
    extracted_images = []

    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"{output_folder}/page{i+1}_img{img_index+1}.{image_ext}"
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            extracted_images.append(image_path)
    
    return extracted_images
from flask import Flask, request, jsonify
@app.route('/save_note', methods=['POST'])
def save_note():
    data = request.json
    note_text = data.get('note', '')
    with open('notes.txt', 'a') as file:
        file.write(note_text + '\n')
    return jsonify({"message": "Note saved successfully!"})



# Route to render the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle search
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    pdf_file = request.files['pdf']
    
    # Save the uploaded PDF file
    pdf_path = os.path.join(UPLOAD_FOLDER, "uploaded_pdf.pdf")
    pdf_file.save(pdf_path)
    
    # Search for keywords and extract images
    search_results = search_for_keyword_in_pdf(query, pdf_path)
    extracted_images = extract_images_from_pdf(pdf_path)
    
    # Limit search results to the first 5 for display purposes
    limited_results = search_results[:5]

    # Render results on the page
    return render_template('index.html', results=limited_results, images=extracted_images)

if __name__ == '__main__':
    app.run(debug=True)
