from flask import Blueprint
from api.Purposes.services import get_purposeOfVisit,add_purposeOfVisit,edit_purposeOfVisit,delete_purposeOfVisit

purposeOfVisit_api = Blueprint('purposeOfVisit_api',__name__,url_prefix='/purpose')

@purposeOfVisit_api.route('/getAllPurposes',methods=["GET"])
def getPurposes():
    return get_purposeOfVisit()

@purposeOfVisit_api.route('/addPurposes',methods=["POST"])
def addPurposes():
    return add_purposeOfVisit()

@purposeOfVisit_api.route('/editPurposes/<int:id>',methods=["POST"])
def editPurposes(id):
    return edit_purposeOfVisit(id)

@purposeOfVisit_api.route('/deletePurposes/<int:id>',methods=["DELETE"])
def deletePurposes(id):
    return delete_purposeOfVisit(id)