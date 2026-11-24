import streamlit as st

from datetime import datetime

from core.generator import TextGenerator, TextForgeError
from core.database import TextForgeDatabase
from config.settings import APP_NAME, APP_VERSION


# ==================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CONFIGURAÇÃO DO MODELO
# ==================================================

MODEL_OPTIONS = {
    "GPT-OSS 120B": "openai/gpt-oss-120b"
}


# ==================================================
# IDENTIDADE VISUAL
# ==================================================

st.markdown("""
<style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #42A5F5;
    }

    .subtitle {
        color: #9AAABD;
        font-size: 0.95rem;
    }

    .stChatMessage {
        border-radius: 12px;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #26364A;
    }

</style>
""", unsafe_allow_html=True)


# ==================================================
# BANCO DE DADOS
# ==================================================

database = TextForgeDatabase()


# ==================================================
# ESTADO DA CONVERSAÇÃO
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = None

if "history_selector" not in st.session_state:
    st.session_state.history_selector = None


# ==================================================
# FUNÇÕES DE EXPORTAÇÃO
# ==================================================

def export_markdown(messages, model):

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    content = [
        "# TextForge AI - Histórico de Conversa",
        "",
        f"**Modelo:** {model}",
        f"**Data da exportação:** {timestamp}",
        "",
        "---",
        ""
    ]

    for message in messages:

        if message["role"] == "user":
            title = "Usuário"
        else:
            title = "TextForge AI"

        content.append(f"### {title}")
        content.append("")
        content.append(message["content"])
        content.append("")
        content.append("---")
        content.append("")

    return "\n".join(content)


def export_txt(messages, model):

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    content = [
        "TEXTFORGE AI - HISTÓRICO DE CONVERSA",
        "=" * 45,
        f"Modelo: {model}",
        f"Data da exportação: {timestamp}",
        "=" * 45,
        ""
    ]

    for message in messages:

        if message["role"] == "user":
            title = "USUÁRIO"
        else:
            title = "TEXTFORGE AI"

        content.append(title)
        content.append("-" * 45)
        content.append(message["content"])
        content.append("")

    return "\n".join(content)


# ==================================================
# FUNÇÕES DO HISTÓRICO
# ==================================================

def create_conversation_title(prompt):

    title = " ".join(prompt.strip().split())

    if len(title) > 45:
        title = title[:45].rsplit(" ", 1)[0] + "..."

    return title or "Nova conversa"


def load_selected_conversation():

    conversation_id = st.session_state.history_selector

    if conversation_id is None:
        return

    conversation = database.get_conversation(conversation_id)

    if conversation:

        saved_messages = database.get_messages(conversation_id)

        st.session_state.active_conversation_id = conversation_id

        st.session_state.messages = [
            {
                "role": message["role"],
                "content": message["content"]
            }
            for message in saved_messages
            if message["role"] in ("user", "assistant")
        ]


def start_new_conversation():

    st.session_state.messages = []

    st.session_state.active_conversation_id = None

    st.session_state.history_selector = None


def delete_active_conversation():

    conversation_id = st.session_state.active_conversation_id

    if conversation_id is not None:

        database.delete_conversation(conversation_id)

        st.session_state.messages = []

        st.session_state.active_conversation_id = None

        st.session_state.history_selector = None


# ==================================================
# BARRA LATERAL
# ==================================================

