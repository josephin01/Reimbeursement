from api.user.models import Purpose_Of_Visit
from flask import request
from config import db

def get_purposeQuery_data():
    data = Purpose_Of_Visit.query.filter_by(deleted_at=None).all()
    data_list = []
    for i in data:
        data_list.append({
            'id':i.id,
            'purposes':i.purposes
        })
    return {'data': data_list}

def add_purposeQuery_data():
    data = request.get_json()
    purposes= data.get('purposes')

    existing_purposes = Purpose_Of_Visit.query.filter_by(purposes=purposes).first()
    if existing_purposes:
        if existing_purposes.deleted_at is not None:
            existing_purposes.deleted_at = None
            return existing_purposes
        else:
            return "Purpose Already Exists"
        return f"Purposes {purposes} Already Exists"

    new_add_purpose = Purpose_Of_Visit(purposes=purposes)
    return new_add_purpose

def edit_purposeQuery_data(id):
    data = request.get_json()
    purposes = data.get('purposes')
    data_update = Purpose_Of_Visit.query.filter_by(id=id).first()
    existing_purposes = Purpose_Of_Visit.query.filter_by(purposes=purposes).first()
    if not data_update:
        return {"error": "Data Not Found"}
    if existing_purposes:
        return {"error":"Purpose Already Exists"}
    if purposes is not None:
        data_update.purposes = purposes
    db.session.commit()

    if purposes is not None:
        return {"msg": "Purpose Updated Successfully"}
def delete_purposeQuery_data(id):
    data = Purpose_Of_Visit.query.filter_by(id=id).first()
    if not data:
        return {"error":"Data not found"}
    elif data.deleted_at:
        return {"error": "Data already deleted"}
    else:
        data.delete()
        return {"msg": "Purpose deleted successfully"}