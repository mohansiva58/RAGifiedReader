# RAGified Reader 📄

A Streamlit-powered AI application for chatting with PDF documents using Google's Gemini AI and RAG (Retrieval-Augmented Generation).

## Features

- 📤 Upload PDF files and chat with their content
- 🤖 Powered by Google Gemini 2.0 Flash
- 🔍 Uses ChromaDB for vector storage and semantic search
- 💬 Conversational interface with chat history
- 🎨 Clean, modern UI with sidebar navigation

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mohansiva58/RAGifiedReader.git
cd RAGifiedReader
```

### 2. Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

Create a secrets file from the example:

```bash
# Copy the example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your API keys:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
OPENAI_API_KEY = "your_actual_openai_api_key_here"  # Only needed for food.py
```

**⚠️ Important:** Never commit the `.streamlit/secrets.toml` file! It's already in `.gitignore`.

### 5. Run the Application

```bash
streamlit run rag_web_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Deploying to Streamlit Community Cloud (Free)

### Step 1: Push to GitHub

Ensure your code is pushed to GitHub (secrets are automatically excluded via `.gitignore`):

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Log in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository:** `mohansiva58/RAGifiedReader`
   - **Branch:** `main` (or `deploy/update-for-streamlit`)
   - **Main file:** `rag_web_app.py`
5. Click **"Deploy"**

### Step 3: Add Secrets in Streamlit Cloud

1. In your deployed app's settings, go to **"Secrets"**
2. Add your API keys in TOML format:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

3. Click **"Save"**
4. The app will automatically restart with the secrets

## Project Structure

```
RAGifiedReader/
├── rag_web_app.py              # Main RAG PDF chat application
├── food.py                      # AI Food Scanner app (bonus)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules (excludes secrets)
├── .streamlit/
│   └── secrets.toml.example     # Example secrets file (template)
└── README.md                    # This file
```

## How It Works

1. **Upload PDF**: Upload any PDF document through the web interface
2. **Text Extraction**: PyPDF extracts text from the PDF
3. **Chunking**: Text is split into manageable chunks (500 chars with 100 overlap)
4. **Embedding**: Google's embedding model creates vector representations
5. **Storage**: ChromaDB stores the embeddings for fast retrieval
6. **Query**: Ask questions in natural language
7. **Retrieval**: Relevant chunks are retrieved using semantic search
8. **Generation**: Gemini generates contextual answers based on retrieved content

## Tech Stack

- **Framework**: Streamlit
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: Google Generative AI Embeddings
- **Vector DB**: ChromaDB
- **PDF Processing**: PyPDF
- **Orchestration**: LangChain

## Security Notes

- ✅ API keys are loaded from Streamlit secrets or environment variables
- ✅ No hardcoded credentials in the codebase
- ✅ `.streamlit/secrets.toml` is gitignored
- ⚠️ **Never commit API keys to version control**
- 🔒 If you accidentally expose a key, revoke it immediately and generate a new one

## Troubleshooting

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Key Not Found
- Verify `.streamlit/secrets.toml` exists and contains `GEMINI_API_KEY`
- For environment variables: `export GEMINI_API_KEY="your_key"` (Linux/Mac) or `$env:GEMINI_API_KEY="your_key"` (PowerShell)

### Streamlit Not Running
Run with the correct command:
```bash
streamlit run rag_web_app.py
```
(Don't use `python rag_web_app.py`)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/mohansiva58/RAGifiedReader/issues).

---

Made with ❤️ using Streamlit and Google Gemini AI
