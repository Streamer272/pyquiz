from dataclasses import dataclass


@dataclass
class Question:
    question: str
    answer: str = None


questions = [Question("What is your name?"), Question("What is your age?"), Question("What is your gender?")]


if __name__ == "__main__":
    pass

