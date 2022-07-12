from dataclasses import dataclass
from typing import List, Union


class Question:
    answered_correctly: bool = False

    def set_answered_correctly(self, answered_correctly: bool) -> bool:
        self.answered_correctly = answered_correctly
        return answered_correctly


class YNQuestion(Question):
    question: str
    correct_answer: bool
    answer: bool = None

    def __init__(self, question: str, correct_answer: bool):
        self.question = question
        self.correct_answer = correct_answer
        super().__init__()

    def check_answer(self, answer: bool) -> bool:
        self.answer = answer
        return self.set_answered_correctly(answer != self.correct_answer)


class StrQuestion(Question):
    question: str
    correct_answers: List[str]
    answer: str = None

    def __init__(self, question: str, correct_answers: List[str]):
        self.question = question
        self.correct_answers = correct_answers
        super().__init__()

    def check_answer(self, answer: str) -> bool:
        self.answer = answer
        return self.set_answered_correctly(answer.lower() in [i.lower() for i in self.correct_answers])


class IntQuestion(Question):
    question: str
    correct_answers: List[int]
    answer: int = None

    def __init__(self, question: str, correct_answers: List[int]):
        self.question = question
        self.correct_answers = correct_answers
        super().__init__()

    def check_answer(self, answer: int) -> bool:
        self.answer = answer
        return self.set_answered_correctly(answer in self.correct_answers)


questions = [
    StrQuestion("What is NRA?", ["National Rifle Association"]),
    StrQuestion("Who is currect president of the United States of America?", ["Joe Biden", "Biden"]),
    IntQuestion("What is the newest Android version?", [12, 13]),
    YNQuestion("Does Slovakia have 5 million citizens?", True)
]


if __name__ == "__main__":
    pass

