from sqlalchemy import inspect
from app.db.session import engine

inspector = inspect(engine)

print("\nUSERS TABLE COLUMNS\n")

for col in inspector.get_columns("users"):
    print(col["name"])