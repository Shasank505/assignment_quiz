from pydantic import BaseModel
from typing import List, Optional

class QuizBase(BaseModel):
    title: str
    description: str

class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    title: Optional[str] = None
    description: Optional[str] = None

class Quiz(QuizBase):
    id: int
    questions: List['Question'] = []

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    question_text: str

class QuestionCreate(QuestionBase):
    quiz_id: int

class QuestionUpdate(QuestionBase):
    question_text: Optional[str] = None

class Question(QuestionBase):
    id: int
    quiz_id: int

    class Config:
        orm_mode = True