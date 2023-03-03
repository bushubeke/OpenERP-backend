import uuid
import enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, UniqueConstraint, Text, Float, Enum
from main.db import Base


# from sqlalchemy import Enum
# class MyEnum(enum.Enum):
#     one = 1
#     two = 2
#     three = 3
# t = Table(
#     'data', MetaData(),
#     Column('value', Enum(MyEnum))
# )
class EmployeeStatus(enum.Enum):
    Probation = "Probation"
    Contract = "Contract"
    Permanent = "Permanent"


class LeaveStatus(enum.Enum):
    Pending = "Pending"
    Canceled = "Canceled"
    Partial = "Partial"
    Approved = "Approved"
    Declined = "Declined"
    Completed = "Completed"


class Employee(Base):
    __tablename__ = 'hr_employee'
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=False)
    gender = Column(String(5), nullable=False)
    hire_date = Column(DateTime(timezone=True), nullable=True)
    manager_id = Column('manager_id', Integer(), ForeignKey('hr_employee.id'), nullable=True)
    gross_salary = Column('salary', Integer(), nullable=True)
    # status=Column('status',Enum(EmployeeStatus))
    user_id = Column('user_id', Integer(), ForeignKey('admin_user.id'), unique=True, nullable=False)
    addresses = relationship('EmployeeAddress', cascade="all, delete")
    bank = relationship('BankDetails')
    account_number = relationship('BankDetails', viewonly=True)
    users = relationship('User', lazy='joined', back_populates='name')
    user_files = relationship('HrDocuments')

    @property
    def name(self):
        return f"{self.first_name} {self.middle_name[0]} {self.last_name}"

    def __str__(self, ):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class EmployeeAddress(Base):
    __tablename__ = "hr_employee_address"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    employee_id = Column('employee_id', Integer(), ForeignKey('hr_employee.id'), nullable=False)
    city = Column(String(20), nullable=False)
    phone_number = Column(String(30), nullable=False)
    kebele = Column(Integer(), nullable=False)
    woreda = Column(Integer(), nullable=False)
    p_o_box = Column(String(10), nullable=False)


class HrFileType(Base):
    __tablename__ = "hr_file_type"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    name = Column(String(10), nullable=False)
    description = Column(Text())

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class HrDocuments(Base):
    __tablename__ = "hr_documents"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    file_name = Column(String(1000), nullable=False)
    employee_id = Column('employee_id', Integer(), ForeignKey('hr_employee.id'), nullable=False)
    document_type = Column('file_type_id', Integer(), ForeignKey('hr_file_type.id'), nullable=False)
    doc_name = relationship('HrFileType', back_populates='')


class Banks(Base):
    __tablename__ = "hr_banks"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    name = Column(String(50), nullable=False)

    def __str__(self):
        return f"{self.name}"


class BankDetails(Base):
    __tablename__ = "hr_bank_details"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    employee_id = Column('employee_id', Integer(), ForeignKey('hr_employee.id'), nullable=False)
    bank_id = Column('bank_id', Integer(), ForeignKey('hr_banks.id'), nullable=False)
    bank_name = relationship('Banks', viewonly=True)
    account_number = Column(String(100), nullable=False)


class JobDescription(Base):
    __tablename__ = 'hr_job_description'
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    role_id = Column('role_id', Integer(), ForeignKey('admin_role.id'), nullable=False)
    task = Column(String(50), nullable=False)
    task_description = Column(Text(2000), nullable=False)
    task_role = relationship('Role', viewonly=True)


class LeaveConfig(Base):
    __tablename__ = "hr_leave_config"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    name = Column(String(30), nullable=False)
    days = Column(Float(), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


def set_balance(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)

    return default_function


class EmployeeLeave(Base):
    __tablename__ = "hr_employee_leave"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    employee_id = Column('employee_id', Integer(), ForeignKey('hr_employee.id'), nullable=False)
    leave_config_id = Column(Integer(), ForeignKey('hr_leave_config.id'), nullable=False)
    days = Column(Float(), nullable=False)
    balance = Column(Float(), default=set_balance('days'))
    leave_year = Column(Integer(), nullable=False)
    status = Column(Boolean(), nullable=False, default=True)
    leave_name = relationship('LeaveConfig')
    ename = relationship('Employee', viewonly=True)
    requests = relationship('LeaveRequest', viewonly=True)
    UniqueConstraint(employee_id, leave_config_id, leave_year)

    def __repr__(self):
        return f"{self.leave_name}-{self.leave_year}"


class LeaveRequest(Base):
    __tablename__ = "hr_leave_request"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    leave_id = Column(Integer(), ForeignKey('hr_employee_leave.id'))
    start_date = Column(DateTime(timezone=True), nullable=False)
    requested_days = Column(Float(), nullable=False)
    status = Column(String(9), default="Pending")
    partial = Column(Float(), default=0.0)


