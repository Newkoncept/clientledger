import uuid
from datetime import datetime

from dependencies.db_dependency import db_dependency


def item_exists_in_db(db:db_dependency, model, value_to_check, column_to_be_checked:str):
    column_value = getattr(model, column_to_be_checked)
    value = db.query(model).filter(column_value == value_to_check).first()

    if not value:
        return False
    return value


def invoice_number_generator(workspace_id:int):
    INVOICE_PREFIX = "INV"
    year = datetime.now().year
    unique_value = uuid.uuid4().hex.upper()

    return f'{INVOICE_PREFIX}-{year}-WS{workspace_id}-{unique_value[:4]}-{unique_value[4:8]}-{unique_value[8:12]}'

 