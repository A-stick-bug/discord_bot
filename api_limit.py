from datetime import datetime
from replit import db


def update_user_stats(user):
    time = list(map(int,(datetime.today().strftime('%Y-%m-%d').split("-"))))  # [year, month, day]
    base = {"weather": 0, "limit_exceeded": [], "previous_time": time}
    
    if user not in db.keys():  # create stats for user
        db[user] = {"weather": 0, "limit_exceeded": [], "previous_time": time}
        
    # if a day has passed, reset user's api use count
    prev_time = db[user]["previous_time"]
    if (time[0] > prev_time[0] or time[1] > prev_time[1]) or (time[2] > prev_time[2]):  
        db[user]["weather"] = 0
        db[user]["previous_time"] = time

    # daily weather api requests limit for regular users
    elif db[user]["weather"] > 3 and user not in db["unlimited_api"]:
        if not db[user]["limit_exceeded"] or db[user]["limit_exceeded"][-1] != time:
            db[user]["limit_exceeded"].append(time)
        return "limit exceeded"
        
    else:  # update stats for user
        db[user]["weather"] += 1
        db[user]["previous_time"] = time

    return "updated stats"
