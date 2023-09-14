from typing import Optional
import yaml
import uuid

from src.worksheet.reader.base import (
    WorkSheetColumn,
    Table,
    Join,
    TablePath,
    Formula,
    WorkSheetColumn,
    WorkSheetFormula,
    WorkSheetProperties,
    Parameter,
    WorkSheetFull,
    WorkSheet,
)

from src.worksheet.reader.base import (
    table_wrapper,
    join_wrapper,
    formula_wrapper,
    worksheet_item_wrapper,
)


class UnwrapperMapper:
    def table_handler(self, tables: list[dict]) -> list[Table]:
        return [
            table_wrapper(data=table, index=index) for index, table in enumerate(tables)
        ]

    def join_handler(self, joins: list[dict]) -> list[Join]:
        return [
            join_wrapper(data=join, index=index) for index, join in enumerate(joins)
        ]

    def table_path_handler(self, table_paths: list[dict]) -> list[TablePath]:
        return [TablePath(**table_path) for table_path in table_paths]

    def formula_handler(self, formulas: list[dict]) -> list[Formula]:
        return [
            formula_wrapper(data=formula, index=index)
            for index, formula in enumerate(formulas)
        ]

    def parameter_handler(self, parameters: list[dict]) -> list[Parameter]:
        return [Parameter(**parameter) for parameter in parameters]

    def worksheet_column_handler(
        self, worksheet_columns: list[dict]
    ) -> list[WorkSheetColumn | WorkSheetFormula]:
        return [
            worksheet_item_wrapper(data=item, index=index)
            for index, item in enumerate(worksheet_columns)
        ]

    def worksheet_properties_column_handler(
        self, properties: list[dict]
    ) -> WorkSheetProperties:
        return WorkSheetProperties(**properties)

    tables = table_handler
    joins = join_handler
    table_paths = table_path_handler
    formulas = formula_handler
    parameters = parameter_handler
    worksheet_columns = worksheet_column_handler
    worksheet_properties = worksheet_properties_column_handler


def null_handler(data: Optional[dict], field: str) -> Optional[list]:
    if data:
        return UnwrapperMapper().__getattribute__(field)(data)
    else:
        return None


class WorkSheetReader:
    def __init__(self):
        self = self

    def read(self, path: str) -> WorkSheetFull:
        with open(path, encoding="utf8") as file:
            opened_file: dict[str, dict] = yaml.safe_load(file)

        worksheet = opened_file["worksheet"]

        self.tables: Optional[list[Table]] = null_handler(
            data=worksheet.get("tables"), field="tables"
        )
        self.joins: Optional[list[Join]] = null_handler(
            data=worksheet.get("joins"), field="joins"
        )
        self.table_paths: Optional[list[TablePath]] = null_handler(
            data=worksheet.get("table_paths"), field="table_paths"
        )
        self.formulas: Optional[list[Formula]] = null_handler(
            data=worksheet.get("formulas"), field="formulas"
        )
        self.parameters: Optional[list] = null_handler(
            data=worksheet.get("parameters"), field="parameters"
        )
        self.worksheet_columns = null_handler(
            data=worksheet.get("worksheet_columns"), field="worksheet_columns"
        )
        self.properties = null_handler(
            data=worksheet.get("properties"), field="worksheet_properties"
        )

        return WorkSheetFull(
            guid=str(uuid.uuid4()),  # can be changed to update the existing one
            worksheet=WorkSheet(
                name="test",  # is not in usage at the moment
                tables=self.tables,
                joins=self.joins,
                table_paths=self.table_paths,
                formulas=self.formulas,
                worksheet_columns=self.worksheet_columns,
                properties=self.properties,
                parameters=self.parameters,
            ),
        )
