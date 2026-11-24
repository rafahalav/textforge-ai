
import sqlite3
from pathlib import Path
from datetime import datetime


# ==================================================
# CONFIGURAÇÃO
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATABASE_DIR / "textforge.db"


# ==================================================
# CLASSE DE BANCO DE DADOS
# ==================================================

class TextForgeDatabase:

    def __init__(self, database_path=DATABASE_PATH):

        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.initialize_database()


    def connect(self):

        connection = sqlite3.connect(
            self.database_path,
            timeout=10
        )

        connection.row_factory = sqlite3.Row

        return connection


    # ==============================================
    # INICIALIZAÇÃO
    # ==============================================

    def initialize_database(self):

        with self.connect() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS conversations (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    title TEXT NOT NULL,

                    model TEXT NOT NULL,

                    created_at TEXT NOT NULL,

                    updated_at TEXT NOT NULL

                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS messages (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    conversation_id INTEGER NOT NULL,

                    role TEXT NOT NULL,

                    content TEXT NOT NULL,

                    created_at TEXT NOT NULL,

                    FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE

                )
            """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS
                idx_messages_conversation

                ON messages(conversation_id)
            """)


    # ==============================================
    # CRIAR CONVERSA
    # ==============================================

    def create_conversation(self, title, model):

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        with self.connect() as connection:

            cursor = connection.execute("""
                INSERT INTO conversations (
                    title,
                    model,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                title,
                model,
                timestamp,
                timestamp
            ))

            return cursor.lastrowid


    # ==============================================
    # LISTAR CONVERSAS
    # ==============================================

    def list_conversations(self):

        with self.connect() as connection:

            rows = connection.execute("""
                SELECT *
                FROM conversations
                ORDER BY updated_at DESC
            """).fetchall()

            return [dict(row) for row in rows]


    # ==============================================
    # RECUPERAR CONVERSA
    # ==============================================

    def get_conversation(self, conversation_id):

        with self.connect() as connection:

            row = connection.execute("""
                SELECT *
                FROM conversations
                WHERE id = ?
            """, (conversation_id,)).fetchone()

            return dict(row) if row else None


    # ==============================================
    # ADICIONAR MENSAGEM
    # ==============================================

    def add_message(
        self,
        conversation_id,
        role,
        content
    ):

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        with self.connect() as connection:

            connection.execute("""
                INSERT INTO messages (
                    conversation_id,
                    role,
                    content,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                conversation_id,
                role,
                content,
                timestamp
            ))

            connection.execute("""
                UPDATE conversations
                SET updated_at = ?
                WHERE id = ?
            """, (
                timestamp,
                conversation_id
            ))


    # ==============================================
    # RECUPERAR MENSAGENS
    # ==============================================

    def get_messages(self, conversation_id):

        with self.connect() as connection:

            rows = connection.execute("""
                SELECT role, content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id ASC
            """, (conversation_id,)).fetchall()

            return [dict(row) for row in rows]


    # ==============================================
    # EXCLUIR CONVERSA
    # ==============================================

    def delete_conversation(self, conversation_id):

        with self.connect() as connection:

            connection.execute(
                "PRAGMA foreign_keys = ON"
            )

            connection.execute("""
                DELETE FROM conversations
                WHERE id = ?
            """, (conversation_id,))


    # ==============================================
    # RENOMEAR CONVERSA
    # ==============================================

    def rename_conversation(
        self,
        conversation_id,
        new_title
    ):

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        with self.connect() as connection:

            connection.execute("""
                UPDATE conversations
                SET title = ?, updated_at = ?
                WHERE id = ?
            """, (
                new_title,
                timestamp,
                conversation_id
            ))
