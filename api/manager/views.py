from flask import Blueprint
from api.manager.services import get_all_managers,get_all_projects,add_projects,edit_projects,deleted_projects

manager_api = Blueprint('manager_api',__name__,url_prefix='/manager')

@manager_api.route('/getAllManagers',methods=["GET"])
def getAllManagers():
    return get_all_managers()

@manager_api.route('/getAllProjects',methods =["GET"])
def getAllProjects():
    return get_all_projects()

@manager_api.route('/addProject',methods=["POST"])
def addProject():
    return add_projects()

@manager_api.route('/editProject/<int:id>',methods = ["POST"])
def editProject(id):
    return edit_projects(id)

@manager_api.route('/deleteProject/<int:id>',methods = ["DELETE"])
def deleteProject(id):
    return deleted_projects(id)