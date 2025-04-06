from app.db.session import engine
from app.db import base  # This imports Base and the models when added

def init_db():
    base.Base.metadata.create_all(bind=engine)
