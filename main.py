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
    if len(request.text) > 10000: raise fastapi.HTTPException(413, "Payload Too Large")
    with Session() as session:
        user_text = request.text
        count = len(user_text.split())
        new_entry = models.TextEntry(content=user_text, word_count = count)
        
        session.add(new_entry)
        session.commit()
        session.refresh(new_entry)
        
        return new_entry
    
@app.get("/history")
def get_history(limit: int = 10, offset: int = 0):
    with Session() as session:
        entries = session.query(models.TextEntry).limit(limit).offset(offset).all()
        return entries
    
@app.delete("/id/{entry_id}")
def delete_entry(entry_id: int):
    with Session() as session:
        entry = session.query(models.TextEntry).filter(models.TextEntry.id == entry_id).first()
        if entry == None: raise fastapi.HTTPException(404, "Entry Not Found")
        
        session.delete(entry)
        session.commit()
        
        return {"detail": "Entry deleted"}