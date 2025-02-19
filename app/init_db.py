from .database import Base, engine
from .models.user import User
from .models.member import Member

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()