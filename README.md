# 💡 GreenLight AI: The ESG Compliance Auditor

**GreenLight AI** is a sophisticated, end-to-end AI application designed to automate the initial stages of Environmental, Social, and Governance (ESG) compliance auditing. Built as a capstone project, it showcases the integration of modern AI technologies to solve a complex and high-value business problem.

The application allows a user to upload a corporate sustainability report. An autonomous AI agent then analyzes the report against official ESG standards (like the GRI Standards) and generates a high-level compliance summary, identifying which requirements are addressed and providing a general summary of the company's ESG posture.

This project stands at the intersection of a **Commerce** background and advanced **AI Engineering**, demonstrating the ability to apply cutting-edge technology to the world of corporate governance and finance.

-----

## 🚀 Features

  * **Interactive Web Interface:** A clean and user-friendly UI built with Streamlit.
  * **PDF Report Analysis:** Users can upload multi-page corporate sustainability reports in PDF format.
  * **Automated Audit & Summary:** The AI agent performs a compliance check against specific standards and generates a concise, general summary of the report's content.
  * **RAG-Powered Knowledge Base:** Utilizes a Retrieval-Augmented Generation (RAG) pipeline with a local vector store (FAISS) to create a searchable knowledge base of the GRI Standards.
  * **Autonomous AI Agent:** An intelligent agent built with LangGraph orchestrates the entire audit workflow.
  * **Local & Private:** Performs all analysis using a locally-hosted LLM (via Ollama) and local embeddings, ensuring data privacy and cost-free operation.
  * **Robust Error Handling:** The agent is designed to handle unexpected model outputs gracefully, ensuring the application remains stable.

-----

## 🧑‍💻 Skills Demonstrated
- **Python** – Modular project structure  
- **NLP & ML** – Embedding + FAISS retrieval + classification  
- **Deep Learning** – Transformer embeddings + local LLM  
- **RAG (Retrieval-Augmented Generation)** – Core workflow  
- **LLMs / Generative AI** – JSON compliance judgments + reasoning  
- **Prompt Engineering** – Structured outputs validated with Pydantic  
- **AI Agents** – LangGraph state machine for ESG audit flow  
- **Deployment/UI** – Streamlit app with PDF upload  

-----

## 🛠️ Architecture & Tech Stack

The application is built on a modular architecture, with each component handling a specific task. The LangGraph agent core directs the workflow between the RAG-based retriever and the LLM-based classifier to produce the final analysis.

### **Tech Stack**

  * **Backend:** Python
  * **AI Frameworks:** LangChain, LangGraph
  * **LLM Serving:** Ollama (`qwen2:0.5b` model)
  * **Embeddings:** HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
  * **Vector Store:** FAISS (Facebook AI Similarity Search)
  * **Web UI:** Streamlit
  * **PDF Processing:** Pypdf

-----

## ⚙️ Setup and Installation

Follow these steps to run the application on your local machine.

### **Prerequisites**

  * Python 3.9+
  * [Ollama](https://ollama.com/) installed and running.

### **1. Clone the Repository**

```bash
git clone https://github.com/arjunvaibhavAI/GreenLight-AI.git
cd GreenLight-AI
```

### **2. Set Up a Virtual Environment**

```bash
# For Windows
python -m venv .venv
.\.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Set Up Ollama**

Open a separate terminal and pull the required model:

```bash
ollama pull qwen2:0.5b
```

*Leave this terminal running in the background to keep the Ollama server active.*

### **5. Prepare the Knowledge Base**

  * Download the **Consolidated Set of GRI Standards** PDF from the [GRI website](https://www.google.com/search?q=https://www.globalreporting.org/how-to-use-the-gri-standards/gri-standards-english-language-downloads/).
  * Place the downloaded PDF inside the `data/knowledge_base/` directory.
  * Rename the file to `GRI_Standards.pdf`.

### **6. Build the Vector Store**

Run the ingestion script to process the PDF and create the local vector database.

```bash
python src/processing.py
```

This will create a `faiss_index` folder inside the `vector_store` directory.

### **7. Launch the Application**

You are now ready to run the Streamlit app\!

```bash
streamlit run app.py
```

The application will open in your web browser.

-----

## 📈 Future Improvements

This project serves as a strong foundation. Future enhancements could include:

  * **Smarter Document Chunking:** Instead of feeding the whole report to the classifier, the agent could first search the report for the 2-3 most relevant paragraphs related to the topic.
  * **Dynamic Topic Extraction:** Use an LLM in the first step to read the report's table of contents and automatically generate the list of topics to audit.
  * **Model Scaling:** The architecture is model-agnostic. It could be upgraded to use a more powerful model (like a 7B parameter local model or a cloud API like GPT-4) for higher accuracy.
  * **Detailed Reporting:** Generate a downloadable PDF report of the audit findings.

-----

## 👤 Contact

Created by [Arjunvaibhav] - feel free to connect\!

  * **LinkedIn:** `[https://www.linkedin.com/in/arjunvaibhav-ai/]`
  * **GitHub:** `[https://github.com/arjunvaibhavAI]`