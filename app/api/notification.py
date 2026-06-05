from fastapi import APIRouter
from fastapi import Depends

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