from sqlalchemy.orm import Session
from app.db.models.quiz import Quiz, Question
from app.schemas.quiz import QuizCreate, QuizUpdate, QuestionCreate, QuestionUpdate

class CRUDQuiz:
    def create_quiz(self, db: Session, quiz: QuizCreate):
        db_quiz = Quiz(title=quiz.title, description=quiz.description)
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    def update_quiz(self, db: Session, db_quiz: Quiz, quiz_update: QuizUpdate):
        if quiz_update.title is not None:
            db_quiz.title = quiz_update.title
        if quiz_update.description is not None:
            db_quiz.description = quiz_update.description
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    def delete_quiz(self, db: Session, quiz_id: int):
        db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if db_quiz:
            db.delete(db_quiz)
            db.commit()
        return db_quiz

    def create_question(self, db: Session, question: QuestionCreate):
        db_question = Question(question_text=question.question_text, quiz_id=question.quiz_id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    def update_question(self, db: Session, db_question: Question, question_update: QuestionUpdate):
        if question_update.question_text is not None:
            db_question.question_text = question_update.question_text
        db.commit()
        db.refresh(db_question)
        return db_question

    def delete_question(self, db: Session, question_id: int):
        db_question = db.query(Question).filter(Question.id == question_id).first()
        if db_question:
            db.delete(db_question)
            db.commit()
        return db_question

crud_quiz = CRUDQuiz()