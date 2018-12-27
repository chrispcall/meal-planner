import datetime


def get_all_dates(weeks=0):
    """Returns a list of all of the dates for the next week, starting with the most recent coming Sunday.
       Pass in direction of 'past or 'future' and how many weeks you'd like to move forward or backward."""
    if weeks == 'favicon.ico':
        print('Fav!')
        pass
    weeks = int(weeks)
    d = datetime.date.today()
    # calculate the dates for the Sunday of current week (start of the week)
    if weeks == 0:
        while d.weekday() != 6:
            d -= datetime.timedelta(1)
    elif weeks < 0:
        # calculate the dates for the coming Sunday
        weeks = -weeks
        d -= datetime.timedelta(7*weeks)
        while d.weekday() != 6:
            d -= datetime.timedelta(1)
    else:
        # calculate the dates for the previous Sunday
        d += datetime.timedelta(7*weeks)
        while d.weekday() != 6:
            d -= datetime.timedelta(1)

    all_week_dates = []
    # print out the dates for each day next week, starting with Sunday.
    for i in range(7):
        all_week_dates.append(d.strftime("%m-%d"))
        d += datetime.timedelta(1)
    return all_week_dates

