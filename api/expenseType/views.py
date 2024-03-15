from flask import Blueprint
from api.expenseType.services import get_expenseType_data,add_expenseType_data,edit_expenseType_data,delete_expenseType_data

expenseType_api = Blueprint('expenseType_api',__name__,url_prefix='/expenseType')

@expenseType_api.route('/getExpenseType',methods=["GET"])
def getExpenseType():
    return get_expenseType_data()

@expenseType_api.route('/addExpenseType',methods=["POST"])
def addExpenseType():
    return  add_expenseType_data()

@expenseType_api.route('/editExpenseType/<int:id>',methods=["POST"])
def editExpenseType(id):
    return edit_expenseType_data(id)

@expenseType_api.route('/deleteExpenseType/<int:id>',methods=["DELETE"])
def deleteExpenseType(id):
    return delete_expenseType_data(id)