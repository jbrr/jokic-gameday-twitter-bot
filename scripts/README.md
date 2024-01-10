# Schedule CSV to `ScheduleExpression`

This is a quick script to convert season schedule CSVs (provided by 
[Basketball Reference](https://basketball-reference.com) to the [`ScheduleExpression`](https://docs.aws.amazon.com/scheduler/latest/APIReference/API_CreateSchedule.html#scheduler-CreateSchedule-request-ScheduleExpression) 
format used by AWS EventBridge Scheduler. 

## Requirements
- `pytz` and `pyyaml` are needed for this script, but not needed for the actual SAM deployment, so I kept them separate in `scripts/requirements.txt` 
- One manual change needs to be made to the CSV before executing the script: Change the times in the `Start (ET)` column to use AM or PM instead of a or p. For example,`Sat Nov 4 2023,9:00p` needs to be `Sat Nov 4 2023,9:00PM` for the script to work.

## Usage
It prints YAML to the console, and you can copy and paste that under the `Events` key in the `AWS::Serverless::Function` resource in `template.yaml`. This process could be improved, and maybe it'll be worth the effort come playoff time.
