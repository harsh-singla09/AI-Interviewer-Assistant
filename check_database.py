from app import app
from database.models import User


with app.app_context():

    users = User.query.all()

    for user in users:
        print(
            user.username,
            user.email
        )