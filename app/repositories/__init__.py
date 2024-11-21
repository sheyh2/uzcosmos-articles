from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db


class Repository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
