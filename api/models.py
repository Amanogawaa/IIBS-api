from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship
from api.database import Base
from datetime import datetime, timezone

service_location = Table(
    "service_location",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id", ondelete="CASCADE"), primary_key=True),
    Column("location_id", Integer, ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
)

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

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_urgent = Column(Boolean, default=False)
    platform = Column(String(255), nullable=False, default='web')
    links = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="announcements")

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

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    file = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    category = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    services = relationship(
        "Service", back_populates="download", cascade="all, delete"
    )

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
    download_id = Column(
        Integer, ForeignKey("downloads.id", ondelete="SET NULL"), nullable=True
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
    download = relationship("Download", back_populates="services")
    user = relationship("User", back_populates="services")
    faqs = relationship("Faq", back_populates="service", cascade="all, delete")
    attributes = relationship(
        "ServiceAttribute", back_populates="service", cascade="all, delete"
    )
    locations = relationship(
        "Location", secondary=service_location, back_populates="services"
    )

class ServiceAttribute(Base):
    __tablename__ = "service_attributes"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(
        Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attribute_name = Column(String(255), nullable=False)
    attribute_value = Column(Text, nullable=False)
    attribute_type = Column(String(255), nullable=False)

    service = relationship("Service", back_populates="attributes")

class Location(Base):
    __tablename__ = "locations"

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
        "Service", secondary=service_location, back_populates="locations"
    )

class BusinessInfo(Base):
    __tablename__ = "business_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    logo = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    attributes = relationship(
        "BusinessInfoAttribute", back_populates="business_info", cascade="all, delete"
    )

class BusinessInfoAttribute(Base):
    __tablename__ = "business_info_attributes"

    id = Column(Integer, primary_key=True, index=True)
    business_info_id = Column(
        Integer, ForeignKey("business_info.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attribute_name = Column(String(255), nullable=False)
    attribute_value = Column(Text, nullable=False)
    attribute_type = Column(String(255), nullable=False)

    business_info = relationship("BusinessInfo", back_populates="attributes")