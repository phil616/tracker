from response.std import URFRouter
from model.Schedule import Schedule,ScheduleIn
from fastapi.background import BackgroundTasks
from model.User import User
from fastapi import Security, HTTPException
from core.background import send_schedule
from core.authorize import check_permissions

schedule_router = URFRouter(prefix="/schedule", dependencies=[Security(check_permissions, scopes=["user:read", "user:write"])])

@schedule_router.post("/new")
async def new_schedule(schedule:ScheduleIn,background:BackgroundTasks):
    
    current_user = await User.filter(user_id=schedule.user_id).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_schedule = await Schedule.create(
        schedule_date=schedule.schedule_date,
        schedule_place=schedule.schedule_place,
        schedule_title=schedule.schedule_title,
        schedule_description=schedule.schedule_description,
        receiver_email=current_user.email,
        is_send=False
    )
    background.add_task(
        send_schedule,
        schedule=schedule,
        sid=new_schedule.schedule_id
    )
    return {"message": "Schedule created successfully"}

@schedule_router.get("/all")
async def get_all_schedules():
    schedules = await Schedule.all()
    return schedules