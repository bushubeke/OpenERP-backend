import typer
import asyncio
# import psycopg
import subprocess
# from tqdm import tqdm
from pathlib import Path
# from sqlalchemy import delete,text
# from sqlalchemy.sql import text as stext
from main.main import create_dev_app
from main.db import async_main
from hrm.models import Employee,EmployeeAddress,EmployeeLeave,Banks,BankDetails,\
    JobDescription,HrDocuments,HrFileType,LeaveConfig,LeaveRequest
from users.models import User, Role, RouteResponse

path = Path(__file__).parent
capp = typer.Typer()
app = create_dev_app()
# /home/bushu/.local/share/virtualenvs/openerp-vNWIj9jV/bin/python

@capp.command()
def rung():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    #  to make ssl keys
    # openssl genrsa 4096 > ssl.key
    # openssl req -new -x509 -nodes -sha1 -days 365 -key ssl.key > ssl.cert
    subprocess.run(["gunicorn", "manage:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:9500", "--reload",
                    "-w", "1", "--keyfile", "ssl.key", "--certfile", "ssl.cert", "--ssl-version", "TLSv1_2"])


@capp.command()
def runh():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:9000 with one worker
    """
    subprocess.run(["hypercorn", "manage:app", "-b", "0.0.0.0:9500", "--reload",
                    "-w", "1", "--keyfile", "ssl.key", "--certfile", "ssl.cert"])


@capp.command()
def upgrade():
    """creates  base models based on their metadata"""
    asyncio.run(async_main())

@capp.command()
def migratenew():
    from main.db import engine
    RouteResponse.metadata.create_all(bind=engine)
    print('Worked')

if __name__ == "__main__":
    capp()
