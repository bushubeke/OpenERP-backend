import os
from uuid import  uuid4,UUID
from datetime import datetime,timedelta,timezone
from random import randint
from json import loads
from main.db import get_session
from users.models import User
from users.serializers import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete,exists
from sqlalchemy.orm import joinedload,subqueryload,selectinload
from fastapi import status, APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate
from erplogging import logger
from hrm.serializers import HrFileTypeModel,LeaveConfigModel,BanksModel,EmployeeModelAll,BankDetModel,HrFileTypeModelView,AddressModel,\
    HrDocumentsModel,JobDescriptionModel,JobRoleModel,EmployeeLeaveBlanceModel,EmployeeModelAddress
from hrm.models import HrFileType,LeaveConfig,Banks,Employee,EmployeeLeave,EmployeeAddress,HrDocuments,LeaveRequest,JobDescription,\
    LeaveRequest,BankDetails

hr_app=APIRouter()
#
# from hrm.responses.index import index
# from hrm.responses.sendmail import send_mail
# from hrm.responses.formone import formone
# from hrm.responses.fromtwo import formtwo
# from hrm.responses.leave import form_add_view_leave_type,set_leave,approve_leave_request,request_leave_type,decline_leave_request,cancel_leave_request,\
#     set_specfic_leave,deactivate_leave
# from hrm.responses.formemployee import form_employee
# from hrm.responses.filetype import form_add_view_file_type
# from hrm.responses.formthree import form_three
# from hrm.responses.bankdetails import bank_details
# from hrm.responses.banks import form_add_view_banks
# from hrm.responses.uploadtest import uploadtest
# from hrm.responses.dowloaded import downloaded
# from hrm.responses.employee import employee
# from hrm.responses.documents import documents
from hrm.responses.address import address_get, address_post, address_delete
# from hrm.responses.jobdescription import form_add_view_jd
# from hrm.responses.viewemployee import view_employee,view_single_employee,personal_single_employee
# from hrm.responses.automated import activate_employee,deactivate_employee,automation_page