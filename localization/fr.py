# Return strings for French language
# This can be used as a template for other languages, too.
# Note that in French, days and months are not capitalized


def localize(today_weekday, today_day, today_month):
    # Set up dictionaries for month and weekdays
    weekdays = {
        0: "lundi",
        1: "mardi",
        2: "mercredi",
        3: "jeudi",
        4: "vendredi",
        5: "samedi",
        6: "dimanche"
    }

    months = {
        1: "janvier",
        2: "février",
        3: "mars",
        4: "avril",
        5: "mai",
        6: "juin",
        7: "juillet",
        8: "août",
        9: "septembre",
        10: "octobre",
        11: "novembre",
        12: "décembre"
    }

    weekday = weekdays[today_weekday].capitalize()
    formatted_date = "{0} {1}".format(months[today_month], str(today_day))

    return weekday, formatted_date
