from flask import Flask, request, jsonify
import PyPDF2
import openai

app = Flask(__name__)

# OpenAI API key setup (Replace with your key)
openai.api_key = "your-openai-api-key"

# Route to upload and process the PDF
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_file = request.files['pdf']
    text_content = extract_text_from_pdf(pdf_file)
    
    # Save text content in memory or database for querying
    with open("processed_text.txt", "w", encoding="utf-8") as f:
        f.write(text_content)
    
    return jsonify({"message": "PDF uploaded and processed successfully!"})

# Extract text from the uploaded PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Route to handle user queries
@app.route('/query', methods=['POST'])
def query_pdf():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Load the processed text
    with open("processed_text.txt", "r", encoding="utf-8") as f:
        text_content = f.read()

    # Use OpenAI or another NLP model to find relevant answers
    response = query_openai(text_content, question)
    return jsonify({"answer": response})

# Use OpenAI's GPT for semantic search
def query_openai(text_content, question):
    prompt = f"Here is the content of a book:\n\n{text_content}\n\nAnswer the following question based on the book:\n{question}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
