import sqlite3

class MedexDatabase:

    def __init__(self):
        self.connection = sqlite3.connect("../data.db")
        self.cursor = self.connection.cursor()
        self.table_name = "medex"

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

    def post_row(self, rec: dict):
        keys = ','.join(rec.keys())
        question_marks = ','.join(list('?'*len(rec)))
        values = tuple(rec.values())
        self.cursor.execute('INSERT INTO '+self.table_name+' ('+keys+') VALUES ('+question_marks+')', values)

    def close(self):
        self.connection.commit()
        
        self.cursor.close()
        self.connection.close()