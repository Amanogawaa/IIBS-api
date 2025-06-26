from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, desc, cast, Date, and_

from api.models import Announcement, Feedback, Service, UserActivity

# def track_visit(
#     request: Request, 
#     page: str,
#     db: Session
# ):
#     client_host = request.client.host if request.client else None
#     user_agent = request.headers.get("user-agent")
    
#     activity = UserActivity(
#         activity_type="visit",
#         page=page,
#         ip_address=client_host,
#         user_agent=user_agent,
#         timestamp=datetime.now(timezone.utc)
#     )
    
#     db.add(activity)
#     db.commit()
    
#     return {"status": "success"}

# def track_interaction(
#     request: Request,
#     db: Session,
#     activity_type: str = "click",
#     announcement_id: Optional[int] = None,
#     service_id: Optional[int] = None
# ):
#     client_host = request.client.host if request.client else None
#     user_agent = request.headers.get("user-agent")
    
#     activity = UserActivity(
#         activity_type=activity_type,
#         ip_address=client_host,
#         user_agent=user_agent,
#         announcement_id=announcement_id,
#         service_id=service_id,
#         timestamp=datetime.now(timezone.utc)
#     )
    
#     db.add(activity)
#     db.commit()
    
#     return {"status": "success"}

# def get_top_announcement(
#     db: Session,
#     days: int = 30,
#     limit: int = 10
# ):
#     start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
#     top_announcements = (
#         db.query(
#             UserActivity.announcement_id,
#             Announcement.name.label("announcement_name"),
#             func.count().label("clicks")
#         )
#         .join(Announcement, UserActivity.announcement_id == Announcement.id)
#         .filter(
#             UserActivity.activity_type == "click",
#             UserActivity.announcement_id.isnot(None),
#             UserActivity.timestamp >= start_date
#         )
#         .group_by(UserActivity.announcement_id, Announcement.name)
#         .order_by(desc("clicks"))
#         .limit(limit)
#         .all()
#     )
    
#     return top_announcements

# def get_top_service(
#     db: Session,
#     days: int = 30,
#     limit: int = 10
#     ):
#     start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
#     top_services = (
#         db.query(
#             UserActivity.service_id,
#             Service.name.label("service_name"),
#             func.count().label("clicks")
#         )
#         .join(Service, UserActivity.service_id == Service.id)
#         .filter(
#             UserActivity.activity_type == "click",
#             UserActivity.service_id.isnot(None),
#             UserActivity.timestamp >= start_date
#         )
#         .group_by(UserActivity.service_id, Service.name)
#         .order_by(desc("clicks"))
#         .limit(limit)
#         .all()
#     )
#     return top_services

# def get_daily_activity(
#     db: Session,
#     days: int = 30
# ):
#     start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
#     daily_visits = (
#         db.query(
#             cast(UserActivity.timestamp, Date).label("date"),
#             func.count().label("count")
#         )
#         .filter(
#             UserActivity.activity_type == "visit",
#             UserActivity.timestamp >= start_date
#         )
#         .group_by(cast(UserActivity.timestamp, Date))
#         .order_by(cast(UserActivity.timestamp, Date))
#         .all()
#     )
    
#     return [{"date": str(day.date), "count": day.count} for day in daily_visits]
    

def track_visit(
    db: Session,
    request: Request,
    page: str
):
    """Track user page visits"""
    client_host = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Check if this is a unique visit (same IP hasn't visited this page in last 30 minutes)
    thirty_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=30)
    recent_visit = db.query(UserActivity).filter(
        and_(
            UserActivity.activity_type == "visit",
            UserActivity.page == page,
            UserActivity.ip_address == client_host,
            UserActivity.timestamp >= thirty_minutes_ago
        )
    ).first()
    
    # Only track if no recent visit from same IP
    if not recent_visit:
        activity = UserActivity(
            activity_type="visit",
            page=page,
            ip_address=client_host,
            user_agent=user_agent,
            timestamp=datetime.now(timezone.utc)
        )
        db.add(activity)
        db.commit()
    
    return {"status": "success", "tracked": not bool(recent_visit)}

def track_interaction(
    request: Request,
    db: Session,
    activity_type: str = "click",
    announcement_id: Optional[int] = None,
    service_id: Optional[int] = None
):
    """Track user interactions (clicks, views, etc.)"""
    client_host = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
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

