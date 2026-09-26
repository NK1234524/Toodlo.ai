from datetime import datetime, timedelta


def calculate_due_date(deadline_type, deadline_value):
    today = datetime.now().astimezone()
# Weekly calcualtion
    if deadline_type == "explicit":
        weekdays = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }

        value = deadline_value.lower().strip()

        if value in weekdays:
            target_day = weekdays[value]
            days_ahead = (target_day - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            return today + timedelta(days=days_ahead)
# Relative calculation        
    if deadline_type == "relative":
            days = int(deadline_value.split()[0])
            return today + timedelta(days=days)

# Suggested due_date
    if deadline_type == "suggested":
         days = int(deadline_value.split()[0])
         return today + timedelta(days=days)


    return None

print(calculate_due_date("explicit","Monday"))