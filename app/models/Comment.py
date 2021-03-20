from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# making a new table for comments

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(100), nullable=False)
    user_id = Column(String(100), ForeignKey('users.id'))
    post_id = Column(String(100), ForeignKey('posts.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User')
    comments = relationship('Comment', cascade='all,delete')
    # line 18 is so that if a post gets deleted, all the comments get deleted too.