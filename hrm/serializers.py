
from typing import List, Optional
from pydantic import BaseModel, validator
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from hrm.models import Employee, HrFileType, HrDocuments, LeaveConfig, Banks, EmployeeAddress, BankDetails, \
    JobDescription, LeaveRequest
from users.serializers import UserModel, RoleModelMatrix

EmployeeModel = sqlalchemy_to_pydantic(Employee)

LeaveConfigModel = sqlalchemy_to_pydantic(LeaveConfig)
BanksModel = sqlalchemy_to_pydantic(Banks)
LeaveRequestModel = sqlalchemy_to_pydantic(LeaveRequest)
HrFileTypeModelView = sqlalchemy_to_pydantic(HrFileType)
AddressModel = sqlalchemy_to_pydantic(EmployeeAddress)
BanksModel = sqlalchemy_to_pydantic(Banks)
BankDetailsModel = sqlalchemy_to_pydantic(BankDetails)


class EmployeeLeaveBlanceModel(BaseModel):
    balance: float
    leave_year: int
    leave_name: LeaveConfigModel
    requests: Optional[List[LeaveRequestModel]]

    class Config:
        orm_mode = True


class JobDescriptionModel(BaseModel):
    id: int
    role_id: int
    task: str
    task_description: str
    task_role: RoleModelMatrix

    class Config:
        orm_mode = True


class JobRoleModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    job_description: Optional[List[JobDescriptionModel]] = []
    task_role: Optional[RoleModelMatrix]

    class Config:
        orm_mode = True


class BanksModelMatrix(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BankDetModel(BaseModel):
    id: int
    bank_name: BanksModelMatrix
    account_number: str

    class Config:
        orm_mode = True


class HrFileTypeModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class HrDocumentsModel(BaseModel):
    id: int
    file_name: str
    doc_name: HrFileTypeModel

    class Config:
        orm_mode = True

class EmployeeModelAddress(BaseModel):
    id : int
    addresses: Optional[List[AddressModel]]

    class Config:
        orm_mode = True

class EmployeeModelAll(EmployeeModel):
    users: Optional[UserModel]
    addresses: Optional[List[AddressModel]]
    user_files: Optional[List[HrDocumentsModel]]
    bank: Optional[List[BankDetModel]]
    files: Optional[set]

    @validator('files', always=True, pre=True)
    def get_files(cls, v, values):
        buttons = [x for x in values["user_files"]]
        buttons = [str(x.doc_name.name) for x in buttons]
        return set(buttons)

    class Config:
        orm_mode = True