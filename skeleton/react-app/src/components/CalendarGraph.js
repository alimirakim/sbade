import React from 'react'
import CalendarHeatmap from 'react-calendar-heatmap';
import '../styles/CalendarGraph.css'

function CalenderGraph() {
    return (
        <div>
            <CalendarHeatmap
                startDate={new Date('2016-01-01')}
                endDate={new Date('2016-12-31')}
                values={[
                    { date: '2016-01-01' },
                    { date: '2016-01-22' },
                    { date: '2016-01-30' },
                    { date: '2016-02-30' },
                    { date: '2016-03-30' },
                    { date: '2016-04-30' },
                    { date: '2016-05-30' },
                    // ...and so on
                ]}
            />
        </div>
    )
}

export default CalenderGraph
