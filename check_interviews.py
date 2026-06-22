from app import app

from database.models import Interview



with app.app_context():


    interviews = Interview.query.all()


    for i in interviews:


        print(
            "Interview ID:",
            i.id
        )

        print(
            "Resume:",
            i.resume
        )