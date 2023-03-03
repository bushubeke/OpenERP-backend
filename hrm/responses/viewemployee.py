from . import *

@hr_app.route('/details',methods=["GET"])
@roles_accepted('superuser','Hr Admin')
def view_employee():
    employees=db.session.execute(select(Employee).options(joinedload(Employee.users)).options(joinedload(Employee.bank).subqueryload(BankDetails.bank_name)).\
        options(joinedload(Employee.adresses)).options(joinedload(Employee.user_files).subqueryload(HrDocuments.doc_name))).unique().scalars().all()
    employees=[EmployeeModelAll.from_orm(x).dict() for x in employees]
    return render_template('hrm/viewemployee.html',peoples=employees)


@hr_app.route('/details/<uid>/',methods=["GET"])
@roles_accepted('superuser','Hr Admin')
def view_single_employee(uid):
    user_id=db.session.execute(select(User).where(User.uid==uid)).scalars().unique().first().id
    employees=db.session.execute(select(Employee).where(Employee.user_id == user_id).options(joinedload(Employee.users)).options(joinedload(Employee.bank).subqueryload(BankDetails.bank_name)).\
        options(joinedload(Employee.adresses)).options(joinedload(Employee.user_files).subqueryload(HrDocuments.doc_name))).unique().scalars().all()
    employees=[EmployeeModelAll.from_orm(x).dict() for x in employees]
    return render_template('hrm/singleemployee.html',peoples=employees)


@hr_app.route('/personal/<uid>/',methods=["GET"])
@roles_xor('superuser')
def personal_single_employee(uid):
    user_id=db.session.execute(select(User).where(User.uid==uid)).scalars().unique().first().id
    employees=db.session.execute(select(Employee).where(Employee.user_id == user_id).options(joinedload(Employee.users)).options(joinedload(Employee.bank).subqueryload(BankDetails.bank_name)).\
        options(joinedload(Employee.adresses)).options(joinedload(Employee.user_files).subqueryload(HrDocuments.doc_name))).unique().scalars().all()
    employees=[EmployeeModelAll.from_orm(x).dict() for x in employees]
    return render_template('hrm/personalemployee.html',peoples=employees)
