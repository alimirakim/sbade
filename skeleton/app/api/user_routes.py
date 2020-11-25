from flask import Blueprint, jsonify
from app.models import db, User, Stamp, Program, Member, Habit, Reward, Color, DailyStamp
from app.schemas import user_schema, program_schema, habit_schema, member_schema, stamp_schema, color_schema, dailystamp_schema
from sqlalchemy.orm import joinedload
from flask_login import current_user, login_user, logout_user, login_required
from app.utils import dump_data_list
from datetime import date, timedelta
import calendar

user_routes = Blueprint('users', __name__, url_prefix="/users")


@user_routes.route('/list')
@login_required
def users():
    users = User.query.all()
    return {"users": [user.to_dict() for user in users]}


@user_routes.route('/')
@login_required
def user():
    """Get the current user's information."""
    user = User.query.filter(User.id == current_user.id).options(joinedload(User.stamp)).one()
    user_data = user_schema.dump(user)
    user_data["stamp"] = user.stamp.to_dict()
    print(user_data, "--------------------HEREE--------------")
    del user_data["hashed_password"]
    return jsonify(user_data)


# TESTED Functions
@user_routes.route("/<int:uid>")
def user_details(uid):
    """Get a user's information by id."""
    user = User.query.get(uid)
    user_data = user_schema.dump(user)
    return jsonify(user_data)




@user_routes.route("/<int:uid>/programs")
def user_programs(uid):
    """Get a user's subscribed programs."""
    current_date = date.today()
    past_week = [(current_date - timedelta(days=i)) for i in range(7)]
    past_week = [(day.strftime('%A')[0:3], day.strftime('%Y-%m-%d')) for day in past_week]
    
    print("\n\nUID", uid)
    user_programs = Program.query \
        .join(Member.program).filter(Member.member_id == uid) \
        .options(joinedload(Program.rewards), \
            joinedload(Program.members), \
            joinedload(Program.stamp), \
            joinedload(Program.color), \
            joinedload(Program.habits).joinedload(Habit.daily_stamps), \
            joinedload(Program.habits).joinedload(Habit.stamp), \
            joinedload(Program.habits).joinedload(Habit.color)) \
        .all()
        # .join(DailyStamp) \
    programs_data = dump_data_list(user_programs, program_schema)
    print("\n\nPROGRAM DATAAAA")
    print(user_programs)
    from pprint import pprint
    pprint(programs_data)
    
    for i in range(len(user_programs)):
        if user_programs[i].members: 
            memberships = [m.id for m in current_user.memberships]
            print("\n\nmemberships", memberships)
            try:
                [mid] = [m for m in programs_data[i]["members"] if m in memberships]
                programs_data[i]["habits"] = []
                
                for j in range(len(user_programs[i].habits)):
                    programs_data[i]["habits"].append(habit_schema.dump(user_programs[i].habits[j]))
                    habit = habit_schema.dump(user_programs[i].habits[j])
                    habit["stamp"] = stamp_schema.dump(user_programs[i].habits[j].stamp)
                    habit["color"] = color_schema.dump(user_programs[i].habits[j].color)
                    # Daily stamps for prev week for habit
                    habit["daily_stamps"] = DailyStamp.query.filter( \
                        DailyStamp.habit_id == habit["id"], \
                        DailyStamp.member_id == mid, \
                        DailyStamp.date <= past_week[0][1], \
                        DailyStamp.date >= past_week[6][1]).all()
                    habit["daily_stamps"] = dump_data_list(habit["daily_stamps"], dailystamp_schema)
                    programs_data[i]["habits"][j] = habit
            except:
                print("\nno mid probs")
        programs_data[i]["stamp"] = stamp_schema.dump(user_programs[i].stamp)
        programs_data[i]["color"] = color_schema.dump(user_programs[i].color)
        
    from pprint import pprint
    print("\nPROGRAMS DATA")
    pprint(programs_data)
    return jsonify(programs_data=programs_data, past_week=past_week)