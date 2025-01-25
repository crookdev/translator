from transformers import pipeline

class GoogleTranslator:
    def __init__(self, source_lang, dest_lang):
        self.pipeline = pipeline(f"translation_{source_lang}_to_{dest_lang}", model="google-t5/t5-small")
    
    def predict(self, text):
        return self.pipeline(text)[0]['translation_text']
