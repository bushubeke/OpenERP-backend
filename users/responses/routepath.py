from . import *


@useradmin.get('/response_path', response_model=Page[RouteResponseModel], dependencies=[Depends(get_current_user)])
async def response_path_get(session: AsyncSession = Depends(get_session)):
    try:
        my_routes = await session.execute(select(RouteResponse))
        my_routes = my_routes.unique().scalars().all()
        logger.info('Routes have been fetched successfully')
        return paginate(my_routes)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.post('/response_path', response_model=RouteResponsePostModel, dependencies=[Depends(get_current_user)])
async def response_path_post(my_route: RouteResponsePostModel, session: AsyncSession = Depends(get_session)):
    try:
        my_route = RouteResponse(**my_route.dict())
        session.add(my_route)
        await session.commit()
        logger.info(f'Path { my_route } have been created successfully')
        print(my_route)
        return my_route
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/response_path/{route_id}', response_model=RouteResponsePostModel,
                 dependencies=[Depends(get_current_user)])
async def response_path_patch(route_id: int, my_route: RouteResponsePostModel,
                              session: AsyncSession = Depends(get_session)):
    try:
        check_route = await session.execute(select(RouteResponse).where(RouteResponse.id == route_id))
        check_route = check_route.scalars().unique().first()
        if check_route:
            await session.execute(update(RouteResponse).where(RouteResponse.id == route_id).values(**my_route.dict()))
            await session.commit()
            logger.info(f'Path {my_route} have been updated successfully')
            return my_route
        return JSONResponse({"Message": "No Such Path"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/response_path/{route_id}', response_model=RouteResponsePostModel,
                  dependencies=[Depends(get_current_user)])
async def response_path_delete(route_id: int, session: AsyncSession = Depends(get_session)):
    try:
        my_route = await session.execute(select(RouteResponse).where(RouteResponse.id == route_id))
        my_route = my_route.unique().scalars().first()
        if my_route:
            await session.execute(delete(RouteResponse).where(RouteResponse.id == route_id))
            await session.commit()
            logger.info(f'Path {my_route} have been deleted successfully')
            return my_route
        else:
            return JSONResponse({"Message": "Path Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.post('/response_path/{route_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def add_response_path_role_post(route_id: int, role_id: AddRole, session: AsyncSession = Depends(get_session)):
    try:
        role = await session.execute(select(Role).where(Role.id == role_id.role_id))
        role = role.scalars().unique().first()
        my_route = await session.execute(select(RouteResponse).where(RouteResponse.id == route_id))
        my_route = my_route.unique().scalars().first()
        if role and my_route:
            data = RouteResponseRoles(role_id=role_id.role_id, route_id=route_id)
            session.add(data)
            await session.commit()
            return role
        return JSONResponse({"Message": "Path or role  Not Found"}, status_code=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/response_path/{route_id}/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def add_response_path_role_delete(route_id: int, role_id : int, session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(delete(RouteResponse).where(RouteResponse.route_id == route_id)
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
