"""Currently unused"""
from pydantic import BaseModel, field_validator
from typing import Union
import hashlib

from src.worksheet.reader import Table, Formula


class NumberFormatConfig(BaseModel):
    unit: str
    decimals: float
    negativeValueFormat: str
    toSeparateThousands: bool


class AnswerFormat(BaseModel):
    category: str
    numberFormatConfig: NumberFormatConfig
    isCategoryEditable: bool


class AnswerColumn(BaseModel):
    name: str
    format: AnswerFormat


class TableColumn:
    column_id: str
    show_headline: bool
    uuid: str


class AnswerTable(BaseModel):
    table_columns: list[TableColumn]
    ordered_column_ids = list[str]
    client_state: str
    client_state_v2: str


class ChartColumn(BaseModel):
    column_id: str
    uuid: str


class Chart(BaseModel):
    type: str
    chart_columns: list[ChartColumn]
    axis_configs: None
    client_state: str
    client_state_v2: str


class Answer(BaseModel):
    id: str
    tables: list[Table]
    formulas: list[Formula]
    search_query: str
    answer_columns: list[AnswerColumn]
    table: AnswerTable
    chart: Chart
    display_mode: str


class Visualisation(BaseModel):
    id: str
    answer: Answer
    viz_guid: str
    note_tile: None


class DateFilter(BaseModel):
    type: str
    date: str
    oper: str


class FilterColumn(BaseModel):
    column: list[str]
    excluded_visualizations: list[str] | None
    is_mandatory: bool
    date_filter: DateFilter | None


class Tile(BaseModel):
    visualisation_id: str
    x: int
    y: int
    height: int
    width: int


class Tab(BaseModel):
    name: str
    description: str
    tiles: list[Tile]


class OverrideValue(BaseModel):
    name: str
    id: str


class ParameterOverride(BaseModel):
    key: str
    value: OverrideValue


class Layout(BaseModel):
    tabs: list[Tab]
    parameter_overrides: list[ParameterOverride]


class LiveBoard(BaseModel):
    name: str
    visualisations: list[Visualisation]
    filters: list
    layout: Layout


class LiveboardFull(BaseModel):
    guid: str
    liveboard: LiveBoard
