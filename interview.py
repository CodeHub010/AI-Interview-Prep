import json


def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_answer(answer, keywords):
    answer = answer.lower()

    matched_keywords = []

    for keyword in keywords:
        if keyword.lower() in answer:
            matched_keywords.append(keyword)

    if len(matched_keywords) == 0:
        score = 0
    else:
        score = (len(matched_keywords) / len(keywords)) * 100

    return round(score, 2), matched_keywords


def get_feedback(score):
    if score >= 80:
        return "Excellent answer! You covered most of the important points."
    elif score >= 60:
        return "Good answer, but you can add a few more important points."
    elif score >= 40:
        return "Your answer is partially correct. Try explaining it in more detail."
    else:
        return "Your answer needs improvement. Review the topic and try again."