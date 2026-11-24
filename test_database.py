
from core.database import TextForgeDatabase


db = TextForgeDatabase()

print("\nTEXTFORGE AI - TESTE SQLITE")
print("=" * 40)

# Criar conversa
conversation_id = db.create_conversation(
    title="Teste do banco de dados",
    model="openai/gpt-oss-120b"
)

print(f"\nConversa criada: {conversation_id}")

# Salvar mensagens
db.add_message(
    conversation_id,
    "user",
    "Olá, TextForge AI!"
)

db.add_message(
    conversation_id,
    "assistant",
    "Olá! Banco de dados funcionando."
)

# Recuperar mensagens
messages = db.get_messages(conversation_id)

print("\nMensagens recuperadas:")

for message in messages:
    print(f"{message['role']}: {message['content']}")

# Listar conversas
conversations = db.list_conversations()

print(f"\nTotal de conversas: {len(conversations)}")

print("\nTeste concluído!")
