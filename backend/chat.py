import json

import requests

#API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class Question:
    def __init__(self, question: str, answers: [str], correct_response_index: int, id: str = "", room: str = ""):
        self.id = id
        self.room = room
        self.question = question
        self.answers = answers
        self.correct_response_index = correct_response_index
        self.responses = []

    def to_dict(self):
        return {
            "id": self.id,
            "room": self.room,
            "question": self.question,
            "answers": self.answers,
            "correct_response_index": self.correct_response_index,
            "responses": self.responses
        }

    def to_dto_dict(self):
        return {
            "id": self.id,
            "room": self.room,
            "question": self.question,
            "answers": self.answers
        }


def prompt_chat(transcript: [str]) -> Question:

    transcript_string = "\n".join(transcript)
    query_string = ("SYSTEM: Create a simple nad short quiz with a question and four answers (up to 15 words) about the content of the following text: \n\n" +
                    f"TEXT: {transcript_string} \n\n" +
                    "QUESTION formated as json {'question': ..., 'answers': ['...', '...', '...', '...'], 'correct_index': ...}")
    output = query({
        "inputs": query_string,
        "parameters": {
            "max_length": 1000,
            "max_new_tokens": 500,
            "return_full_text": False,
            "num_return_sequences": 3,
        },
        "options": {
            "wait_for_model": True
        }
    })
    print(query_string + "\n---" + output[0]['generated_text'])

    try:
        di = json.JSONDecoder().decode(output[0]['generated_text'])
        return Question(di['question'], di['answers'], di['correct_index'])
    except Exception:
        print("FAILED JSON")
        return None