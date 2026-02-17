import models

def add_entry(session, content):
    count = len(content.split())
    new_entry = models.TextEntry(content=content, word_count = count)
    
    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    
    return new_entry


def get_history(session, limit: int = 10, offset: int = 0):
    return session.query(models.TextEntry).limit(limit).offset(offset).all()


def delete_entry(session, entry_id):
    entry = session.query(models.TextEntry).filter(models.TextEntry.id == entry_id).first()
    if entry == None: return None
    session.delete(entry)
    session.commit()
    
    return {"detail": "Entry deleted"}


def update_entry(session, entry_id, content):
    entry = session.query(models.TextEntry).filter(models.TextEntry.id == entry_id).first()
    if entry == None: return None
    entry.content = content
    entry.word_count = len(content.split())
    
    session.commit()
    session.refresh(entry)
    
    return entry
    