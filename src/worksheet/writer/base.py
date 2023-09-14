# from src.worksheet.reader import WorkSheetColumn, WorkSheetFormula, Formula
from src.support import quoted
from pydantic import BaseModel
import src.worksheet.reader.base as reader
from src.library.library import Library
import re
import copy
import hashlib


def null_remover(data: dict) -> dict:
    return {keys: values for keys, values in data.items() if values is not None}


class Table(BaseModel):
    name: str
    fqn: str


def table_unwrapper(data: reader.Table) -> dict:
    name = data.name
    fqn = data.fqn
    table = Table(
        name=name,
        fqn=fqn,
    )
    return table.model_dump(exclude_none=True)


class Formula(BaseModel):
    name: str
    expr: str
    was_auto_generated: bool


def replace_variables(expression: str, library: Library, target_locale: str) -> str:
    variables = re.findall(r"\[(.*?)\]", expression)
    variables_to_replace = []

    for variable in variables:
        if "::" in variable:
            pass
        else:
            variables_to_replace.append(variable)

    updated: str = copy.deepcopy(expression)

    for variable in variables_to_replace:
        uuid: str = hashlib.md5(variable.encode()).hexdigest()
        try:
            translated_variable = library.translate(key=uuid, locale=target_locale)
        except Exception:
            translated_variable = "This is an error"
        updated: str = updated.replace(variable, translated_variable)
    return updated


def formula_unwrapper(
    data: reader.Formula, library: Library, target_locale: str
) -> dict:
    expression = data.expr
    was_auto_generated = data.was_auto_generated
    uuid = data.uuid

    translated_expression: str = replace_variables(
        expression=expression, library=library, target_locale=target_locale
    )

    try:
        name = library.translate(key=uuid, locale=target_locale)
    except Exception as e:
        print(e)
        name = "This is an error"

    formula = Formula(
        name=name, expr=translated_expression, was_auto_generated=was_auto_generated
    )
    return formula.model_dump(exclude_none=True)


class Join(BaseModel):
    name: str
    source: str
    destination: str
    type: str
    is_one_to_one: bool


def join_unwrapper(data: reader.Join) -> dict:
    name = data.name
    source = data.source
    destination = data.destination
    type = data.type
    is_one_to_one = data.is_one_to_one

    join = Join(
        name=name,
        source=source,
        destination=destination,
        type=type,
        is_one_to_one=is_one_to_one,
    )
    return join.model_dump(exclude_none=True)


class WorkSheetProperties(BaseModel):
    is_bypass_rls: bool | None = None
    join_progressive: bool | None = None


def worksheet_properties_unwrapper(data: reader.WorkSheetProperties) -> dict:
    is_bypass_rls = data.is_bypass_rls
    join_progressive = data.join_progressive

    worksheet_properties = WorkSheetProperties(
        is_bypass_rls=is_bypass_rls, join_progressive=join_progressive
    )
    return worksheet_properties.model_dump(exclude_none=True)


class JoinPath(BaseModel):
    join: list[str]


class TablePath(BaseModel):
    id: str
    table: str
    join_path: list[JoinPath] | list[dict]


def table_path_unwrapper(data: reader.TablePath) -> dict:
    id = data.id
    table = data.table
    join_path: list[JoinPath] | list[dict] = data.join_path

    table_path = TablePath(id=id, table=table, join_path=join_path)
    return table_path.model_dump(exclude_none=True)


class WorkSheetColumn(BaseModel):
    name: str
    column_id: str
    properties: reader.Properties


def worksheet_column_unwrapper(
    data: reader.WorkSheetColumn, library: Library, target_locale: str
) -> dict:
    properties: reader.Properties = data.properties
    key = data.uuid
    column_id = data.column_id

    try:
        name = library.translate(key=key, locale=target_locale)
    except Exception as e:
        print(e)
        name = "This is an error"

    worksheet_column = WorkSheetColumn(
        name=name, column_id=column_id, properties=properties
    )
    return worksheet_column.model_dump(exclude_none=True)


class WorkSheetFormula(BaseModel):
    name: str
    formula_id: str
    properties: reader.Properties


def worksheet_formula_unwrapper(
    data: reader.WorkSheetFormula, library: Library, target_locale: str
) -> dict:
    properties: reader.Properties = data.properties
    key = data.uuid

    try:
        name = library.translate(key=key, locale=target_locale)
    except Exception as e:
        print(e)
        name = "This is an error"

    try:
        formula_id = library.translate(key=key, locale=target_locale)
    except Exception as e:
        print(e)
        formula_id = "This is an error"

    worksheet_formula = WorkSheetFormula(
        name=name, formula_id=formula_id, properties=properties
    )
    return worksheet_formula.model_dump(exclude_none=True)


def worksheet_item_unwrapper(
    data: reader.WorkSheetFormula | reader.WorkSheetColumn,
    library: Library,
    target_locale: str,
) -> dict:
    if isinstance(data, reader.WorkSheetFormula):
        return worksheet_formula_unwrapper(
            data=data, library=library, target_locale=target_locale
        )
    elif isinstance(data, reader.WorkSheetColumn):
        return worksheet_column_unwrapper(
            data=data, library=library, target_locale=target_locale
        )
    else:
        ValueError("Unexpected codepath")


class Parameter(BaseModel):
    id: str
    name: str
    data_type: str
    default_value: str
    list_config: reader.ListConfig | None = None
    range_config: reader.RangeConfig | None = None


def parameter_unwrapper(
    data: reader.Parameter, library: Library, target_locale: str
) -> dict:
    id = data.id
    name = data.name
    data_type = data.data_type
    default_value = data.default_value
    list_config = data.list_config
    range_config = data.range_config
    uuid = None

    try:
        name = library.translate(key=uuid, locale=target_locale)
    except Exception as e:
        print(Exception)
        name = "This is an error"

    parameter = Parameter(
        id=id,
        name=name,
        data_type=data_type,
        default_value=default_value,
        list_config=list_config,
        range_config=range_config,
    )
    return parameter.model_dump(exclude_none=True)
