import uuid
from datetime import datetime

from dependencies.db_dependency import db_dependency


def get_db_item_by_column(db:db_dependency, model, column_name:str, value):
    column = getattr(model, column_name, None)
    return db.query(model).filter(column == value).first()


def invoice_number_generator(workspace_id:int):
    INVOICE_PREFIX = "INV"
    year = datetime.now().year
    unique_value = uuid.uuid4().hex.upper()

    return f'{INVOICE_PREFIX}-{year}-WS{workspace_id}-{unique_value[:4]}-{unique_value[4:8]}-{unique_value[8:12]}'

 