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
    return Question("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0)
