# These functions modify an RGB image into the bitmaps used by the e-paper screen

from importlib import import_module
from PIL import Image, ImageFont, ImageColor, ImageDraw
import datetime


def convert_bitmap(rgb_image, screencolor, date_location="bottomright", date_coords=(0, 0)):
    imgwidth = rgb_image.width
    imgheight = rgb_image.height
    if screencolor != "grayscale":
        # Create an empty grayscale image for the color channel
        colorscale = Image.new("L", (imgwidth, imgheight), 255)
        colorscale_access = colorscale.load()
    # Create an empty grayscale image that will be the black channel
    grayscale = Image.new("L", (imgwidth, imgheight), 255)
    grayscale_access = grayscale.load()
    secret = (0, 0, 255, 255)

    # The logic for everything but topright will put the box out of bounds, but this is corrected in addDateboxes once the box is dynamically generated.
    if date_location == "detect":
        # This will be used to figure out where the calendar will be placed on the image
        secret_pixel = (-1, -1)
    elif date_location == "topleft":
        secret_pixel = (0, 0)
    elif date_location == "bottomleft":
        secret_pixel = (0, imgheight)
    elif date_location == "topright":
        secret_pixel = (imgwidth, 0)
    elif date_location == "bottomright":
        secret_pixel = (imgwidth, imgheight)
    elif date_location == "manual":
        secret_pixel = date_coords
    else:
        print("Date location {0} is not a valid choice. Defaulting to bottomright".format(
            date_location))
        secret_pixel = (imgwidth, imgheight)

    mode = rgb_image.mode
    pixelaccess = rgb_image.load()

    if screencolor == "red" or screencolor == "yellow":
        # Go through the original image pixel by pixel and separate out red and an average of blue/green channels

        # Create a color and black bitmap if the screencolor is not grayscale
        print("Begin processing image per-pixel")
        for y in range(imgheight):
            for x in range(imgwidth):
                if mode == "RGB":
                    r, g, b = pixelaccess[x,y]
                    a = 255  # Alpha is always totally opaque on an RGB image
                elif mode == "RGBA":
                    r, g, b, a = pixelaccess[x,y]
                    # The next two lines fade out images approximating alpha transparency
                    inverse_alpha = 255 - a
                    r, g, b = (r + inverse_alpha), (g +
                                                    inverse_alpha), (b + inverse_alpha)

                if (r, g, b, a) == secret and secret_pixel == (-1, -1):
                    secret_pixel = (x, y)

                # Math for red screens
                if screencolor == "red":
                    # Average the blue and green channels to output it to the black channel
                    avg = int((g + b) / 2)
                    color_value = r - max(g, b)
                    colorscale_access[x,y] = 255 - color_value
                    grayscale_access[x,y] = avg

                # Math for yellow screens
                elif screencolor == "yellow":
                    # Average the red and green channels to try to get a yellow value
                    yellow_avg = int(((r-b) + (g-b)) / 2)
                    yellow_avg = yellow_avg - max(r - g, g - r)
                    gray_avg = int((r + g + b) / 3)
                    colorscale_access[x, y] = 255 - yellow_avg
                    grayscale_access[x, y] = gray_avg

        # Convert the two grayscale images to single color bitmaps
        color_bitmap = colorscale.convert("1")
        black_bitmap = grayscale.convert("1")

    elif screencolor == "grayscale":
        black_bitmap = rgb_image.convert("1")
        color_bitmap = None
        # If the date location is "detect", we still need to parse each pixel to find the secret pixel.
        # I realize this is repeating an awful lot of code up above. This should be refacroted later.
        if date_location == "detect":
            print("Looking for the secret pixel")
            for y in range(imgheight):
                for x in range(imgwidth):
                    if mode == "RGB":
                        r, g, b = pixelaccess[x,y]
                        a = 255
                    elif mode == "RGBA":
                        r, g, b, a = pixelaccess[x,y]

                    if (r, g, b, a) == secret and secret_pixel == (-1, -1):
                        secret_pixel = (x, y)

    else:
        print("{0} is not a valid screencolor!".format(screencolor))
        # Return dummy values
        black_bitmap = None
        color_bitmap = None
    if secret_pixel == (-1, -1):
        # Default the calendar to the bottom right if it hasn't been detected.
        secret_pixel = (imgwidth, imgheight)
    print("Secret pixel: {0}".format(secret_pixel))
    return black_bitmap, color_bitmap, secret_pixel

# This function is largely used for testing. It will save a file a combined output to use as a preview


def merge_bitmaps(black_bitmap, color_bitmap, screencolor="red"):
    # Define colors that will be used
    color = ImageColor.getcolor(screencolor, "RGB")
    black = ImageColor.getcolor("black", "RGB")
    white = ImageColor.getcolor("white", "RGB")

    outputImage = Image.new(
        "RGB", (color_bitmap.width, color_bitmap.height), white)
    blackaccess = black_bitmap.load()
    coloraccess = color_bitmap.load()
    outputaccess = outputImage.load()
    # Map each pixel to color or black
    for y in range(color_bitmap.height):
        for x in range(color_bitmap.width):
            colorcheck = coloraccess[x,y]
            blackcheck = blackaccess[x,y]

            if colorcheck == 0:
                outputaccess[x,y] = color
            elif blackcheck == 0:
                outputaccess[x,y] = black

    return outputImage

# The following is en.py hard coded into the program as a failsafe


