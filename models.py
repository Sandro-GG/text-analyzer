from database import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class TextEntry(Base):
    __tablename__ = "entries"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(sa.Text)
    word_count: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now)
    