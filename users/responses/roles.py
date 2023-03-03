from . import *


@useradmin.get('/roles', response_model=Page[RoleModelMatrix], dependencies=[Depends(get_current_user)])
async def role_get(session: AsyncSession = Depends(get_session)):
    try:
        my_roles = await session.execute(select(Role))
        my_roles = my_roles.unique().scalars().all()
        logger.info('Role  have been fetched successfully')
        return paginate(my_roles)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.post('/roles', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def role_post(role: RoleModel, session: AsyncSession = Depends(get_session)):
    try:
        role = Role(**role.dict())
        session.add(role)
        await session.commit()
        logger.info(f'Role {role} have been created successfully')
        return role
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/roles', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def role_patch(role: RoleModelMatrix, session: AsyncSession = Depends(get_session),
                     ):
    try:
        check_role = await session.execute(select(Role).where(Role.id == role.id))
        check_role = check_role.scalars().unique().first()
        if check_role:
            await session.execute(update(Role).where(Role.id == role.id).values(**role.dict()))
            await session.commit()
            logger.info(f'Role {role} have been updated successfully')
            return role
        return JSONResponse({"Message": "No Such Role"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/roles/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def role_delete(role_id: int, session: AsyncSession = Depends(get_session)):
    try:
        role = await session.execute(select(Role).where(Role.id == role_id))
        role = role.unique().scalars().first()
        if role:
            await session.execute(delete(Role).where(Role.id == role_id))
            await session.commit()
            logger.info(f'Role {role} have been deleted successfully')
            return role
        return JSONResponse({"Message": "Role Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/roles/{uid}', response_model=RoleUserModelAll, dependencies=[Depends(get_current_user)])
async def add_user_role_get(uid: UUID, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.uid == str(uid)).options(selectinload(User.roles)))
        user = user.scalars().unique().first()
        if user:
            return user
        return JSONResponse({"Message": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.post('/roles/{uid}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def add_user_role_post(uid: UUID, role_id: AddRole, session: AsyncSession = Depends(get_session)):
    try:
        check_role = await session.execute(select(Role).where(Role.id == role_id.role_id))
        check_role = check_role.scalars().unique().first()
        user = await session.execute(select(User).where(User.uid == str(uid)))
        user = user.scalars().unique().first()
        if check_role and user:
            user_id = user.id
            data = RolesUsers(user_id=user_id, role_id=role_id.role_id)
            session.add(data)
            role = await session.execute(select(Role).where(Role.id == role_id.role_id))
            role = role.scalars().unique().first()
            await session.commit()
            return role
        return JSONResponse({"Message": "User or Role does not Exist"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/roles/{uid}/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def add_user_role_delete(uid: UUID, role_id: int , session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.uid == str(uid)))
        user = user.scalars().unique().first()
        user_id = user.id
        await session.execute(delete(RolesUsers).where(RolesUsers.user_id == user_id)
                              .where(RolesUsers.role_id == role_id))
        role = await session.execute(select(Role).where(Role.id == role_id))
        role = role.scalars().unique().first()
        await session.commit()
        logger.info(f"{role.name} has been successfully removed from user")
        return role
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
