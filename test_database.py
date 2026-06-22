from app import app
from database.db import db
from database.models import User


with app.app_context():

    user = User(
        username="Harsh",
        email="harsh@test.com",
        password="12345"
    )


    db.session.add(user)

    db.session.commit()


print("User Added")