# Return strings for English language
# This can be used as a template for other languages, too.


def localize(today_weekday, today_day, today_month):
    # Set up dictionaries for month and weekdays
    weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    weekday = weekdays[today_weekday]
    formatted_date = "{0} {1}".format(months[today_month], str(today_day))

    return weekday, formatted_date
