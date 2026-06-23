from app import app
from database.models import Answer

with app.app_context():

    answers = Answer.query.all()

    print(f"\nTotal Answers: {len(answers)}\n")

    for answer in answers:

        print("Interview ID:", answer.interview_id)
        print("Question:", answer.question)
        print("Answer:", answer.answer)
        print("-" * 50)