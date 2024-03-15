from flask import request
from config import db
from datetime import datetime, timezone
from api.user.models import TravelForm, User, TravelFormStatus, Projects, Purpose_Of_Visit


def add_travel_form():
    data = request.get_json()
    user_id = db.session.query(User.id).filter_by(empId=data.get('employeeId')).scalar()
    manager_id = db.session.query(User.manager_id).filter_by(empId=data.get('managerId')).scalar()
    new_form = TravelForm(
        apply_date=datetime.now(timezone.utc),
        colleague_details=data.get('colleague'),
        description=data.get('projectScope'),
        number_of_people=data.get('numberOfPeople'),
        remarks=None,
        travel_date=datetime.strptime(data.get('dateOfTravel'), '%Y-%m-%d'),
        travel_status=TravelFormStatus.FORM_PENDING,
        user_id=user_id,
        manager_id=manager_id,
        project_id=data.get('projectId'),
        purpose_of_visit_id=data.get('purpose'),

    )
    db.session.add(new_form)
    db.session.commit()
    print(new_form)
    return new_form


def get_all_travelForm():
    data = (db.session.query(TravelForm.apply_date, Projects.project_name,
                             TravelForm.travel_status, Purpose_Of_Visit.purposes,
                             TravelForm.travel_date)
            .join(Projects)
            .join(Purpose_Of_Visit)
            .filter(Projects.id == TravelForm.project_id)
            .filter(Purpose_Of_Visit.id == TravelForm.purpose_of_visit_id)
            .all())
    return data

def get_travelFormById(id):
    data = (db.session.query(Purpose_Of_Visit.purposes,TravelForm.apply_date,
                             TravelForm.colleague_details,TravelForm.number_of_people,
                             TravelForm.travel_date,TravelForm.description,
                             Projects.project_name))

def change_admin_travelForm_status(id,status):
    travel_form = TravelForm.query.filter_by(id=id)
    if travel_form:
        return


