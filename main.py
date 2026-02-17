from database import db, Session, Base, get_db
from pydantic import BaseModel
import fastapi
import service

Base.metadata.create_all(bind=db)
app = fastapi.FastAPI()

class TextRequest(BaseModel):
    text: str
    
    
@app.post("/analyze")
def analyze_text(request: TextRequest, db: Session = fastapi.Depends(get_db)):
    if len(request.text) > 10000: raise fastapi.HTTPException(413, "Payload Too Large")
    return service.add_entry(db, request.text)
    
    
@app.get("/history")
def get_history(limit: int = 10, offset: int = 0, db: Session = fastapi.Depends(get_db)):
    return service.get_history(db, limit, offset)
    
    
@app.delete("/id/{entry_id}")
def delete_entry(entry_id: int, db: Session = fastapi.Depends(get_db)):
    message = service.delete_entry(db, entry_id)
    if message is None: 
        raise fastapi.HTTPException(404, "Entry Not Found")
    return message
            

@app.put("/id/{entry_id}")
def update_entry(entry_id: int, request: TextRequest, db: Session = fastapi.Depends(get_db)):
    message = service.update_entry(db, entry_id, request.text)
    if message is None:
        raise fastapi.HTTPException(404, "Entry Not Found")
    return message