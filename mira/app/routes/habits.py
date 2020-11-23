from flask import Blueprint, render_template, redirect
from app.models import db, User, Program, Habit, Member, DailyStamp
from app.schemas import user_schema, program_schema, habit_schema, member_schema, dailystamp_schema
from app.utils import dump_data_list

habits = Blueprint("habits", __name__, url_prefix="/habits")


@habits.route("/programs/<int:pid>")
def program_habits(pid):
    """Get a list of a program's habits."""
    habits = Habit.query.filter(Habit.program_id == pid).all()
    return jsonify(dump_data_list(habits, habit_schema))
  

@habits.route("/<int:hid>")
def habit_details(hid):
    """Get a habit's details, including recent histories for all members."""
    habit = Habit.query.filter(Habit.id == hid).one()
    return jsonify(habit_schema.dump(habit))


@habits.route("/programs/<int:pid>", methods=["POST"])
def create_habit(pid):
    """Create a new habit for a program."""
    # habit = Habit(habit=,
    #               description=,
    #               frequency=,
    #               color=,
    #               stamp_id=,
    #               program_id=,
    #               creator_id=,)
    # db.session.add(habit)
    db.session.commit()
    return jsonify(habit_schema.dump(habit))


@habits.route("/<int:hid>", methods=["PATCH"])
def edit_habit(hid):
    """Edit a habit's details by id."""
    habit = Habit.query.filter(Habit.id == hid).one()
    # habit.habit = 
    # habit.description = 
    # habit.frequency = 
    # habit.color = 
    # habit.stamp_id = 
    # habit.program_id = 
    # habit.creator_id = 
    db.session.commit()
    return jsonify(habit_schema.dump(habit))
    

@habits.route("/<int:hid>", methods=["DELETE"])
def delete_habit(hid):
    """Delete a habit by id."""
    habit = Habit.query.filter(Habit.id == hid).one()
    db.session.delete(habit)
    db.commit()
    return "Habit is donezo~!"


# How to get the date/daily stamp through params?
# Get the stamper for the daily stamp's member
# If no stamper, just toggle the status.
# If stamper, check stamper id from params. If it's the member, NOT stamper,
# change to pending. If it IS the stamper, change to checked or unchecked.
@habits.route("/dailystamps/<int:sid>/stamper/<int:uid>", methods=["POST"])
def stamp_day(sid, uid):
    """Change the status of a daily_stamp to 'stamped' or 'pending'."""
    day = DailyStamp.query.filter(DailyStamp.id == sid)
    if uid == day.member.stamper_id:
        if day.status == 'unstamped' or day.status == 'pending':
            day.status = 'stamped'
        elif day.status == 'stamped':
            day.status = 'unstamped'
    elif uid == day.member_id:
        if day.status == 'unstamped':
            day.status = 'pending'
        elif day.status == 'pending':
            day.status = 'unstamped'
    return jsonify(dailystamp_schema.dump(day))