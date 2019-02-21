# Return strings for German language
# This can be used as a template for other languages, too.


def localize(today_weekday, today_day, today_month):
    # Set up dictionaries for month and weekdays
    weekdays = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
    }

    months = {
        1: "Januar",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember"
    }

    weekday = weekdays[today_weekday]
    formatted_date = "der {0}.{1}".format(str(today_day),months[today_month])

    return weekday, formatted_date