with st.sidebar:

    # BANNER DA BARRA LATERAL
    st.image(
        "assets/sidebar-banner.png",
        use_container_width=True
    )


    st.caption(f"Versão {APP_VERSION}")

    st.divider()

    # MODELO

    st.markdown("### Modelo generativo")

    selected_model = st.selectbox(
        "Selecione o modelo",
        options=list(MODEL_OPTIONS.keys())
    )

    model_id = MODEL_OPTIONS[selected_model]

    st.caption(f"ID: `{model_id}`")

    st.divider()

    # PARÂMETROS DE GERAÇÃO

    st.markdown("### Parâmetros de geração")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controla a diversidade das respostas."
    )

    max_tokens = st.slider(
        "Máximo de tokens",
        min_value=256,
        max_value=8192,
        value=2048,
        step=256,
        help="Define o limite máximo de tokens da resposta."
    )

    st.divider()

    # CONVERSAÇÃO

    st.markdown("### Conversação")

    if st.button(
        "➕ Nova conversa",
        use_container_width=True
    ):

        start_new_conversation()
        st.rerun()

    if st.button(
        "🗑️ Excluir conversa",
        use_container_width=True,
        disabled=st.session_state.active_conversation_id is None
    ):

        delete_active_conversation()
        st.rerun()

    # RECUPERA AS CONVERSAS DO SQLITE

    conversations = database.list_conversations()

    conversation_ids = [
        conversation["id"]
        for conversation in conversations
    ]

    # SINCRONIZA O SELETOR COM A CONVERSA ATIVA

    active_id = st.session_state.active_conversation_id

    if active_id in conversation_ids:

        if st.session_state.history_selector != active_id:
            st.session_state.history_selector = active_id

    elif st.session_state.history_selector not in [None] + conversation_ids:

        st.session_state.history_selector = None

    # ORGANIZA OS TÍTULOS DAS CONVERSAS

    conversation_titles = {
        conversation["id"]: conversation["title"]
        for conversation in conversations
    }

    # EXIBE O HISTÓRICO

    st.markdown("#### Histórico de conversas")

    if conversations:

        st.selectbox(
            "Selecione uma conversa",
            options=[None] + conversation_ids,
            format_func=lambda conversation_id: (
                "Selecione uma conversa..."
                if conversation_id is None
                else conversation_titles.get(
                    conversation_id,
                    "Conversa sem título"
                )
            ),
            key="history_selector",
            on_change=load_selected_conversation,
            label_visibility="collapsed"
        )

        st.caption(
            f"{len(conversations)} conversa(s) armazenada(s)"
        )

    else:

        st.caption(
            "Nenhuma conversa salva ainda."
        )

    st.divider()

    # EXPORTAÇÃO

    st.markdown("### Exportar conversa")

    if st.session_state.messages:

        markdown_data = export_markdown(
            st.session_state.messages,
            selected_model
        )

        txt_data = export_txt(
            st.session_state.messages,
            selected_model
        )

        st.download_button(
            label="📄 Baixar Markdown",
            data=markdown_data,
            file_name="textforge_conversa.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.download_button(
            label="📝 Baixar TXT",
            data=txt_data,
            file_name="textforge_conversa.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:

        st.caption(
            "Inicie uma conversa para habilitar a exportação."
        )

    st.divider()

    # INFORMAÇÕES

    st.caption(
        "Inferência realizada pela infraestrutura da Groq."
    )

    st.caption(
        "Desenvolvido com Python + Streamlit"
    )


# ==================================================
# CABEÇALHO PRINCIPAL
# ==================================================

st.markdown(
    '<div class="main-title">TextForge AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Seu laboratório pessoal de inteligência artificial generativa.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==================================================
# TELA INICIAL
# ==================================================

if not st.session_state.messages:

    st.markdown("### Como posso ajudar?")

    st.markdown("""
    Experimente algumas possibilidades:

    - Criar textos e artigos.
    - Explicar conceitos técnicos.
    - Desenvolver ideias e projetos.
    - Gerar exemplos de programação.
    - Resumir e reescrever conteúdos.
    """)

    st.info(
        "Digite uma instrução no campo abaixo para começar."
    )


# ==================================================
# EXIBIÇÃO DO HISTÓRICO
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==================================================
# ENTRADA DE PROMPTS
# ==================================================

prompt = st.chat_input(
    "Digite sua instrução para o TextForge AI..."
)


# ==================================================
# PROCESSAMENTO DA MENSAGEM
# ==================================================

if prompt:

    # CRIA UMA CONVERSA NO BANCO, SE NECESSÁRIO

    if st.session_state.active_conversation_id is None:

        conversation_id = database.create_conversation(
            title=create_conversation_title(prompt),
            model=model_id
        )

        st.session_state.active_conversation_id = conversation_id

    else:

        conversation_id = st.session_state.active_conversation_id

    # REGISTRA A MENSAGEM DO USUÁRIO

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    database.add_message(
        conversation_id,
        "user",
        prompt
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # RECUPERA O HISTÓRICO ANTERIOR

    history = st.session_state.messages[:-1]

    try:

        # INICIALIZA O MOTOR GENERATIVO

        generator = TextGenerator(
            model=model_id
        )

        with st.chat_message("assistant"):

            st.caption(
                f"Modelo: {selected_model}"
            )

            # GERAÇÃO PROGRESSIVA

            response = st.write_stream(
                generator.stream(
                    prompt=prompt,
                    history=history,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )

        # ARMAZENA A RESPOSTA NO HISTÓRICO E NO SQLITE

        if response:

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            database.add_message(
                conversation_id,
                "assistant",
                response
            )

    except TextForgeError as error:

        st.error(
            f"Erro no motor generativo: {error}"
        )

    except Exception as error:

        st.error(
            f"Erro inesperado: {error}"
        )

    # ATUALIZA A BARRA LATERAL E O HISTÓRICO

    st.rerun()
