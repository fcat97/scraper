import sqlite3
from medex_dot_com.utils import create_dir, db_directory, safe_run
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

        self.__do_migration()

    def insert_record(self, rec: dict):
        keys = ','.join(rec.keys())
        question_marks = ','.join(list('?'*len(rec)))
        values = tuple(rec.values())
        self.cursor.execute('INSERT INTO '+self.table_name+' ('+keys+') VALUES ('+question_marks+')', values)

    def save_status(self, url: str, status: str, msg: str|None):
        self.cursor.execute("INSERT INTO status(url, status, msg) VALUES (?, ?, ?)", tuple([url, status, msg]))

    @safe_run
    def __do_migration(self):
        self.cursor.execute('PRAGMA user_version')
        version = self.cursor.fetchone()[0]

        if version == 0:
            self.__migrate_to_v1()
            self.cursor.execute('PRAGMA user_version = 1')

    def __migrate_to_v1(self):
        self.cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = [col[1] for col in self.cursor.fetchall()]
        columns_str = ', '.join(columns)

        self.cursor.execute(f"ALTER TABLE {self.table_name} RENAME TO old_{self.table_name}")

        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}(
                id INTEGER primary key AUTOINCREMENT,
                url TEXT,
                name TEXT,
                type TEXT,
                generic_group TEXT,
                manufacturer TEXT,
                strength TEXT,
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
                storage_conditions TEXT,
                composition TEXT,
                overdose_effects TEXT,
                compound_summary TEXT,
                commonly_asked_questions TEXT
            )
        """)

        self.cursor.execute(f'INSERT INTO {self.table_name} ({columns_str}) SELECT {columns_str} FROM old_{self.table_name}')
        self.cursor.execute(f"DROP TABLE old_{self.table_name}")

    def close(self):
        self.connection.commit()

        self.cursor.close()
        self.connection.close()
