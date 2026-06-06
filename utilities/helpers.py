from dependencies.db_dependency import db_dependency


def item_exists_in_db(db:db_dependency, model, value_to_check, column_to_be_checked:str):
    column_value = getattr(model, column_to_be_checked)
    value = db.query(model).filter(column_value == value_to_check).first()

    if not value:
        return False
    
    return value


