from model.Task import Task, TaskSchema
from model.User import User
import asyncio
import datetime
from core.setting import config
from lib.api_email import send_email,Email
import pytz
from core.logger import log

async def send_notice(task:TaskSchema):
    user_id = task.task_assignee
    user = await User.filter(user_id=user_id).first()
    user_email = user.email
    contest_msg = f"""<html>
    <head></head>
    <body>
    <h1>Task Due Notice</h1>
        <p>Dear {user.username},</p>
        <p>Your task {task.task_name} is due in 10 minutes.</p>

        <p> {task.task_description}</p>
        <p> Pority : {task.task_priority}</p>
        <p>Tracking System</p>
        <p>At {datetime.datetime.now()}</p>
    </body>
</html>
"""
    construct_email = Email(
        host=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASSWORD,
        send_to_addr=user_email,
        from_addr=config.EMAILS_FROM_EMAIL,
        subject=f"[Tracking System] Your task {task.task_name} is due in 10 minutes",
        contest_msg=contest_msg,
        text="html"
    )        
    log.info(f"Sending email with {construct_email.model_dump()}")
    await send_email(construct_email)
    log.info(f"Email sent to {user_email}")

async def bg_check_tasks():
    log.info("[Background Task] Background task started")
    while True:
        tasks = await Task.filter(task_status=1)
        for task in tasks:
            # less than 10 minutes left
            offset_seconds = task.task_start_time - datetime.datetime.now(pytz.utc)
            if offset_seconds.total_seconds() < 600:
                task.task_status = 2
                await task.save()
                await send_notice(TaskSchema(**task.__dict__))  # send email to user
        await asyncio.sleep(60)
        # log.info("[Background Task] next Background task running") # save logs