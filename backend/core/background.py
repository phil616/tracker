from model.Task import Task, TaskSchema
from model.User import User
from model.Schedule import ScheduleIn,Schedule
import asyncio
import datetime
from core.setting import config
from lib.api_email import send_email,Email
import pytz
from core.logger import log
import uuid
async def send_schedule(schedule:ScheduleIn,sid:int):
    user_id = schedule.user_id
    user = await User.filter(user_id=user_id).first()
    user_email = user.email
    contest_msg = f"""<html>
    <head></head>
    <body>
    <h1>Schedule Archive</h1>
        <p>Dear {user.username}, you have a new schedule for archive.</p>

        <p> Title : {schedule.schedule_title}</p>
        <p> Description : {schedule.schedule_description}</p>
        <p> Date: {schedule.schedule_date} </p>
        <p> Place: {schedule.schedule_place} </p>
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
        subject=f"[Tracking System] Schedule {schedule.schedule_title}",
        contest_msg=contest_msg,
        text="html"
    )        
    log.info(f"Sending email with {construct_email.model_dump()}")
    await send_email(construct_email)
    schedule = await Schedule.filter(schedule_id=sid).first()
    schedule.is_sent = True
    await schedule.save()
    log.info(f"Email sent to {user_email}")


async def send_notice(task:TaskSchema):
    user_id = task.task_assignee
    user = await User.filter(user_id=user_id).first()
    user_email = user.email
    content_msg_header = """
    <!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>
<style>
        body {
        font-family: Arial, sans-serif;
        margin: 0;
        margin-top: 20px;
        padding: 0;
        background-color: #e6f9e6; 
    }.email-container {
        background-color: #ffffff;
        width: 600px;
        margin: auto;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1); 
    }header {
        display: flex;
        align-items: center;
        justify-content: start;
    }footer {
        border-top: 1px solid #ddd;
        padding-top: 10px;
        font-size: 12px;
    }.footer-links a {
        color: gray; 
        
        margin-right: 15px;
    }.gray-bold {
        color: gray; 
        font-weight: bold; 
    }.gray-normal {
        color: gray; 
        font-weight: normal; 
    }</style>
</head>
<body>
"""
    content_msg_body = f"""<div class="email-container">
    <table>
        <tr>
            <th></th>
            <th></th>
        </tr>
        <tr>
            <th> <img src="https://phil616vue.pages.dev/img/gs.b3add859.png" alt="GreenShadeCapital Logo" style="height: auto; width: 50px; padding: 10px; margin-right: 10px;"></th>
            <th style="font-size: 28px;">Green Shade Telegram</th>
        </tr> 
    </table>
    <hr>
    <h2>Your task is due in 10 minutes.</h2>
    <p class="gray-normal">References: {uuid.uuid4().hex}</p>
    <p>Dear  {user.username}</p>
    <p>Task: <strong>{task.task_name}</strong></p>
        <p> {task.task_description}</p>
        <p> Pority : {task.task_priority}</p>
        <p>Tracking System</p>
        <p>At {datetime.datetime.now(pytz.utc)}</p>
    <footer>
        <div>
            <p class="gray-bold">THIS IS A GREENSHADECAPITAL SERVICE EMAIl</p>
            <p class="gray-normal">This email was sent to you because you are a GreenShadeCapital customer or requested information about our services.</p>
            <p class="gray-normal">© 2024 Green Shade Capital. All Rights Reserved.</p>
        </div>
        <div class="footer-links">
            <a href="https://greenshadecapital.com">GreenShadeCapital</a>
            <a href="https://secure.greenshadecapital.com">OSCP&amp;PGP</a>
            <a href="https://help.greenshadecapital.com">Support</a>
        </div>
    </footer>
</div>
</body>
</html>
"""
    contest_msg = content_msg_header + content_msg_body
    construct_email = Email(
        host=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASSWORD,
        send_to_addr=user_email,
        from_addr="Tracker <" + config.EMAILS_FROM_EMAIL+">",
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