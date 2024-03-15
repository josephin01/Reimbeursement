# routing
from flask import Blueprint, request
from api.user.services import (get_all_employees, add_employee,
                               get_employee, get_all_roles,
                               change_roles, user_role,
                               get_dashboard_data, get_status_table_data,
                               get_view_table_data, update_status_travel_form, get_view_table_data_travelForm)
from flask_jwt_extended import jwt_required, get_jwt_identity
from common.response import success_response

user_api = Blueprint('user_api', __name__, url_prefix='/user')


@user_api.route('/index', methods=["GET"])
def index():
    return "Hello world"


@user_api.route('/getAllEmployees', methods=["GET"])
def getAllEmployees():
    return get_all_employees()


@user_api.route('/addEmployee', methods=["POST"])
def addEmployee():
    return add_employee()


@user_api.route('/getEmployee/<int:empId>', methods=["GET"])
def getEmployee(empId):
    return get_employee(empId)


@user_api.route('/getAllRoles', methods=["GET"])
def getAllRoles():
    return get_all_roles()


@user_api.route('/change-role/<int:empId>', methods=["POST"])
def changeRole(empId):
    return change_roles(empId)


@user_api.route('/dashboard', methods=['GET'])
# @jwt_required()
def dashboard():
    # u_id = get_jwt_identity()
    data = request.get_json()
    u_id = data.get('u_id')
    role = user_role(u_id)
    dashboard_data = get_dashboard_data(role)
    return success_response(status_code=200, content=dashboard_data)


@user_api.route('/travelExpense', methods=['GET'])
# @jwt_required()
def travel_expense():
    # u_id = get_jwt_identity()
    data = request.get_json()
    u_id = data.get('u_id')
    status = request.args.get('status')
    role = user_role(u_id)
    status_table_data = get_status_table_data(role, status)
    return success_response(status_code=200, content=status_table_data)


@user_api.route('/travelExpensesView', methods=["GET"])
# @jwt_required()
def travel_expenses_view():
    # u_id = get_jwt_identity()
    data = request.get_json()
    u_id = data.get('u_id')
    travel_form_id = data.get('travel_form_id')
    role = user_role(u_id)
    view_table_data = get_view_table_data(role, travel_form_id)
    return success_response(status_code=200, content=view_table_data)


@user_api.route('/statusUpdate/travelForm', methods=["PATCH"])
# @jwt_required()
def travel_form_status_update():
    # u_id = get_jwt_identity()
    data = request.get_json()
    u_id = data.get('u_id')
    travel_form_id = data.get('travel_form_id')
    role = user_role(u_id)
    status = data.get('status')
    status_update = update_status_travel_form(role, travel_form_id, status)
    return success_response(status_code=200, content=status_update)

@user_api.route('/travelFormView', methods=["GET"])
# @jwt_required()
def travel_form_view():
    # u_id = get_jwt_identity()
    data = request.get_json()
    u_id = data.get('u_id')
    travel_form_id = data.get('travel_form_id')
    role = user_role(u_id)
    view_table_data_travelForm = get_view_table_data_travelForm(role, travel_form_id)
    return success_response(status_code=200, content=view_table_data_travelForm)

