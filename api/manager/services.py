from flask import jsonify, request
from config import db
from api.manager.controller import get_allManager_QueryData, get_allProjects_QueryData, add_projects_QueryData, \
    edit_projects_QueryData, delete_projects_QueryData


def get_all_managers():
    return jsonify({'msg': get_allManager_QueryData()})


def get_all_projects():
    return jsonify({'msg': get_allProjects_QueryData()})


def add_projects():
    if request.method == 'POST':
        add_data = add_projects_QueryData()
        if isinstance(add_data, str):
            return jsonify({"error": "Project Name Already Exists"})
        db.session.add(add_data)
        db.session.commit()
        return jsonify({'msg': "Project Added Successfully"}), 200
    return jsonify({'error': 'Method Not Allowed'}), 405


def edit_projects(id):
    data = edit_projects_QueryData(id)

    if data == {"error": "Data Not Found"}:
        return jsonify({"error": "Data Not Found"}), 400
    elif data == {"error": "Projects name already exists"}:
        return jsonify({"error": "Projects name already exists"}), 400
    else:
        return jsonify({"data": "Projects Updated Successfully"}), 200


def deleted_projects(id):
    data = delete_projects_QueryData(id)
    if data == {"error": "Data not found"}:
        return jsonify({"error": "Data not found"}), 400
    if data == {"error": "Data already deleted"}:
        return jsonify({"error": "Data already deleted"}), 400
    else:
        return jsonify({"msg": "Project deleted successfully"}), 200
