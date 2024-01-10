import csv
from datetime import datetime, timedelta

import pytz
import yaml

schedule = {}
source_tz = pytz.timezone('America/New_York')
home_tz = pytz.timezone('America/Denver')
with open('2023_2024_nuggets_schedule.csv') as raw_sched:
    reader = csv.DictReader(raw_sched)
    for row in reader:
        start_datetime = row['Date'] + ' ' + row['Start (ET)']
        start = datetime.strptime(start_datetime, '%a %b %d %Y %I:%M%p')
        start.replace(tzinfo=source_tz)
        local_start = start.astimezone(home_tz)
        event_start = local_start - timedelta(hours=6)
        schedule_name = datetime.strftime(local_start, '%Y%m%d') + row['Opponent'].replace(' ', '')
        schedule_expression = datetime.strftime(event_start, '%Y-%m-%dT%H:%M:%S')
        event = {
                'Type': 'ScheduleV2',
                'Properties': {
                    "GroupName": "NuggetsSchedule",
                    'ScheduleExpression': f"at({schedule_expression})",
                    'ScheduleExpressionTimezone': 'America/Denver'
                }
        }
        schedule[schedule_name] = event

print(yaml.dump(schedule, default_style=None, default_flow_style=False))