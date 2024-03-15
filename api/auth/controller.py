from api.user.models import User


def get_data(email):
    user = User.query.filter_by(email=email).first()
    return user
