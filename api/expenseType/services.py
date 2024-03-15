from api.expenseType.controller import get_expenseQueryData,add_expenseQueryData,edit_expenseQueryData,delete_expenseQueryData
from flask import jsonify,request
from config import db

def get_expenseType_data():
    return jsonify({'msg':get_expenseQueryData()})
def add_expenseType_data():
    if request.method == 'POST':
        add_data = add_expenseQueryData()
        if isinstance(add_data,str):
            return jsonify({"error":"Expense Already Exists"})
        db.session.add(add_data)
        db.session.commit()
        return jsonify({'msg':"Expense Type Added Successfully"}),200
    return jsonify({'error':'Method Not Allowed'}),405

def edit_expenseType_data(id):
    data = edit_expenseQueryData(id)
    if data == {"error":"Data Not Found"}:
        return jsonify({"error":"Data Not Found"}),400
    elif data == {"error": "Expense Type already exists"}:
        return jsonify({"error": "Expense Type already exists"}),400
    else:
        # data = {key: list(value) if isinstance(value,set) else value for key, value in data.items()}
        return jsonify({"msg":"Expense Type Updated Successfully"}),200

def delete_expenseType_data(id):
    data = delete_expenseQueryData(id)
    print(data)
    if data == {"error": "Data not found"}:
        return jsonify({"error": "Data not found"}), 400
    if data == {"error": "Data already deleted"}:
        return jsonify({"error": "Data already deleted"}),400
    else:
        data = {key: list(value) if isinstance(value, set) else value for key, value in data.items()}
        return jsonify({"msg": "Expense Type deleted successfully"}), 200


