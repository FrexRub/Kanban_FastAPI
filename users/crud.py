import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Result

from users.models import User
from core.exceptions import ExceptDB
from core.config import format_log


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(format_log)
logger.addHandler(console_handler)


async def get_user_from_db(
    name: str,
    session: AsyncSession,
):
    logger.info("Start get_user_from_db")
    stmt = select(User).where(User.email == name)
    result: Result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user:
        logger.info(f"User {name} has been found")
    else:
        logger.info(f"User {name} not found")
    return user


async def add_user_to_db(
    user: User,
    session: AsyncSession,
):
    logger.info("Start add new user")
    try:
        session.add(user)
        await session.commit()
    except SQLAlchemyError as exc:
        logger.exception(exc)
        raise ExceptDB(f"Error in DB")
    else:
        logger.info("User add in db")
        return user.id


    # except InvalidTokenError as exc:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail=f"invalid token error exception: {exc}"
    #     )