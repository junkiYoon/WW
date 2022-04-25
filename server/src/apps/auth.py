from fastapi import APIRouter, status, Depends

from src import Settings, get_settings

from src.core.schemas.auth import Sign_up, Sign_in

from src.core.models import session_scope

from src.utils.auth import is_email, is_nickname, create_user, login


router = APIRouter()


@router.get("/email", status_code=status.HTTP_200_OK)
async def email_validation(email: str, settings: Settings = Depends(get_settings())):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = await is_email(session=session, email=email)

        return response


@router.get("/nickname", status_code=status.HTTP_200_OK)
async def nickname_validation(nickname: str, settings: Settings = Depends(get_settings())):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = await is_nickname(session=session, nickname=nickname)

        return response


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(body: Sign_up, settings: Settings = Depends(get_settings())):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = create_user(session=session, email=body.email, password=body.password, nickname=body.nickname)

        return response


@router.post("/signin", status_code=status.HTTP_200_OK)
def sign_in(body: Sign_in, settings: Settings = Depends(get_settings())):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = login(session=session, email=body.email, password=body.password)

        return response
