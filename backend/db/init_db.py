from backend.db.models import Base
from backend.db.session import engine

# IMPORT ALL MODELS HERE
from backend.auth.models import User
from backend.creator.models import Creator


def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")