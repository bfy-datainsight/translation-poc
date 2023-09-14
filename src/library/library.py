from pydantic import BaseModel
from typing import Optional
import yaml
from src.worksheet.reader.base import WorkSheetColumn, WorkSheetFormula, WorkSheetFull


class Locale(BaseModel):
    nl: str | None
    se: str | None
    es: str | None


class Translation(BaseModel):
    key: str
    id: str
    name: str
    locale: Locale


class Library:
    def __init__(
        self,
        full_worksheet: WorkSheetFull | None = None,
        languages: list[str] | None = None,
    ):
        self = self
        self.full_worksheet = full_worksheet
        self.languages = languages

    def construct_base(self):
        if not self.full_worksheet:
            raise ValueError("No worksheet available")

        assert self.languages

        self.translations: list[Translation] = []

        for items in self.full_worksheet.worksheet.worksheet_columns:
            key: str = items.uuid
            name: str = items.name
            if isinstance(items, WorkSheetColumn):
                id: str = items.column_id
            elif isinstance(items, WorkSheetFormula):
                id: str = items.formula_id
            else:
                raise ValueError("No instance of worksheet item found")

            locales = {language: None for language in self.languages}
            self.translations.append(
                Translation(key=key, name=name, id=id, locale=Locale(**locales))
            )
        return self

    def write_translation_file(self, file_name: str = "content/library/output.yml"):
        self.construct_base()
        output: list[dict] = [model.model_dump() for model in self.translations]
        file = open(file_name, "w")
        yaml.dump(output, file, indent=4, default_flow_style=False, explicit_start=True)
        file.close()
        print("YAML saved to {file_name}.")

    def from_file(self, path: str):
        with open(path, encoding="utf8") as file:
            opened_file: dict = yaml.safe_load(file)

        self.translations: list[Translation] = []
        for elements in opened_file:
            key: Optional[str] = elements.get("key")
            name: Optional[str] = elements.get("name")
            id: Optional[str] = elements.get("id")
            locale: Optional[dict[str, str]] = elements.get("locale")
            assert key, "The key is null and should not be"
            assert name, "The name is null and should not be"
            assert id, "The id is null and should not be"
            assert locale, "The locale is null and should not be"

            self.translations.append(
                Translation(key=key, name=name, id=id, locale=Locale(**locale))
            )
        return self

    def translate(self, key: str, locale: str) -> str:
        assert self.translations
        translation = [
            translation for translation in self.translations if translation.key == key
        ][0]
        translated_string = translation.locale.model_dump()[locale]
        if translated_string:
            return translated_string
        else:
            return translation.name
