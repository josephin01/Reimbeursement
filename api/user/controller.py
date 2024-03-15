from api.user.models import (User, Expenses, Expense_Claim,
                             ExpensesStatus, TravelFormStatus,
                             TravelForm, Projects, Purpose_Of_Visit,
                             ExpenseType, Bills)
from config import db
from flask import request
from api.user.models import Roles, Managers


def get_employeeQuery_data():
    data = User.query.filter(User.email != "admin@gmail.com").all()
    data_list = []

    for i in data:
        data_list.append({
            'email': i.email,
            'empId': i.empId,
            'fname': i.fname,
            'lname': i.lname,
            'contact': i.contact,
            'dob': i.dob,
            'role': i.role.value
        })
    return {'data': data_list}


def add_employeeQuery_data():
    data = request.get_json()
    email = data.get('email', None)
    fname = data.get('fname', None)
    lname = data.get('lname', None)
    contact = data.get('contact', None)
    dob = data.get('dob', None)
    role = data.get('role', 'EMPLOYEE').upper()
    password = data.get('password', None)
    empId = data.get('empId', None)
    is_manager = False

    existing_user = User.query.filter_by(email=email, empId=empId).first()
    if existing_user:
        if existing_user.deleted_at is not None:
            existing_user.deleted_at = None
        else:
            return "Employee Already Exists"
    user = User(email=email, fname=fname, lname=lname, contact=contact, dob=dob,
                password=password, role=role, empId=empId, is_manager=is_manager)
    return user


def get_employeeQuery_databyId(empId):
    data = User.query.filter_by(empId=empId).all()
    data_list = []
    for i in data:
        data_list.append({
            'email': i.email,
            'empId': i.empId,
            'fname': i.fname,
            'lname': i.lname,
            'contact': i.contact,
            'dob': i.dob,
            'role': i.role.value
        })
    return {'data': data_list}


def get_rolesQuery_data():
    enum_roles = []
    for i in Roles:
        enum_roles.append(i.value)
    print(enum_roles)
    return {'data': enum_roles}


def change_rolesQuery_data(empId):
    data = request.get_json()
    new_role = data.get('role')
    user = User.query.filter_by(empId=empId).first()
    if user:
        if new_role == 'MANAGER':
            user.role = new_role
            user.is_manager = True
            manager = Managers(
                manager_name=user.fname,
                user_id=user.id
            )
            db.session.add(manager)
            new_manager = db.session.query(Managers).filter_by(manager_name=user.fname).first()
            user.manager_id = new_manager.id
            db.session.commit()
            return {'message': 'Role updated successfully '}
        elif new_role in Roles.__members__:  #
            user.role = new_role
            user.is_manager = False
            db.session.commit()
            return {'message': 'Role updated successfully'}
        else:
            return {'error': 'Invalid role specified'}
    else:
        return {'error': 'User not found'}


def get_admin_dashboard():
    travel_expenses = {}
    for status in ExpensesStatus:
        travel_expenses[status.value] = Expenses.query.filter_by(expense_status=status).count()
    expenses_claim = {}
    for status in ExpensesStatus:
        expenses_claim[status.value] = Expense_Claim.query.filter_by(expense_status=status).count()
    travel_form = {}
    for status in TravelFormStatus:
        travel_form[status.value] = TravelForm.query.filter_by(travel_status=status).count()
    return {'travel_expenses': travel_expenses, 'expenses_claim': expenses_claim, 'travel_form': travel_form}


def get_admin_status_table(status):
    sub_query = (db.session.query(Expenses.apply_date, Expenses.expense_amount,
                                  Expenses.expense_status, TravelForm.user_id,
                                  TravelForm.project_id, TravelForm.id)
                 .join(Expenses)
                 .filter_by(expense_status=status)
                 .subquery())

    travel_expense_data = (db.session.query(sub_query.c.apply_date, sub_query.c.expense_amount,
                                            sub_query.c.expense_status, User.fname,
                                            Projects.project_name, sub_query.c.id)
                           .join(User, User.id == sub_query.c.user_id)
                           .join(Projects, Projects.id == sub_query.c.project_id)
                           .all())
    return travel_expense_data


def get_admin_view_table_data(travel_form_id):
    travel_form_data = (db.session.query(TravelForm.id, Purpose_Of_Visit.purposes, TravelForm.apply_date,
                                         TravelForm.colleague_details, TravelForm.number_of_people,
                                         TravelForm.travel_date, TravelForm.description,
                                         Projects.project_name, Managers.manager_name)
                        .join(Projects, Projects.id == TravelForm.project_id)
                        .join(Managers, Managers.id == TravelForm.manager_id)
                        .join(Purpose_Of_Visit, Purpose_Of_Visit.id == TravelForm.purpose_of_visit_id)
                        .filter(TravelForm.id == travel_form_id)
                        .all())
    expense_form_data = (db.session.query(Expenses.id, Expenses.expense_type_id, ExpenseType.expenses,
                                          Expenses.expense_description, Expenses.expense_date,
                                          Expenses.expense_amount, Expenses.apply_date)
                         .join(ExpenseType, ExpenseType.id == Expenses.expense_type_id)
                         .filter(Expenses.travel_form_id == travel_form_id)
                         .all())
    bills_form_data = (db.session.query(Bills.expenses_id,
                                        Bills.id, Bills.bills_url,
                                        Bills.bill_type, Bills.bill_name)
                       .join(Expenses, Expenses.id == Bills.expenses_id)
                       .filter(Expenses.travel_form_id == travel_form_id)
                       .all())
    return {'travel_form_data': travel_form_data,
            'expense_form_data': expense_form_data,
            'bills_form_data': bills_form_data}


def status_update_travel_form(travel_form_status, expense_form_status, travel_form_id):
    travel_form_data = db.session.query(TravelForm).filter_by(id=travel_form_id).first()
    travel_form_data.travel_status = travel_form_status
    expense_form_data = (db.session.query(Expenses)
                         .filter_by(travel_form_id=travel_form_data.id)
                         .all())
    for expense in expense_form_data:
        expense.expense_status = expense_form_status
    db.session.commit()
    return "success"


def get_admin_view_travel_form(travel_form_id):
    travel_form_data = (db.session.query(Purpose_Of_Visit.purposes, TravelForm.apply_date,
                                         TravelForm.colleague_details, TravelForm.number_of_people,
                                         TravelForm.travel_date, TravelForm.description, Projects.project_name,
                                         Managers.manager_name)
                        .join(Purpose_Of_Visit, Purpose_Of_Visit.id == TravelForm.purpose_of_visit_id).
                        join(Projects, Projects.id == TravelForm.project_id)
                        .join(Managers, Managers.id == TravelForm.manager_id)
                        .filter(TravelForm.id == travel_form_id)
                        .all())
    return {'travel_form_data': travel_form_data}
