import os
import sys
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import glob
from langchain.document_loaders import PyPDFLoader
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, ServiceContext, LLMPredictor

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig
from llama_index import download_loader

# Create a blueprint for the Flask app
chatpdf_bp = Blueprint('chatpdf', __name__)

# Route for the chatpdf page
@chatpdf_bp.route('/chatpdf')
def chatpdf():
    return render_template('chatpdf.html')

@chatpdf_bp.route('/chatpdf/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    file_type = file.content_type

    
        # Save the file to the training/uploads folder
    filename = secure_filename(file.filename)
    file_path = os.path.join("training/uploads", filename)
    file.save(file_path)

        # Remove all other files in the training/uploads folder
    for old_file in glob.glob("training/uploads/*.*"):
        if old_file != file_path:
            os.remove(old_file)

        # Retrain the model with the newly uploaded file
    train(filename)

    return "", 204
    
agent_chain = None

# Function to generate the FAISS index
def train(filename):
    global agent_chain
    if(filename.endswith(".pdf")):
        FileReader = download_loader("PDFReader")
        loader = FileReader()
        document = loader.load_data(file=Path(f"training/uploads/{filename}"))
    elif(filename.endswith(".docx")):
        FileReader = download_loader("DocxReader")
        loader = FileReader()
        document = loader.load_data(file=Path(f"training/uploads/{filename}"))
    elif(filename.endswith(".pptx")):
        FileReader = download_loader("PptxReader")
        loader = FileReader()
        document = loader.load_data(file=Path(f"training/uploads/{filename}"))
    else:
        document = SimpleDirectoryReader(input_files=[f"training/uploads/{filename}"]).load_data()
    
    service_context = ServiceContext.from_defaults(chunk_size_limit=512)
    index = GPTSimpleVectorIndex.from_documents(document, service_context=service_context)
    llm=ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")
    llm_predictor = LLMPredictor(llm)
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=512)

    index_configs = []
    tool_config = IndexToolConfig(index=index, name=f"Vector Index {filename}", description=f"useful for when you want to answer questions about {filename}", index_query_kwargs={"similarity_top_k": 3}, tool_kwargs={"return_direct": True})
    index_configs.append(tool_config)
    toolkit = LlamaToolkit(index_configs=index_configs)
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=512)
    agent_chain = create_llama_chat_agent(toolkit, llm, memory=memory, verbose=True)


@chatpdf_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get('question')

    try:
        conversation_result = agent_chain.run(input=question)
        return jsonify({
            "answer": conversation_result,
            "success": True
        })
    except:
        return jsonify({
            "answer": None,
            "success": False,
            "message": "Error"
        }), 400
