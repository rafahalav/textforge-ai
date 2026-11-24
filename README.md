# TextForge AI

<p align="center">
  <img src="assets/textforge-banner.png" alt="TextForge AI Banner" width="100%">
</p>

**An AI-powered text generation application built with Python, Streamlit, and the Groq API.**

TextForge AI is a Python-based application designed to generate, manage, and export AI-powered text content through an interactive web interface.

Powered by **OpenAI GPT-OSS 120B**, running through the **Groq inference API**, the application combines real-time response streaming, persistent conversation management, and content export in a modular and lightweight architecture.

This project demonstrates the practical integration of generative AI APIs, Python development, database persistence, and web application development.

---

## ✨ Features

- 🤖 **AI Text Generation:** Generate content using the GPT-OSS 120B language model.
- ⚡ **Real-Time Streaming:** Display responses progressively as they are generated.
- 💾 **Persistent Conversation History:** Store conversations and messages locally using SQLite.
- 🗂️ **Conversation Management:** Create, retrieve, rename, and delete individual conversations.
- 📄 **Content Export:** Export generated content in Markdown (`.md`) and plain text (`.txt`) formats.
- 🎛️ **Generation Parameters:** Customize temperature and maximum completion tokens.
- 🖥️ **Interactive Web Interface:** User-friendly interface developed with Streamlit.
- 🔐 **Environment-Based Configuration:** Secure API key management using environment variables.
- 🚀 **Quick Startup:** Launch the application on Linux and macOS using the included `run.sh` script.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web interface |
| Groq API | Remote AI inference |
| GPT-OSS 120B | Large language model |
| SQLite | Local conversation storage |
| SQL | Database operations |
| python-dotenv | Environment variable management |
| Bash | Application startup automation |

## 🏗️ Architecture

The application follows a modular structure, separating the user interface, AI generation logic, configuration, and database operations.

- **Presentation Layer:** Streamlit interface and user interaction.
- **Generation Layer:** API communication, prompt handling, and response streaming.
- **Configuration Layer:** Model settings, environment variables, and system instructions.
- **Persistence Layer:** SQLite database for conversations and messages.

This architecture promotes separation of responsibilities, maintainability, and future extensibility.

## 📁 Project Structure

```text
textforge-ai/
│
├── app.py
├── run.sh
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
│
├── assets/
│   ├── textforge-banner.png
│   └── sidebar-banner.png
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── core/
│   ├── __init__.py
│   ├── generator.py
│   └── database.py
│
├── data/                       # Created locally
│   └── textforge.db
│
├── .streamlit/
│   └── config.toml
│
├── test_api.py
├── test_database.py
└── test_stream.py
```

**Directory responsibilities:**

- `app.py` — Main Streamlit application and user interface.
- `run.sh` — Linux/macOS startup script.
- `config/` — Application settings and environment configuration.
- `core/` — AI generation engine and SQLite database operations.
- `assets/` — Project visual resources.
- `data/` — Local database storage, generated when the application runs.
- `.streamlit/` — Streamlit application configuration.

The database and its data directory are generated locally and excluded from version control.

## ⚙️ Requirements

- Python 3.10 or newer.
- pip.
- Internet connection.
- Groq API key.

The language model runs remotely through the Groq API, so local GPU hardware is not required.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/rafahalav/textforge-ai.git
cd textforge-ai
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the environment

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the API key

Create a `.env` file in the project root directory, using `.env.example` as a reference.

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your own API key.

**Important:** Never commit your `.env` file or expose your API key in source code.

### 6. Run the application

**Linux / macOS — Recommended**

Make the startup script executable:

```bash
chmod +x run.sh
```

Start the application:

```bash
./run.sh
```

The script checks the virtual environment, verifies the required dependencies, and starts the Streamlit application. If the virtual environment does not exist, it attempts to create it automatically.

**Alternative — Manual startup**

```bash
streamlit run app.py
```

**Windows**

Use the activated virtual environment and run:

```powershell
streamlit run app.py
```

Streamlit will start the application and open it in your default browser.

## 🎛️ Configuration

The application allows users to adjust generation parameters through the interface:

- **Temperature:** Controls the variability and creativity of generated responses.
- **Maximum Tokens:** Sets the maximum completion length.

The model and application settings are maintained in the configuration module.

## 💾 Data Persistence

TextForge AI uses SQLite to store conversation history locally.

The database supports:

- Conversation creation.
- Message storage.
- Conversation retrieval.
- Conversation renaming.
- Individual conversation deletion.

Deleting a conversation also removes its associated messages, while preserving other conversations.

The database is stored locally in the `data/` directory. This directory is excluded from version control to protect local conversation data.

## 🔐 Security

API credentials are managed through environment variables using `python-dotenv`.

The project excludes sensitive and local files from version control, including:

- `.env` files.
- Virtual environments.
- Python cache files.
- Local SQLite databases.
- Local development configuration files.

Users must provide their own Groq API key to run the application.

Conversation history is stored locally in the user's SQLite database and is not included in the repository.

## 🧪 Verification Scripts

The project includes standalone scripts for manually checking core functionality:

| Script | Purpose |
|---|---|
| `test_database.py` | Checks SQLite conversation and message operations |
| `test_api.py` | Checks AI text generation through the Groq API |
| `test_stream.py` | Checks real-time response streaming |

The API and streaming scripts require a valid Groq API key and an active internet connection.

## 📌 Project Status

**Version 1.0.0 — Initial Development Release**

TextForge AI is an evolving personal software project. Its current implementation focuses on reliable AI text generation, conversation persistence, and a practical user experience.

Future development may include additional AI-powered tools and improvements to conversation management.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🧑‍💻 Author

**Rafael Halav**

- GitHub: [@rafahalav](https://github.com/rafahalav)

---

*Built with Python, curiosity, and a passion for technology.*
# textforge-ai
