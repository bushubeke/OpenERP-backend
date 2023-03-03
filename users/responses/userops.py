from . import *
from opencelery.core import send_celery_email


@useradmin.get('/mail')
async def send_mail() -> Any:
    send_celery_email.apply_async(("Beimnet B Degefu", ["beimdegefu@gmail.com", "bushubekele@gmail.com"]),
                                  queue='opencelery')
    return JSONResponse({'Message': "Working fine"}, status_code=status.HTTP_200_OK)


@useradmin.get('/user/{user_id}', response_model=UserModelAll, dependencies=[Depends(get_current_user)])
async def get_one_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id).options(joinedload(User.roles)))
        user = user.unique().scalars().first()
        if user:
            logger.info('User  have been fetched successfully')
            return user
        else:
            logger.info('No User Found  ')
            return JSONResponse({"Message": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/user', response_model=Page[UserModelAll], dependencies=[Depends(get_current_user)])
async def get_some_user(session: AsyncSession = Depends(get_session)):
    try:
        users = await session.execute(select(User).options(joinedload(User.roles)).order_by(User.id))
        users = users.unique().scalars().all()
        return paginate(users)
    except Exception as e:
        JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
