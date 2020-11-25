import React, { useEffect, useState, useContext } from "react";

import UserContext from '../context/UserContext'
import HabitBoardContext from "../context/HabitBoardContext"

export default function HabitBoard() {
  // const uid = document.cookie.split("; ").find(cookie => cookie.startsWith("uid_cookie")).split("=")[1]

  const [programs, setPrograms] = useState()
  const [week, setWeek] = useState()

  const user = useContext(UserContext);
  const uid = user.id

  useEffect(() => {
    (async () => {
      console.log("UNRAVELED", uid, programs)
      if (!programs) {
        const res = await fetch(`/api/users/${uid}/programs`)
        const { past_week, programs_data } = await res.json()
        setPrograms(programs_data)
        setWeek(past_week)
      }
    })()
  }, [programs, week, uid])

  console.log("prograaams", programs)
  if (!week) return null
  return (
    <HabitBoardContext.Provider value={{ programs, week }}>
      <HabitsEntry />
    </HabitBoardContext.Provider>
  )
}





function HabitsEntry() {
  const { programs, week } = useContext(HabitBoardContext)
  const user = useContext(UserContext)
  console.log("programs", programs)
  console.log("week", week)

  if (!week) return null
  console.log("WEEK", week)
  return (
    <article>
      <h2>Habit Board</h2>
      <table style={{ borderWidth: "1px" }}>
        <thead>
          <tr>
            <th>Habit</th>
            <th><time dateTime={week[0][1]}>{week[0][0]} <br /><small>{week[0][1].slice(8, 10)}</small></time></th>
            <th><time dateTime={week[1][1]}>{week[1][0]} <br /><small>{week[1][1].slice(8, 10)}</small></time></th>
            <th><time dateTime={week[2][1]}>{week[2][0]} <br /><small>{week[2][1].slice(8, 10)}</small></time></th>
            <th><time dateTime={week[3][1]}>{week[3][0]} <br /><small>{week[3][1].slice(8, 10)}</small></time></th>
            <th><time dateTime={week[4][1]}>{week[4][0]} <br /><small>{week[4][1].slice(8, 10)}</small></time></th>
            <th><time dateTime={week[5][1]}>{week[5][0]} <br /><small>{week[5][1].slice(8, 10)}</small></time></th>
            <th><time dateTime={week[6][1]}>{week[6][0]} <br /><small>{week[6][1].slice(8, 10)}</small></time></th>
          </tr>
        </thead>
        <tbody>
          {programs.map(program => (
            <>
              <tr style={{ color: program.color.hex }}>
                <td colSpan={8}>
                  <h3><img src={`/icons/${program.stamp.stamp}.svg`} style={{ height: "1rem", width: "1rem" }} alt="" /> {program.program}</h3>
                </td>
              </tr>
              {program.habits.map(habit => (
                <tr style={{ color: habit.color.hex }}>
                  <td>
                    <img
                      src={`/icons/${habit.stamp.stamp}.svg`}
                      alt={`${habit.stamp.type}: {habit.stamp.stamp}`}
                      style={{ height: "1rem", width: "1rem" }}
                    />
                    {habit.habit}
                  </td>
                  {week.map(day => {
                    const [mid] = program.members.filter(m => user.memberships.includes(m))
                    console.log("mid", mid)
                    return (
                      <StampBox pid={program.id} mid={mid} habit={habit} day={day} />
                    )
                  })}
                </tr>
              ))}
            </>
          ))}
        </tbody>
      </table>
    </article>
  )
}

function StampBox({ pid, mid, habit, day }) {
  console.log("pid, mid, habit, day", pid, mid, habit, day)
  const [isStamped, setIsStamped] = useState(habit.daily_stamps.find(stamp => stamp.date == day[1]))

  // TODO WHY IS NOT DELETING ICON ON CLICK TOO???
  useEffect(() => {
    // console.log("habit on effect", habit)
    console.log("isStamped", isStamped)
    if (!isStamped) setIsStamped(false);
    if (habit.daily_stamps.find(stamp => stamp.date == day[1])) setIsStamped(true)
  }, [isStamped])

  async function onStamp(ev) {
    ev.preventDefault()
    const res = await fetch(`/api/habits/${habit.id}/programs/${pid}/members/${mid}/days/${day[1]}`, { method: "POST" })
    const dailyStamp = await res.json()
    console.log("what is dailyStamp", dailyStamp)
    if (dailyStamp.status) {
      if (dailyStamp.status === "stamped") setIsStamped(true)
    } else {
      console.log("nothin")
      setIsStamped(false)
    }
  }


  if (isStamped) {
    return (
      <td>
        <form method="POST" action={`/api/habits/${habit.id}/programs/${pid}/members/${mid}/days/${String(day.slice(1))}`} onSubmit={onStamp}>
          <button type="submit">
            <img
              src={`/icons/${habit.stamp.stamp}.svg`}
              alt={`${habit.stamp.type}: {habit.stamp.stamp}`}
              style={{ height: "1rem", width: "1rem" }}
            />
          </button>
        </form>
      </td>
    )

  } else {
    return (
      <td>
        <form method="POST" action={`/api/habits/${habit.id}/programs/${pid}/members/${mid}/days/${String(day.slice(1))}`} onSubmit={onStamp}>
          <button type="submit">
            <span>X</span>
          </button>
        </form>
      </td>
    )
  }
}

function StampBoxMark({ habit, day }) {
  const [isStamped, setIsStamped] = useState(false)

  useEffect(() => {
    const foundStamp = habit.daily_stamps.find(stamp => stamp.date == day[1])
    if (foundStamp) setIsStamped(true)
    else setIsStamped(false)
  }, [isStamped])

  if (isStamped) {
    return (
      <img
        src={`/icons/${habit.stamp.stamp}.svg`}
        alt={`${habit.stamp.type}: {habit.stamp.stamp}`}
        style={{ height: "1rem", width: "1rem" }}
      />
    )
  } else {
    return (
      <span>X</span>
    )
  }
}
