# check_fk.py

from sqlalchemy import create_engine
from sqlalchemy import inspect

engine = create_engine(
    "postgresql+psycopg2://postgres:MyNewPassword123!@localhost:5432/makermint"
)

inspector = inspect(engine)

for fk in inspector.get_foreign_keys("creators"):
    print(fk)