def localize_failsafe(today_weekday, today_day, today_month):
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


def add_dateboxes(screencolor, black_bitmap, color_bitmap,
                  secret_pixel, border=True, margin=5,
                  fontname="LeagueSpartan-Bold.otf",
                  holiday_file=None, language="en"):
    today = datetime.datetime.now()

    # Set up the holiday_text, holiday_width, and holiday_height variables ahead of time.
    holiday_text = None
    holiday_width = 0
    holiday_height = 0
    # This block will add an extra line with a holiday loaded from a txt file
    # This block will not run if no txt file was supplied.
    if holiday_file is not None:
        holiday_font = ImageFont.truetype("./fonts/Linden Hill.otf", 18)
        try:
            with open(holiday_file, "r") as holiday_list:
                holidays = holiday_list.read().splitlines(True)
                for date in holidays:
                    # Don't parse commented or lines without ":"
                    if date[0] == "#" or ":" not in date:
                        day = [0, 0]  # This is sort of an ugly hack
                    else:
                        day = date.split(":")[0]
                        holiday = date.split(":")[1].rstrip()
                        day = day.split("-")
                    if today.month == int(day[0]) and today.day == int(day[1]):
                        holiday_text = holiday
                        holiday_width = holiday_font.getsize(
                            holiday_text)[0] + (margin * 2)
                        holiday_height = holiday_font.getsize(holiday_text)[
                            1] + margin
        except:
            print("Unable to load holiday file {0}".format(holiday_file))
            holiday_text = "Unable to load holiday file {0}".format(
                holiday_file)
            holiday_width = holiday_font.getsize(
                holiday_text)[0] + (margin * 2)
            holiday_height = holiday_font.getsize(holiday_text)[1] + margin
    indent = margin + 20
    font = ImageFont.truetype("./fonts/{0}".format(fontname), 32)
    print("Importing language {0}".format(language))
    try:
        lang = import_module("localization.{0}".format(language))
        day_of_week, formatted_date = lang.localize(
            today.weekday(), today.day, today.month)
    except:
        print(
            "Error importing language {0}. Using Built-in English as fallback".format(language))
        day_of_week, formatted_date = localize_failsafe(
            today.weekday(), today.day, today.month)
    width = max((margin * 2 + font.getsize(day_of_week)[0]),
                (margin + indent + font.getsize(formatted_date)[0]),
                holiday_width)
    newline = margin + font.getsize(day_of_week)[1]
    holiday_line = margin + font.getsize(formatted_date)[1] + newline
    height = newline + margin + \
        font.getsize(formatted_date)[1] + holiday_height
    black_date = Image.new("1", (width, height), 1)
    black_draw = ImageDraw.Draw(black_date)
    # Recalculate the secret_pixel to avoid going out of bounds
    x = min(black_bitmap.width - width, secret_pixel[0])
    y = min(black_bitmap.height - height, secret_pixel[1])
    secret_pixel = (x, y)
    if screencolor != "grayscale":
        color_date = Image.new("1", (width, height), 1)
        color_draw = ImageDraw.Draw(color_date)
        color_draw.text((margin, margin), day_of_week, fill=0, font=font)
        color_draw.text((indent - 2, newline + 2),
                        formatted_date, fill=0, font=font)  # Shadow
        color_draw.text((indent, newline), formatted_date, fill=1, font=font)
        if border == True:
            black_draw.rectangle(
                (0, 0, black_date.width, black_date.height), fill=1, outline=0, width=2)
        black_draw.text((margin - 2, margin + 2), day_of_week,
                        fill=0, font=font)  # Shadow
        black_draw.text((margin, margin), day_of_week, fill=1, font=font)
        black_draw.text((indent, newline), formatted_date, fill=0, font=font)
        if holiday_text is not None:
            black_draw.text((margin, holiday_line), holiday_text, fill=0,
                            font=holiday_font)
        color_bitmap.paste(color_date, secret_pixel)
        black_bitmap.paste(black_date, secret_pixel)

    elif screencolor == "grayscale":
        if border == True:
            black_draw.rectangle(
                (0, 0, black_date.width, black_date.height), fill=1, outline=0, width=2)
        black_draw.text((margin, margin), day_of_week, fill=0, font=font)
        black_draw.text((indent, newline), formatted_date, fill=0, font=font)
        if holiday_text is not None:
            black_draw.text((margin, holiday_line), holiday_text, fill=0,
                            font=holiday_font)
        black_bitmap.paste(black_date, secret_pixel)
        color_bitmap = None
    return black_bitmap, color_bitmap


def fix_size(image, max_size, letterbox_color="black"):
    max_width = max_size[0]
    max_height = max_size[1]
    # First, check to see if width or height are too large
    if image.width > max_width or image.height > max_height:
        print("Image too large: shrinking down")
        image.thumbnail((max_width, max_height), Image.ANTIALIAS)

    # The image should not be too large now, but still may not fill the whole screen
    if image.width != max_width or image.height != max_height:
        print("Image not correct aspect ratio. Adding border")
        # Create a blank canvas to paste the new image onto.
        canvas = Image.new(
            image.mode, (max_width, max_height), letterbox_color)
        # Figure out where to paste the image by finding the remaining space and dividing by 2
        x = max(0, int((max_width - image.width) / 2))
        y = max(0, int((max_height - image.height) / 2))
        canvas.paste(image, (x, y))
        image = canvas

    return image
