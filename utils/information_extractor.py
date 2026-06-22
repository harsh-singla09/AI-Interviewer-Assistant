import re


def extract_resume_info(text):

    info = {
        "name": "",
        "skills": [],
        "projects": [],
        "education": []
    }

    lines = text.split("\n")

    # Name (usually first non-empty line)
    for line in lines:
        if line.strip():
            info["name"] = line.strip()
            break

    skills_keywords = [
        "python",
        "flask",
        "sql",
        "mysql",
        "machine learning",
        "deep learning",
        "html",
        "css",
        "javascript",
        "git",
        "github",
        "pandas",
        "numpy",
        "scikit-learn"
    ]

    text_lower = text.lower()

    for skill in skills_keywords:

        if skill in text_lower:
            info["skills"].append(skill.title())

    for line in lines:

        line = line.strip()

        if "project" in line.lower():
            continue

        if len(line) > 5:

            if (
                "predictor" in line.lower()
                or
                "checker" in line.lower()
                or
                "assistant" in line.lower()
            ):
                info["projects"].append(line)

    education_keywords = [
        "b.tech",
        "btech",
        "computer science",
        "engineering",
        "college",
        "university"
    ]

    for line in lines:

        for keyword in education_keywords:

            if keyword in line.lower():

                info["education"].append(
                    line.strip()
                )

    return info