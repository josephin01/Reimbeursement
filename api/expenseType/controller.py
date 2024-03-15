from api.user.models import ExpenseType
from flask import request
from config import db
def get_expenseQueryData():
    data = ExpenseType.query.filter_by(deleted_at=None).all()
    data_list=[]
    for i in data:
        data_list.append({
            'id':i.id,
            'form_type':i.form_type,
            'expenses':i.expenses
        })
    return {'data':data_list}

def add_expenseQueryData():
    data = request.get_json()
    form_type= data.get('form_type')
    expenses = data.get('expenses')

    existing_expenses = ExpenseType.query.filter_by(expenses=expenses,form_type=form_type).first()
    if existing_expenses:
        if existing_expenses.deleted_at is not None:
            existing_expenses.deleted_at = None
            return existing_expenses
        else:
            return "Expense Already Exists"

    new_add_expenseType = ExpenseType(form_type=form_type,expenses=expenses)
    return new_add_expenseType

def edit_expenseQueryData(id):
    data = request.get_json()
    form_type = data.get('form_type')
    expenses = data.get('expenses')
    data_update = ExpenseType.query.filter_by(id=id).first()
    existing_record = ExpenseType.query.filter_by(form_type=form_type, expenses=expenses).first()
    if not data_update:
        return {"error":"Data Not Found"}
    if existing_record:
        return {"error": "Expense Type already exists"}
    if form_type is not None:
        data_update.form_type = form_type
    if expenses is not None:
        data_update.expenses = expenses

    db.session.commit()

    if form_type is not None or expenses is not None:
        return {"msg": "Expense Type Updated Successfully"}
    else:
        return {"msg": "No changes detected"}


def delete_expenseQueryData(id):
    data = ExpenseType.query.filter_by(id=id).first()
    if not data:
        return {"error":"Data not found"}
    elif data.deleted_at:
        return {"error": "Data already deleted"}
    else:
        data.delete()
        return {"msg": "Expense Type deleted successfully"}
