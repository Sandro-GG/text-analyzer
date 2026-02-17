import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

db = sa.create_engine("postgresql://fullsandro:@localhost:5432/text_analyzer")
Session = sessionmaker(bind=db)
Base = declarative_base()

def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()