from database import db, Session, Base
import models
from pydantic import BaseModel
import fastapi

Base.metadata.create_all(bind=db)
app = fastapi.FastAPI()

class TextRequest(BaseModel):
    text: str
    
@app.post("/analyze")
def analyze_text(request: TextRequest):
    with Session() as session:
        user_text = request.text
        count = len(user_text.split())
        new_entry = models.TextEntry(content=user_text, word_count = count)
        
        session.add(new_entry)
        session.commit()
        session.refresh(new_entry)
        
        return new_entry