from app.db.session import SessionLocal
from app.auth.repository import AuthRepository

db = SessionLocal()

repo = AuthRepository(db)

user = repo.get_user_by_email(
    "test@example.com"
)

print(user)
print(user.email)
print(user.hashed_password)

db.close()