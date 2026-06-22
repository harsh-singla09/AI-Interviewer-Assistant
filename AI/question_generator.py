from ollama import chat


def generate_questions(resume_info):

    prompt = f"""
You are a senior software engineer conducting an internship interview.

Candidate Skills:
{', '.join(resume_info['skills'])}

Projects:
{', '.join(resume_info['projects'])}

Generate:

- 5 Python questions
- 3 Flask questions
- 3 SQL questions
- 4 project-specific questions
- 2 HR questions

Do not provide answers.

Only provide questions.
""" 

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]