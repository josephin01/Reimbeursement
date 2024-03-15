from flask import jsonify, request
from config import db
from api.travelForm.controller import add_travel_form, get_all_travelForm
from datetime import datetime


def add_travelForm():
    if request.method == 'POST':
        add_data = add_travel_form()
        db.session.add(add_data)
        db.session.commit()
        return jsonify({'msg': 'Travel Form Added Successfully'})
    return jsonify({'msg': 'Method Not Allowed'})


def get_travel_forms():
    raw_data = get_all_travelForm()
    data = []
    for i in raw_data:
        data.append({
            'date': i[0].__str__(),
            'project_name': i[1],
            'status': i[2].value,
            'purposes': i[3],
            'date_of_travel': i[4].strftime('%Y-%m-%d')
        })
    return jsonify({'msg': data})


def get_travelForm_byId(id):
    return
