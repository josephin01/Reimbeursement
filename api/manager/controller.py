from api.user.models import Managers,Projects
from flask import request
from config import db

def get_allManager_QueryData():
    data = Managers.query.filter_by(deleted_at=None).all()
    data_list = []
    for i in data:
        data_list.append({
            'id':i.id,
            ' manager_name': i.manager_name
        })
    return {'data':data_list}

def get_allProjects_QueryData():
    data = Projects.query.filter_by(deleted_at=None).all()
    data_list = []
    for i in data:
        data_list.append({
            'id':i.id,
            'project_name': i.project_name
        })
    return {'data':data_list}

def add_projects_QueryData():
    data = request.get_json()
    project_name = data.get('project_name')
    manager_id = data.get('manager_id')

    existing_project = Projects.query.filter_by(project_name=project_name).first()
    if existing_project:
        if existing_project.deleted_at is not None:
            existing_project.deleted_at = None
            return  existing_project
        else:
            return "Project name already exists"
        return "Project Name already exists"

    new_add_project = Projects(project_name=project_name,manager_id=manager_id)
    return new_add_project

def edit_projects_QueryData(id):
    data = request.get_json()
    project_name = data.get('project_name')
    manager_id = data.get('manager_id')
    data_update = Projects.query.filter_by(id=id).first()
    existing_projects = Projects.query.filter_by(project_name=project_name).first()
    if not data_update:
        return {"error":"Data Not Found"}
    if existing_projects:
        return {"error":"Projects name already exists"}
    if project_name is not None and manager_id is not None:
        data_update.project_name = project_name
        data_update.manager_id = manager_id
    db.session.commit()
    if project_name is not None and manager_id is not None:
        return {"data":"Projects Updated Successfully"}

def delete_projects_QueryData(id):
    data = Projects.query.filter_by(id=id).first()
    if not data:
        return {"error": "Data not found"}
    elif data.deleted_at:
        return {"error": "Data already deleted"}
    else:
        data.delete()
        return {"msg": "Project deleted successfully"}

