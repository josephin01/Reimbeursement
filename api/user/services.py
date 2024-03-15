from flask import jsonify, request
from config import db
from api.user.controller import get_employeeQuery_data, add_employeeQuery_data, get_employeeQuery_databyId, \
    get_rolesQuery_data, change_rolesQuery_data, get_admin_dashboard, get_admin_status_table, get_admin_view_table_data, \
    status_update_travel_form, get_admin_view_travel_form
from api.auth.controller import get_data
from datetime import datetime


def get_all_employees():
    return jsonify({'msg': get_employeeQuery_data()})


def add_employee():
    if request.method == 'POST':
        add_employee = add_employeeQuery_data()
        if isinstance(add_employee, str):
            return jsonify({"error": "Employee Already Exists"}), 400

        db.session.add(add_employee)
        db.session.commit()
        return jsonify({"msg": "Employee Added Successfully"}), 200
    return jsonify({'error': 'Method Not Allowed'}), 405


def get_employee(empId):
    return jsonify({'msg': get_employeeQuery_databyId(empId)})


def get_all_roles():
    role_data = get_rolesQuery_data()
    return jsonify({'msg': role_data})


def change_roles(empId):
    data = change_rolesQuery_data(empId)

    if data == {'error': 'Invalid role specified'}:
        return jsonify({'error': 'Invalid role specified'}), 400
    elif data == {'error': 'User not found'}:
        return jsonify({'error': 'User not found'}), 400
    else:
        return jsonify({"msg": "Role updated successfully"}), 200


def user_role(u_id):
    return get_data(u_id).role.value


def get_dashboard_data(role):
    if role == 'ADMIN':
        return get_admin_dashboard()
    elif role == 'MANAGER':
        return []
    elif role == 'EMPLOYEE':
        return []
    return None


def get_status_table_data(role, status):
    if role == 'ADMIN':
        data = get_admin_status_table(status)
        res = []
        for i in data:
            res.append({
                'date': i[0].__str__(),
                'amount': i[1],
                'status': i[2].value,
                'fname': i[3],
                'project_name': i[4],
                'travel_form_id': i[5]
            })
        return res
    elif role == 'MANAGER':
        return []
    elif role == 'EMPLOYEE':
        return []
    return None


def get_view_table_data(role, travel_form_id):
    if role == 'ADMIN':
        raw_data = get_admin_view_table_data(travel_form_id)
        data = {}
        travel_form_data = raw_data['travel_form_data'][0]
        data['id'] = travel_form_data[0]
        data['purposeOfVisit'] = travel_form_data[1]
        data['applyDate'] = travel_form_data[2].__str__()
        data['colleagueDetails'] = travel_form_data[3]
        data['numberOfPeople'] = travel_form_data[4]
        data['travelDate'] = travel_form_data[5].__str__()
        data['projectScope'] = travel_form_data[6]
        data['projectName'] = travel_form_data[7]
        data['managerName'] = travel_form_data[8]
        data['expensesList'] = []
        for row in raw_data['expense_form_data']:
            data['expensesList'].append({
                'id': row[0],
                'expenseType': {
                    'id': row[1],
                    'expenses': row[2]
                },
                'expenseDescription': row[3],
                'expenseDate': row[4].__str__(),
                'expenseAmount': row[5],
                'applyDate': row[6].__str__(),
                'bills': []
            })
        for expense in data['expensesList']:
            for bill in raw_data['bills_form_data']:
                if expense['id'] == bill[0]:
                    expense['bills'].append({
                        'id': bill[1],
                        'billsUrl': bill[2],
                        'billType': bill[3],
                        'billName': bill[4]
                    })
                else:
                    pass
        return data
    elif role == 'MANAGER':
        return []
    elif role == 'EMPLOYEE':
        return []
    return None


def update_status_travel_form(role, travel_form_id, status):
    if role == 'ADMIN':
        expense_form_status = f"ADMIN_{status.split('_')[1]}"
        return status_update_travel_form(status, expense_form_status, travel_form_id)
    elif role == 'MANAGER':
        return []
    elif role == 'EMPLOYEE':
        return []
    return None


def get_view_table_data_travelForm(role, travel_form_id):
    if role == 'ADMIN':
        raw_data = get_admin_view_travel_form(travel_form_id)
        data = {}
        travel_form_data = raw_data['travel_form_data'][0]
        data['purpose'] = travel_form_data[0]
        data['date'] = travel_form_data[1].__str__()
        data['colleague_details'] = travel_form_data[2]
        data['no_of_people'] = travel_form_data[3]
        data['travelDate'] = travel_form_data[4].__str__()
        data['projectScope'] = travel_form_data[5]
        data['projectName'] = travel_form_data[6]
        data['managerName'] = travel_form_data[7]

    elif role == 'MANAGER':
        return []
    elif role == 'EMPLOYEE':
        return []
    return None
