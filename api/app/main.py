from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, field_validator, ValidationInfo
from modules.wrappers import DBConnector, Translator


app = FastAPI()


class TranslationRequest(BaseModel):
    """
    Data model for the user request
    """
    source_language: Literal['en', 'de']
    destination_language: Literal['en', 'de']
    text: str

    @field_validator("destination_language")
    def non_identical_languages(cls, v:str, info: ValidationInfo):
        if v == info.data['source_language']:
            raise ValueError("source and destination languages must be different")
        return v


@app.get("/translate")
def predict(request: Annotated[TranslationRequest, Query()]):
    """
    main endpoint for the user to translate a text. What happens:

    1. translates the text
    2. stores the translated text alongside the source and destination languages to the DB
    """
    # setup
    # TODO: read the "location" parameter dynamically
    translator = Translator(request.source_language, request.destination_language, location="ON-PREM").translator_obj
    db = DBConnector(location='ON-PREM').db_obj

    # translate
    text = translator.predict(request.text)
    
    # store
    db.write_data([request.source_language, request.destination_language, text])

    return text
