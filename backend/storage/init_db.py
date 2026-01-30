from backend.storage.database import engine, Base
from backend.storage.models import Article  

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
