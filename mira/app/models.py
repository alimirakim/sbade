from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

default_color = "#000"
default_stamps = {
  "user": 1, #"user-circle"
  "program": 2, #"calendar-alt"
  "habit": 3, #"check-circle"
  "reward": 4, #"award"
}

bonds = db.Table( # combined unique constraint
    "bonds",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user1_id", db.Integer, db.ForeignKey("users.id"), nullable=False),
    db.Column("user2_id", db.Integer, db.ForeignKey("users.id"), nullable=False),
    db.Column("created_at", db.DateTime, default=datetime.now()),
)

redeemed = db.Table(
    "redeemed",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False),
    db.Column("reward_id", db.Integer, db.ForeignKey("rewards.id"), nullable=False),
    db.Column("redeemed_at", db.DateTime, nullable=False, default=datetime.now())
)


class Stamp(db.Model):
    __tablename__ = "stamps"
    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)

    users = db.relationship("User", back_populates="stamp")
    programs = db.relationship("Program", back_populates="stamp")
    habits = db.relationship("Habit", back_populates="stamp")
    rewards = db.relationship("Reward", back_populates="stamp")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=False, default=default_color)
    stamp_id = db.Column(db.Integer, db.ForeignKey("stamps.id"), nullable=False, default=default_stamps["user"])
    birthday = db.Column(db.Date)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    stamp = db.relationship("Stamp", back_populates="users")
    created_programs = db.relationship("Program", back_populates="creator")
    created_habits = db.relationship("Habit", back_populates="creator")
    created_rewards = db.relationship("Reward", back_populates="creator")
    members = db.relationship("Member", back_populates="member")
    stampers = db.relationship("Member", back_populates="stamper")
    redeemed = db.relationship("Reward", secondary=redeemed, back_populates="redeemed")
    bonds = db.relationship("Bond", secondary=bonds, back_populates="bonds")


class Program(db.Model):
    __tablename__ = "programs"
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    color = db.Column(db.String(7), nullable=False, default=default_color)
    stamp_id = db.Column(db.Integer, db.ForeignKey("stamps.id"), nullable=False, default=default_stamps["program"])
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    stamp = db.relationship("Stamp", back_populates="programs")
    creator = db.relationship("User", back_populates="created_programs")
    members = db.relationship("Member", back_populates="program")
    habits = db.relationship("Habit", back_populates="program")
    rewards = db.relationship("Reward", back_populates="program")


class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stamper_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    points = db.Column(db.Integer, nullable=False, default=0)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO Program+member should be unique

    program = db.relationship("Program", back_populates="members")
    member = db.relationship("User", back_populates="members")
    stamper = db.relationship("User", back_populates="stampers")
    daily_stamps = db.relationship("Daily_Stamp", back_populates="member")


class Habit(db.Model):
    __tablename__ = "habits"
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    frequency = db.Column(db.String(7), nullable=False, default="ttttttt")
    color = db.Column(db.String(7), nullable=False, default=default_color)
    stamp_id = db.Column(db.Integer, db.ForeignKey("stamps.id"), nullable=False, default=default_stamps["habit"])
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"))
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO habit+program should be unique

    stamp = db.relationship("Stamp", back_populates="habits")
    program = db.relationship("Program", back_populates="habits")
    creator = db.relationship("User", back_populates="created_habits")
    daily_stamps = db.relationship("Daily_Stamp", back_populates="habit")


class Daily_Stamp(db.Model):
    __tablename__ = "daily_stamps"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.today())
    status = db.Column(db.Enum('unstamped', 'pending', 'stamped', name="status"))
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"))
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    habit = db.relationship("Habit", back_populates="daily_stamps")
    member = db.relationship("Member", back_populates="daily_stamps")


### FOR REWARD SHOP STRETCH GOAL BELOW:
class Reward(db.Model):
    __tablename__ = "rewards"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False) # enum?
    reward = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    cost = db.Column(db.Integer, nullable=False, default=7)
    color = db.Column(db.String(7), nullable=False, default=default_color)
    limit_per_member = db.Column(db.Integer, nullable=False, default=1)
    quantity = db.Column(db.Integer, nullable=False, default=-1)
    stamp_id = db.Column(db.Integer, db.ForeignKey("stamps.id"), nullable=False, default=default_stamps["reward"])
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"))
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO program+ reward should be unique

    stamp = db.relationship("Stamp", back_populates="rewards")
    program = db.relationship("Program", back_populates="rewards")
    creator = db.relationship("User", back_populates="created_rewards")
    redeemed = db.relationship("User", back_populates="redeemed")