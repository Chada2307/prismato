from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric, Boolean, Table

from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from database import Base
import uuid
import datetime

photo_album_assoc = Table(
    'photo_album',
    Base.metadata,
    Column('photo_id', UUID(as_uuid=True), ForeignKey('photos.id'), primary_key=True),
    Column('album_id', UUID(as_uuid=True), ForeignKey('albums.id'), primary_key=True)
)

class Album(Base):
    __tablename__ = "albums"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    photos = relationship("Photo", secondary=photo_album_assoc, back_populates="albums")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    passwd_hash = Column(String)
    created_at = Column(DateTime, default = datetime.datetime.now)

class Photo(Base):
    __tablename__ = "photos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    file_path = Column(String)
    thumbnail_path = Column(String)
    file_size = Column(Integer)
    captured_at = Column(DateTime, default = datetime.datetime.now)
    camera_model=Column(String)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    exif_raw = Column(JSONB)
    is_deleted = Column(Boolean, default = False, index=True)
    is_favorite = Column(Boolean, default = False, index=True)
    deleted_at = Column(DateTime, nullable = True)

    owner = relationship("User")
    albums = relationship("Album", secondary=photo_album_assoc, back_populates="photos")

