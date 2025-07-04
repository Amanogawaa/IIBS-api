from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship
from api.database import Base
from datetime import datetime, timezone


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=True)  
    comment = Column(Text, nullable=True)
    user_name = Column(String(255), nullable=True)
    announcement_id = Column(
        Integer, ForeignKey("announcements.id", ondelete="CASCADE"), nullable=True
    )
    service_id = Column(
        Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    announcement = relationship("Announcement", back_populates="feedback")
    service = relationship("Service", back_populates="feedback")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    announcement_id = Column(
        Integer, ForeignKey("announcements.id", ondelete="CASCADE"), nullable=True
    )
    service_id = Column(
        Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    announcement = relationship("Announcement", back_populates="comments")
    service = relationship("Service", back_populates="comments")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    announcements = relationship(
        "Announcement", back_populates="user", cascade="all, delete"
    )
    services = relationship(
        "Service", back_populates="user", cascade="all, delete"
    )
    business_info = relationship(
        "BusinessInfo", back_populates="user", cascade="all, delete"
    )

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    platform = Column(String(255), nullable=False, default='physical')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    
    user = relationship("User", back_populates="announcements")
    feedback = relationship(
        "Feedback", back_populates="service", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="service", cascade="all, delete-orphan")


class Faq(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False, unique=True)
    answer = Column(Text, nullable=False)
    service_id = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    service = relationship("Service", back_populates="faqs")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    status = Column(String(255), nullable=False, default="active")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    services = relationship(
        "Service", back_populates="category", cascade="all, delete"
    )

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=True)
    status = Column(String(255), nullable=False, default="active")
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    category = relationship("Category", back_populates="services")
    user = relationship("User", back_populates="services")
    faqs = relationship("Faq", back_populates="service", cascade="all, delete")
    feedback = relationship(
        "Feedback", back_populates="service", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="service", cascade="all, delete-orphan")
    

class BusinessInfo(Base):
    __tablename__ = "business_info"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Core Public Information
    name = Column(String(255), nullable=False, unique=True)
    logo = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    tagline = Column(String(255), nullable=True)
    
    # Contact & Location
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Business Details
    industry = Column(String(100), nullable=True)
    business_type = Column(String(50), nullable=True) 
    founded_date = Column(DateTime, nullable=True)
    employee_count_range = Column(String(50), nullable=True)
    
    # Operating Information
    business_hours = Column(Text, nullable=True)  
    timezone = Column(String(50), nullable=True)
    
    # Social & Online Presence
    social_media = Column(Text, nullable=True) 
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="business_info")


Announcement.comments = relationship("Comment", back_populates="announcement", cascade="all, delete-orphan")

Service.comments = relationship("Comment", back_populates="service", cascade="all, delete-orphan")

Announcement.feedback = relationship("Feedback", back_populates="announcement", cascade="all, delete-orphan")

Service.feedback = relationship("Feedback", back_populates="service", cascade="all, delete-orphan")

class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String(50), nullable=False) 
    page = Column(String(255), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id", ondelete="SET NULL"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="SET NULL"), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    announcement = relationship("Announcement")
    service = relationship("Service")
