from pydantic import BaseModel, field_validator
from typing import Union, Optional
import hashlib


def get_uuid(name: str) -> str:
    return hashlib.md5(string=name.encode()).hexdigest()


class Table(BaseModel):
    name: str
    fqn: str
    uuid: str
    index: int


def table_wrapper(data: dict, index: int) -> Table:
    name: Optional[str] = data.get("name")
    return Table(
        name=name, fqn=data.get("fqn"), uuid=get_uuid(data.get("name")), index=index
    )


class Join(BaseModel):
    name: str
    source: str
    destination: str
    type: str
    is_one_to_one: bool
    uuid: str
    index: int


def join_wrapper(data: dict, index: int) -> Join:
    return Join(
        name=data.get("name"),
        source=data.get("source"),
        destination=data.get("destination"),
        type=data.get("type"),
        is_one_to_one=data.get("is_one_to_one"),
        uuid=get_uuid(data.get("name")),
        index=index,
    )


class JoinPath(BaseModel):
    join: list[str]


class TablePath(BaseModel):
    id: str
    table: str
    join_path: list[JoinPath] | list[dict]


class Formula(BaseModel):
    name: str
    expr: str
    was_auto_generated: bool
    uuid: str
    index: int


def formula_wrapper(data: dict, index: int) -> Formula:
    return Formula(
        name=data.get("name"),
        expr=data.get("expr"),
        was_auto_generated=data.get("was_auto_generated"),
        uuid=get_uuid(data.get("name")),
        index=index,
    )


class Properties(BaseModel):
    column_type: str
    aggregation: str | None = None
    index_type: str | None = None
    value_casing: str | None = None


def properties_wrapper(data: dict[str, str]) -> Properties:
    return Properties(
        column_type=data.get("column_type"),
        aggregation=data.get("aggregation"),
        index_type=data.get("index_type"),
        value_casing=data.get("value_casing"),
    )


class WorkSheetColumn(BaseModel):
    name: str
    column_id: str
    properties: Properties
    uuid: str
    index: int


def column_wrapper(data: dict[str, str], index: int) -> WorkSheetColumn:
    return WorkSheetColumn(
        name=data.get("name"),
        column_id=data.get("column_id"),
        properties=properties_wrapper(data=data.get("properties")),
        uuid=get_uuid(data.get("name")),
        index=index,
    )


class WorkSheetFormula(BaseModel):
    name: str
    formula_id: str
    properties: Properties
    uuid: str
    index: int


def worksheet_formula_wrapper(data: dict, index: int) -> WorkSheetFormula:
    return WorkSheetFormula(
        name=data.get("name"),
        formula_id=data.get("formula_id"),
        properties=properties_wrapper(data=data.get("properties")),
        uuid=get_uuid(data.get("name")),
        index=index,
    )


def worksheet_item_wrapper(
    data: dict, index: int
) -> WorkSheetColumn | WorkSheetFormula:
    if "column_id" in data.keys():
        return column_wrapper(data=data, index=index)
    elif "formula_id" in data.keys():
        return worksheet_formula_wrapper(data=data, index=index)
    else:
        raise ValueError("No worksheetcolumn or worksheetformula is found")


class WorkSheetProperties(BaseModel):
    is_bypass_rls: bool | None = None
    join_progressive: bool | None = None


class ListChoice(BaseModel):
    value: str
    display_name: str


class ListConfig(BaseModel):
    list_choice: list[ListChoice]


class RangeConfig(BaseModel):
    range_min: str
    range_max: str
    include_min: bool
    include_max: bool


class Parameter(BaseModel):
    id: str
    name: str
    data_type: str
    default_value: str
    list_config: ListConfig | None = None
    range_config: RangeConfig | None = None


class WorkSheet(BaseModel):
    name: str
    tables: list[Table] | None
    joins: list[Join] | None
    table_paths: list[TablePath] | None
    formulas: list[Formula] | None
    worksheet_columns: list[WorkSheetColumn | WorkSheetFormula]
    properties: WorkSheetProperties | None
    parameters: list[Parameter] | None


class WorkSheetFull(BaseModel):
    guid: str
    worksheet: WorkSheet