def get_top_announcements(
    db: Session,
    days: int = 30,
    limit: int = 10
):
    """Get most clicked announcements"""
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    top_announcements = (
        db.query(
            UserActivity.announcement_id,
            Announcement.name.label("announcement_title"),
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
    
    return [
        {
            "announcement_id": item.announcement_id,
            "title": item.announcement_title,
            "clicks": item.clicks
        }
        for item in top_announcements
    ]

def get_top_services(
    db: Session,
    days: int = 30,
    limit: int = 10
):
    """Get most clicked services"""
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    top_services = (
        db.query(
            UserActivity.service_id,
            Service.name.label("service_title"),
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
    
    return [
        {
            "service_id": item.service_id,
            "title": item.service_title,
            "clicks": item.clicks
        }
        for item in top_services
    ]

def get_daily_activity(
    db: Session,
    days: int = 30
):
    """Get daily activity statistics"""
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

def get_popular_pages(
    db: Session,
    days: int = 30,
    limit: int = 10
):
    """Get most visited pages"""
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    popular_pages = (
        db.query(
            UserActivity.page,
            func.count().label("visits")
        )
        .filter(
            UserActivity.activity_type == "visit",
            UserActivity.page.isnot(None),
            UserActivity.timestamp >= start_date
        )
        .group_by(UserActivity.page)
        .order_by(desc("visits"))
        .limit(limit)
        .all()
    )
    
    return [
        {
            "page": item.page,
            "visits": item.visits
        }
        for item in popular_pages
    ]

def get_activity_summary(
    db: Session,
    days: int = 30
):
    """Get overall activity summary"""
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Total visits
    total_visits = db.query(func.count(UserActivity.id)).filter(
        UserActivity.activity_type == "visit",
        UserActivity.timestamp >= start_date
    ).scalar()
    
    # Total clicks
    total_clicks = db.query(func.count(UserActivity.id)).filter(
        UserActivity.activity_type == "click",
        UserActivity.timestamp >= start_date
    ).scalar()
    
    # Unique visitors (based on IP)
    unique_visitors = db.query(func.count(func.distinct(UserActivity.ip_address))).filter(
        UserActivity.activity_type == "visit",
        UserActivity.timestamp >= start_date
    ).scalar()
    
    return {
        "total_visits": total_visits,
        "total_clicks": total_clicks,
        "unique_visitors": unique_visitors,
        "period_days": days
    }

def get_service_ratings(db: Session):
    """Get aggregated ratings for services including service names"""
    service_ratings = (
        db.query(
            Feedback.service_id,
            Service.name.label("service_name"),
            func.avg(Feedback.rating).label("average_rating"),
            func.count(Feedback.id).label("rating_count")
        )
        .join(Service, Feedback.service_id == Service.id)
        .filter(Feedback.service_id.isnot(None))
        .group_by(Feedback.service_id, Service.name)
        .all()
    )
    
    return [
        {
            "service_id": item.service_id,
            "service_name": item.service_name,
            "average_rating": float(item.average_rating) if item.average_rating else 0.0,
            "rating_count": item.rating_count
        }
        for item in service_ratings
    ]

def get_announcement_ratings(db: Session):
    """Get aggregated ratings for announcements including announcement names"""
    announcement_ratings = (
        db.query(
            Feedback.announcement_id,
            Announcement.name.label("announcement_name"),
            func.avg(Feedback.rating).label("average_rating"),
            func.count(Feedback.id).label("rating_count")
        )
        .join(Announcement, Feedback.announcement_id == Announcement.id)
        .filter(Feedback.announcement_id.isnot(None))
        .group_by(Feedback.announcement_id, Announcement.name)
        .all()
    )
    
    return [
        {
            "announcement_id": item.announcement_id,
            "announcement_name": item.announcement_name,
            "average_rating": float(item.average_rating) if item.average_rating else 0.0,
            "rating_count": item.rating_count
        }
        for item in announcement_ratings
    ]


def get_overall_rating(db: Session):
    """Get aggregated overall rating for feedback with no service_id or announcement_id"""
    overall_rating = (
        db.query(
            func.avg(Feedback.rating).label("average_rating"),
            func.count(Feedback.id).label("rating_count")
        )
        .filter(
            Feedback.service_id.is_(None),
            Feedback.announcement_id.is_(None)
        )
        .first()
    )
    
    return {
        "average_rating": float(overall_rating.average_rating) if overall_rating.average_rating else 0.0,
        "rating_count": overall_rating.rating_count
    }