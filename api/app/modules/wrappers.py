from modules.local_cognitive_models import GoogleTranslator
from modules.db_connectors import PostgresDB


class DBConnector:
    def __init__(self, location):
        if location == 'ON-PREM':
            self.db_obj = PostgresDB()
        else:
            raise ValueError(f"location {location} is not implemented.")


class Translator:
    def __init__(self, source_language, destination_language, location):
        if location == 'ON-PREM':
            self.translator_obj = GoogleTranslator(source_lang=source_language, dest_lang=destination_language)
        else:
            raise ValueError(f"location {location} is not implemented.")