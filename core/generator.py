
from groq import Groq, APIError, RateLimitError, AuthenticationError

from config.settings import (
    GROQ_API_KEY,
    MODEL_NAME,
    DEFAULT_MAX_TOKENS,
    SYSTEM_PROMPT
)


class TextForgeError(Exception):
    """Erro personalizado do motor generativo."""
    pass


class TextGenerator:
    """
    Motor de geração de texto do TextForge AI.

    Responsável por:
    - Comunicação com a API Groq.
    - Geração de conteúdo.
    - Controle de parâmetros.
    - Streaming de respostas.
    - Gerenciamento do contexto.
    """

    def __init__(self, model=None):

        if not GROQ_API_KEY:
            raise TextForgeError(
                "Chave GROQ_API_KEY não encontrada."
            )

        self.client = Groq(api_key=GROQ_API_KEY)

        self.model = model or MODEL_NAME

        self.system_prompt = SYSTEM_PROMPT

    def _build_messages(self, prompt, history=None):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        if history:
            messages.extend(history)

        messages.append({
            "role": "user",
            "content": prompt
        })

        return messages

    def generate(
        self,
        prompt,
        history=None,
        temperature=0.7,
        max_tokens=DEFAULT_MAX_TOKENS
    ):
        """
        Gera uma resposta completa.
        """

        if not prompt or not prompt.strip():
            raise ValueError("O prompt não pode estar vazio.")

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(prompt, history),
                temperature=temperature,
                max_completion_tokens=max_tokens,
                stream=False
            )

            return response.choices[0].message.content or ""

        except AuthenticationError as error:
            raise TextForgeError(
                "Falha de autenticação. Verifique sua API Key."
            ) from error

        except RateLimitError as error:
            raise TextForgeError(
                "Limite de utilização da API atingido."
            ) from error

        except APIError as error:
            raise TextForgeError(
                f"Erro na API Groq: {error}"
            ) from error

    def stream(
        self,
        prompt,
        history=None,
        temperature=0.7,
        max_tokens=DEFAULT_MAX_TOKENS
    ):
        """
        Gera uma resposta progressivamente.
        """

        if not prompt or not prompt.strip():
            raise ValueError("O prompt não pode estar vazio.")

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(prompt, history),
                temperature=temperature,
                max_completion_tokens=max_tokens,
                stream=True
            )

            for chunk in response:

                if not chunk.choices:
                    continue

                content = chunk.choices[0].delta.content

                if content:
                    yield content

        except AuthenticationError as error:
            raise TextForgeError(
                "Falha de autenticação. Verifique sua API Key."
            ) from error

        except RateLimitError as error:
            raise TextForgeError(
                "Limite de utilização da API atingido."
            ) from error

        except APIError as error:
            raise TextForgeError(
                f"Erro na API Groq: {error}"
            ) from error
