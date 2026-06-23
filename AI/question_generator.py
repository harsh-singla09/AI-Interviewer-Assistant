from ollama import chat


def generate_questions(resume_info):

    prompt = f"""
You are a professional interviewer.

Candidate Skills:
{', '.join(resume_info['skills'])}

Projects:
{', '.join(resume_info['projects'])}

Generate exactly 10 interview questions.

Rules:
- Output only questions.
- Do not write introductions.
- Do not write explanations.
- One question per line.
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