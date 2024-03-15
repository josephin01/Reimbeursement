from flask import Blueprint, request
from api.travelForm.services import add_travelForm, get_travel_forms, get_travelForm_byId

travelForm_api = Blueprint('travelForm_api', __name__, url_prefix='/travelForm')


@travelForm_api.route('/getTravelForm', methods=["GET"])
def get_all_travelForm():
    return get_travel_forms()


@travelForm_api.route('/addTravelForm', methods=["POST"])
def addTravelForm():
    return add_travelForm()


@travelForm_api.route('/getTravelFormById/<int:id>', methods=["GET"])
def getTravelFormById(id):
    return get_travelForm_byId(id)


@travelForm_api.route('/travelFormStatus/<int:id>', methods=["PATCH"])
def changeTravelFormStatus(id):
    data = request.get_json()
    status = data.get('status')
    return change_travelForm_status(status)
