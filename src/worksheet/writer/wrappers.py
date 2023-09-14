from typing import Optional, Union
from src.library.library import Library
import yaml
from src.worksheet.reader.base import (
    Table,
    Formula,
    Join,
    Parameter,
    WorkSheetProperties,
    WorkSheetFormula,
    WorkSheetColumn,
    WorkSheetFull,
    WorkSheet,
    TablePath,
)

from src.worksheet.writer.base import (
    table_unwrapper,
    formula_unwrapper,
    join_unwrapper,
    worksheet_properties_unwrapper,
    table_path_unwrapper,
    parameter_unwrapper,
    worksheet_item_unwrapper,
)


class WrapperMapper:
    def __init__(self, library: Library, target_locale: str):
        self = self
        self.library = library
        self.target_locale = target_locale

    def table_handler(self, tables: Optional[list[Table]]) -> Optional[list[dict]]:
        if tables:
            return [table_unwrapper(data=table) for _, table in enumerate(tables)]
        else:
            return None

    def formula_handler(
        self, formulas: Optional[list[Formula]]
    ) -> Optional[list[dict]]:
        if formulas:
            return [
                formula_unwrapper(
                    data=table, library=self.library, target_locale=self.target_locale
                )
                for _, table in enumerate(formulas)
            ]
        else:
            return None

    def join_handler(self, joins: Optional[list[Join]]) -> Optional[list[dict]]:
        if joins:
            return [join_unwrapper(data=join) for _, join in enumerate(joins)]
        else:
            return None

    def worksheet_properties_handler(
        self, worksheet_properties: Optional[WorkSheetProperties]
    ) -> Optional[dict]:
        if worksheet_properties:
            return worksheet_properties_unwrapper(data=worksheet_properties)
        else:
            return None

    def table_path_handler(
        self, table_paths: Optional[list[TablePath]]
    ) -> Optional[list[dict]]:
        if table_paths:
            return [
                table_path_unwrapper(data=table_path)
                for _, table_path in enumerate(table_paths)
            ]
        else:
            return None

    def parameter_handler(
        self, parameters: Optional[list[Parameter]]
    ) -> Optional[list[dict]]:
        if parameters:
            return [
                parameter_unwrapper(
                    data=parameter,
                    library=self.library,
                    target_locale=self.target_locale,
                )
                for _, parameter in enumerate(parameters)
            ]
        else:
            return None

    def column_handler(
        self, columns: Optional[list[WorkSheetColumn | WorkSheetFormula]]
    ) -> Optional[list[dict]]:
        if columns:
            return [
                worksheet_item_unwrapper(
                    data=column, library=self.library, target_locale=self.target_locale
                )
                for _, column in enumerate(columns)
            ]
        else:
            return None


class WorkSheetWriter:
    def __init__(self, full_worksheet: WorkSheetFull, name: str, library: Library):
        self = self
        self.full_worksheet = full_worksheet
        self.type = "worksheet"
        self.name = name
        self.library = library

    def transform(self, guid: str, target_locale: str):
        name = self.name
        self.target_locale = target_locale

        worksheet: WorkSheet = self.full_worksheet.worksheet
        tables: Optional[list[Table]] = worksheet.tables
        formulas: Optional[list[Formula]] = worksheet.formulas
        joins: Optional[list[Join]] = worksheet.joins
        worksheet_properties: Optional[WorkSheetProperties] = worksheet.properties
        table_paths: Optional[list[TablePath]] = worksheet.table_paths
        parameters: Optional[list[Parameter]] = worksheet.parameters
        columns: Optional[
            list[WorkSheetColumn | WorkSheetFormula]
        ] = worksheet.worksheet_columns
        wrapper: WrapperMapper = WrapperMapper(
            library=self.library, target_locale=target_locale
        )

        table_section: dict[str, Optional[list]] = {
            "tables": wrapper.table_handler(tables=tables)
        }
        formula_section: dict[str, Optional[list]] = {
            "formulas": wrapper.formula_handler(formulas=formulas)
        }
        join_section: dict[str, Optional[list]] = {
            "joins": wrapper.join_handler(joins=joins)
        }
        properties_section: dict[str, Optional[dict]] = {
            "properties": wrapper.worksheet_properties_handler(
                worksheet_properties=worksheet_properties
            )
        }
        table_path_section: dict[str, Optional[list]] = {
            "table_paths": wrapper.table_path_handler(table_paths=table_paths)
        }
        parameters_section: dict[str, Optional[list]] = {
            "parameters": wrapper.parameter_handler(parameters=parameters)
        }
        worksheet_section: dict[str, Optional[list]] = {
            "worksheet_columns": wrapper.column_handler(columns=columns)
        }

        wrapped_worksheet = {"name": name}
        """Following ensures no nulls are in the final output as TML will throw an error"""
        for section in [
            table_section,
            formula_section,
            join_section,
            properties_section,
            table_path_section,
            parameters_section,
            worksheet_section,
        ]:
            for keys, values in section.items():
                if values:
                    wrapped_worksheet[keys] = values

        data: dict[str, Union[dict, str]] = {
            "guid": guid,
            "worksheet": wrapped_worksheet,
        }
        self.data: dict = data
        return self

    def write(self, output_dir: str) -> None:
        assert self.target_locale, "Locale not set"

        output_path: str = f"{output_dir}/locale-{self.target_locale}-{self.name}.tml"

        with open(output_path, "w") as file:
            yaml.dump(
                self.data, file, indent=2, default_flow_style=False, explicit_start=True
            )
        # file.close()
        print(f"YAML saved to {output_path}.")
