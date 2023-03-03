from . import *


@hr_app.get('/addrops/{uid}', response_model=EmployeeModelAddress)
async def address_get(uid: UUID, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.uid == str(uid)))
        user = user.scalars().unique().first()
        user_id = user.id
        employee = await session.execute(select(Employee).where(Employee.user_id == int(user_id)).
                                         options(joinedload(Employee.addresses)))
        employee = employee.scalars().unique().first()
        if employee:
            return employee
        else:
            return JSONResponse({"Message": "Address Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@hr_app.post('/addrops/', response_model=AddressModel)
async def address_post(new_address: AddressModel, session: AsyncSession = Depends(get_session)):
    try:
        session.add(EmployeeAddress(new_address.dict()))
        await session.commit()
        return address
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@hr_app.delete('/addrops/{del_id}')
async def address_delete(del_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(delete(AddressModel).where(AddressModel.id == del_id))
        await session.commit()
        return JSONResponse({"Message": "Deleting Object Successful"}, status_code=status.HTTP_202_ACCEPTED)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        await session.rollback()
        return JSONResponse({"Message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
