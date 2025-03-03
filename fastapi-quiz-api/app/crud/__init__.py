# app/crud/__init__.py

from .base import CRUDBase
from .quiz import CRUDQuiz
from .user import CRUDUser

crud = {
    "quiz": CRUDQuiz,
    "user": CRUDUser,
}