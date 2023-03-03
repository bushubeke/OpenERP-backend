from . import *


@useradmin.post('/register', response_model=UserModel)
async def register(user: UserModelPost, session: AsyncSession = Depends(get_session)):
    try:
        new_user = user.dict()
        new_user['password'] = pbkdf2_sha512.using(rounds=25000, salt_size=80).hash(new_user['password'])
        new_user = User(**new_user)
        session.add(new_user)
        await session.commit()
        return new_user
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/register/{uid}', response_model=UserModelUpdate)
async def register_patch(uid: UUID, user: UserModelUpdate, session: AsyncSession = Depends(get_session)):
    try:
        check_user = await session.execute(select(User).where(User.uid == str(uid)))
        check_user = check_user.scalars().unique().first()
        if check_user:
            await session.execute(update(User).where(User.uid == str(uid)).values(**user.dict()))
            await session.commit()
            return user
        return JSONResponse({"Message": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
