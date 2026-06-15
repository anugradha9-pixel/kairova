from app.db.session import SessionLocal


class UnitOfWork:
    """
    Ensures transaction safety across repositories.
    """

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()