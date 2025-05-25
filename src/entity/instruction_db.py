import sqlite3
from typing import List, Tuple
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../instruction.db")


class InstructionDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS instructions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    is_default INTEGER DEFAULT 0
                )
            """
            )
            conn.commit()

    def add_instruction(self, name: str, content: str, is_default: bool = False):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO instructions (name, content, is_default) VALUES (?, ?, ?)",
                (name, content, int(is_default)),
            )
            conn.commit()

    def get_instructions(self) -> List[Tuple[int, str, str, int]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, name, content, is_default FROM instructions ORDER BY is_default DESC, id ASC"
            )
            return c.fetchall()

    def get_instruction_by_id(self, id: int) -> Tuple[int, str, str, int]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, name, content, is_default FROM instructions WHERE id = ?",
                (id,),
            )
            return c.fetchone()

    def delete_instruction(self, id: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM instructions WHERE id = ?", (id,))
            conn.commit()

    def update_instruction(self, id: int, name: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE instructions SET name = ?, content = ? WHERE id = ?",
                (name, content, id),
            )
            conn.commit()

    def ensure_default(self, name: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM instructions WHERE is_default = 1")
            if c.fetchone()[0] == 0:
                self.add_instruction(name, content, is_default=True)


# 利用例:
# db = InstructionDB()
# db.ensure_default('デフォルト', 'デフォルトのインストラクション内容')
# db.add_instruction('サンプル', 'サンプル内容')
# print(db.get_instructions())
