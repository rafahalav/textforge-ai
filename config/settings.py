
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações principais
APP_NAME = "TextForge AI"
APP_VERSION = "1.0.0"

# Provedor de IA
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Modelo generativo
MODEL_NAME = "openai/gpt-oss-120b"

# Parâmetros padrão de geração
DEFAULT_MAX_TOKENS = 2048

# Identidade do assistente
SYSTEM_PROMPT = """
Você é o TextForge AI, um assistente de inteligência artificial
especializado em geração de conteúdo.

Suas responsabilidades:
- Produzir textos originais.
- Explicar conceitos técnicos.
- Criar conteúdos educacionais.
- Auxiliar na programação.
- Responder em português brasileiro, salvo quando solicitado
  outro idioma.

Seja claro, organizado e tecnicamente preciso.
"""
