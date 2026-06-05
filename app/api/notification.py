from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.notification import Notification


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db)
):

    return (
        db.query(Notification)
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db)
):

    count = (
        db.query(Notification)
        .filter(
            Notification.is_read == False
        )
        .count()
    )

    return {
        "count": count
    }


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: str,
    db: Session = Depends(get_db)
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()

    return {
        "message": "Notification marked as read"
    }


@router.put("/mark-all-read")
def mark_all_read(
    db: Session = Depends(get_db)
):

    notifications = (
        db.query(Notification)
        .filter(
            Notification.is_read == False
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return {
        "message": "All notifications marked as read"
    }