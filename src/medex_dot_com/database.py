import sqlite3
from medex_dot_com.utils import create_dir, db_directory
from domain.database import Database

class MedexDatabase(Database):

    def __init__(self):
        create_dir(db_directory)

        self.connection = sqlite3.connect(f"{db_directory}/medex.db")
        self.cursor = self.connection.cursor()

        self.table_name = "medex"
        self.init_db()

    def init_db(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}(
                id INTEGER primary key AUTOINCREMENT,
                url TEXT,
                name TEXT,
                type TEXT,
                generic_group TEXT,
                price TEXT,
                strip_price TEXT,
                pack_size_info TEXT,
                indications TEXT,
                pharmacology TEXT,
                dosage TEXT,
                interaction TEXT,
                contraindications TEXT,
                side_effects TEXT,
                precautions TEXT,
                pediatric_uses TEXT,
                pregnancy_cat TEXT,
                drug_classes TEXT,
                storage_conditions TEXT
            )
        """)

        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS status(
                id INTEGER primary key AUTOINCREMENT,
                url TEXT,
                status TEXT,
                msg TEXT
            )
            """)

    def insert_record(self, rec: dict):
        keys = ','.join(rec.keys())
        question_marks = ','.join(list('?'*len(rec)))
        values = tuple(rec.values())
        self.cursor.execute('INSERT INTO '+self.table_name+' ('+keys+') VALUES ('+question_marks+')', values)

    def save_status(self, url: str, status: str, msg: str|None):
        self.cursor.execute("INSERT INTO status(url, status, msg) VALUES (?, ?, ?)", tuple([url, status, msg]))

    def close(self):
        self.connection.commit()

        self.cursor.close()
        self.connection.close()
