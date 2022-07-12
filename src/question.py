from dataclasses import dataclass
from typing import List, Union
from enum import Enum


class QuestionType(Enum):
    yes_no = 1
    input_str = 2
    input_int = 3
    dropdown = 4


@dataclass
class Question:
    question_type: QuestionType
    question: str
    correct_answers: List[str]
    answer: str = None
    answered_correctly: bool = False


questions = [
    Question(QuestionType.input_str, "What is NRA?", ["National Rifle Association"]),
    Question(QuestionType.input_str, "Who is currect president of the United States of America?", ["Joe Biden"]),
    Question(QuestionType.input_str, "What is Germanies most known band?", ["Rammstein"]),
    Question(QuestionType.yes_no, "Does Slovakia have 5 million citizens?", ["Yes"])
]


if __name__ == "__main__":
    pass

