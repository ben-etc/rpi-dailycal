# Return strings for Spanish language
# This can be used as a template for other languages, too.


def localize(today_weekday, today_day, today_month):
    # Set up dictionaries for month and weekdays
    # Note that in Spanish, months and days are not capitalized by default.
    weekdays = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo"
    }

    months = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre"
    }

    weekday = weekdays[today_weekday].capitalize()
    formatted_date = "{0} de {1}".format(str(today_day), months[today_month])

    return weekday, formatted_date
