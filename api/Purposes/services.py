from flask import jsonify,request
from config import db
from api.Purposes.controller import get_purposeQuery_data,add_purposeQuery_data,edit_purposeQuery_data,delete_purposeQuery_data

def get_purposeOfVisit():
    return jsonify({'msg': get_purposeQuery_data()})

def add_purposeOfVisit():
    if request.method == 'POST':
        add_data = add_purposeQuery_data()
        if isinstance(add_data,str):
            return jsonify({"error":"Purpose Already Exists"})
        db.session.add(add_data)
        db.session.commit()
        return jsonify({'msg':"Purpose Added Successfully"}),200
    return jsonify({'error':'Method Not Allowed'}),405

def edit_purposeOfVisit(id):
    data = edit_purposeQuery_data(id)

    if data == {"error":"Data Not Found"}:
        return jsonify({"error":"Data Not Found"}),400
    elif data == {"error":"Purpose Already Exists"}:
        return  jsonify({"error":"Purpose Already Exists"}),400
    else:
        # data = {key: list(value) if isinstance(value,set) else value for key, value in data.items()}
        return jsonify({"msg":"Purposes Updated Successfully"}),200

def delete_purposeOfVisit(id):
    data = delete_purposeQuery_data(id)

    if data == {"error": "Data not found"}:
        return jsonify({"error": "Data not found"}), 400
    if data == {"error": "Data already deleted"}:
        return jsonify({"error": "Data already deleted"}), 400
    else:
        data = {key: list(value) if isinstance(value, set) else value for key, value in data.items()}
        return jsonify({"msg": "Purpose deleted successfully"}), 200
