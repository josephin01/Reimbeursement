from config import db
from base.base import Base
from sqlalchemy import Enum, DATE
import enum


class Roles(enum.Enum):
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    EMPLOYEE = 'EMPLOYEE'


class TravelFormStatus(enum.Enum):
    FORM_PENDING = 'FORM_PENDING'
    FORM_APPROVED = 'FORM_APPROVED'
    FORM_REJECTED = 'FORM_REJECTED'


class ExpensesStatus(enum.Enum):
    PENDING = 'PENDING'
    MANAGER_APPROVED = 'MANAGER_APPROVED'
    MANAGER_REJECTED = 'MANAGER_REJECTED'
    ADMIN_APPROVED = 'ADMIN_APPROVED'
    ADMIN_REJECTED = 'ADMIN_REJECTED'


class NotificationStatus(enum.Enum):
    SENT = 'SENT'
    SEEN = 'SEEN'


class ExpenseTypeStatus(enum.Enum):
    TRAVEL_FORM = 'TRAVEL_FORM'
    EXPENSE_CLAIM = 'EXPENSE_CLAIM'


class NotificationFormType(enum.Enum):
    TRAVEL_FORM = 'TRAVEL_FORM'
    EXPENSE_CLAIM = 'EXPENSE_CLAIM'
    EXPENSE = 'EXPENSE'


class BillStatus(enum.Enum):
    NO_BILL = 'NO_BILL'
    BILL_ADDED = 'BILL_ADDED'
    BILL_APPROVED = 'BILL_APPROVED'
    BILL_REJECTED = 'BILL_REJECTED'


class User(Base):
    __tablename__ = 'User'

    email = db.Column(db.String(250))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    dob = db.Column(db.String(10))
    empId = db.Column(db.Integer, unique=True)
    role = db.Column(Enum(Roles))
    password = db.Column(db.String(100))
    manager_id = db.Column(db.Integer, db.ForeignKey('Managers.id', ondelete='CASCADE'))
    is_manager = db.Column(db.Boolean)
    profile = db.Column(db.String(255))


class Managers(Base):
    __tablename__ = 'Managers'

    manager_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))


class Projects(Base):
    __tablename__ = 'Projects'

    project_name = db.Column(db.String(150))
    manager_id = db.Column(db.Integer, db.ForeignKey('Managers.id', ondelete='CASCADE'))


class ExpenseType(Base):
    __tablename__ = "ExpenseType"

    expenses = db.Column(db.String(150))
    form_type = db.Column(Enum(ExpenseTypeStatus))


class Purpose_Of_Visit(Base):
    __tablename__ = "Purpose_Of_Visit"

    purposes = db.Column(db.String(150))


class Batches(Base):
    __tablename__ = "Batches"

    # date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    from_date = db.Column(DATE)
    to_date = db.Column(DATE)
    reference = db.Column(db.String(150))
    travel_form_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))


class Notification(Base):
    __tablename__ = "Notification"

    admin_notification_status = db.Column(Enum(NotificationStatus))
    # date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    emp_id = db.Column(db.Integer)
    employee_notification_status = db.Column(Enum(NotificationStatus))
    manager_id = db.Column(db.Integer)
    manager_notification_status = db.Column(Enum(NotificationStatus))
    notification_form_type = db.Column(Enum(NotificationFormType))


class Expenses(Base):
    __tablename__ = "Expenses"

    apply_date = db.Column(DATE)
    expense_amount = db.Column(db.Double)
    expense_date = db.Column(DATE)
    expense_description = db.Column(db.String(255))
    expense_status = db.Column(Enum(ExpensesStatus))
    expense_type_id = db.Column(db.Integer, db.ForeignKey('ExpenseType.id', ondelete='CASCADE'))
    notification_id = db.Column(db.Integer, db.ForeignKey('Notification.id', ondelete='CASCADE'))
    travel_form_id = db.Column(db.Integer, db.ForeignKey('TravelForm.id', ondelete='CASCADE'))


class TravelForm(Base):
    __tablename__ = "TravelForm"

    apply_date = db.Column(DATE)
    bill_status = db.Column(Enum(BillStatus))
    colleague_details = db.Column(db.String)
    description = db.Column(db.String(255))
    number_of_people = db.Column(db.Integer)
    remarks = db.Column(db.String(255))
    travel_date = db.Column(DATE)
    travel_status = db.Column(Enum(TravelFormStatus))
    batch_id = db.Column(db.Integer, db.ForeignKey('Batches.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    manager_id = db.Column(db.Integer, db.ForeignKey('Managers.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id', ondelete='CASCADE'))
    purpose_of_visit_id = db.Column(db.Integer, db.ForeignKey('Purpose_Of_Visit.id', ondelete='CASCADE'))


class Bills(Base):
    __tablename__ = "Bills"

    bill_name = db.Column(db.String(150))
    bill_type = db.Column(db.String(150))
    bills_url = db.Column(db.String(255))
    expense_claims_id = db.Column(db.Integer, db.ForeignKey('Expense_Claim.id', ondelete='CASCADE'))
    expenses_id = db.Column(db.Integer, db.ForeignKey('Expenses.id', ondelete='CASCADE'))


class Expense_Claim(Base):
    __tablename__ = "Expense_Claim"

    apply_date = db.Column(DATE)
    colleague_details = db.Column(db.String(255))
    expense_amount = db.Column(db.Double)
    expense_date = db.Column(DATE)
    expense_description = db.Column(db.String(255))
    expense_status = db.Column(
        Enum(ExpensesStatus))
    remarks = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    expense_type_id = db.Column(db.Integer, db.ForeignKey('ExpenseType.id', ondelete='CASCADE'))
    manager_id = db.Column(db.Integer, db.ForeignKey('Managers.id', ondelete='CASCADE'))
    notification_id = db.Column(db.Integer, db.ForeignKey('Notification.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id', ondelete='CASCADE'))
