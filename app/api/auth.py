from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from app.core.auth import verify_token

from app.database.database import get_db
from app.models.user import User

from app.schemas.auth import LoginSchema
from app.schemas.auth import TokenResponse

from app.core.security import verify_password
from app.core.auth import create_access_token

security = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginSchema,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        payload.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = verify_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload