from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from api.database import Base
from datetime import datetime

service_requirement_association = Table(
    "service_requirement_association",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id", ondelete="CASCADE")),
    Column("requirement_id", Integer, ForeignKey("requirements.id", ondelete="CASCADE"))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    announcements = relationship('Announcement', back_populates='user', cascade="all, delete")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    requirements = relationship("Requirement", secondary=service_requirement_association, back_populates="services")

class RequirementCategory(Base):
    __tablename__ = "requirement_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    requirements = relationship("Requirement", back_populates="category", cascade="all, delete")

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("requirement_categories.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    category = relationship("RequirementCategory", back_populates="requirements")
    services = relationship("Service", secondary=service_requirement_association, back_populates="requirements")

class Announcement(Base):
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship('User', back_populates='announcements')
