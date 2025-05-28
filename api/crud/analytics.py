from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, desc, cast, Date

from api.models import Announcement, Service, UserActivity

def track_visit(
    request: Request, 
    page: str,
    db: Session
):
    client_host = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    activity = UserActivity(
        activity_type="visit",
        page=page,
        ip_address=client_host,
        user_agent=user_agent,
        timestamp=datetime.now(timezone.utc)
    )
    
    db.add(activity)
    db.commit()
    
    return {"status": "success"}

def track_interaction(
    request: Request,
    db: Session,
    activity_type: str = "click",
    announcement_id: Optional[int] = None,
    service_id: Optional[int] = None
):
    client_host = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    activity = UserActivity(
        activity_type=activity_type,
        ip_address=client_host,
        user_agent=user_agent,
        announcement_id=announcement_id,
        service_id=service_id,
        timestamp=datetime.now(timezone.utc)
    )
    
    db.add(activity)
    db.commit()
    
    return {"status": "success"}

def get_top_announcement(
    db: Session,
    days: int = 30,
    limit: int = 10
):
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    top_announcements = (
        db.query(
            UserActivity.announcement_id,
            Announcement.name.label("announcement_name"),
            func.count().label("clicks")
        )
        .join(Announcement, UserActivity.announcement_id == Announcement.id)
        .filter(
            UserActivity.activity_type == "click",
            UserActivity.announcement_id.isnot(None),
            UserActivity.timestamp >= start_date
        )
        .group_by(UserActivity.announcement_id, Announcement.name)
        .order_by(desc("clicks"))
        .limit(limit)
        .all()
    )
    
    return top_announcements

def get_top_service(
    db: Session,
    days: int = 30,
    limit: int = 10
    ):
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    top_services = (
        db.query(
            UserActivity.service_id,
            Service.name.label("service_name"),
            func.count().label("clicks")
        )
        .join(Service, UserActivity.service_id == Service.id)
        .filter(
            UserActivity.activity_type == "click",
            UserActivity.service_id.isnot(None),
            UserActivity.timestamp >= start_date
        )
        .group_by(UserActivity.service_id, Service.name)
        .order_by(desc("clicks"))
        .limit(limit)
        .all()
    )
    return top_services

def get_daily_activity(
    db: Session,
    days: int = 30
):
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    daily_visits = (
        db.query(
            cast(UserActivity.timestamp, Date).label("date"),
            func.count().label("count")
        )
        .filter(
            UserActivity.activity_type == "visit",
            UserActivity.timestamp >= start_date
        )
        .group_by(cast(UserActivity.timestamp, Date))
        .order_by(cast(UserActivity.timestamp, Date))
        .all()
    )
    
    return [{"date": str(day.date), "count": day.count} for day in daily_visits]
    