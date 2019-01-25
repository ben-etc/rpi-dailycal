import argparse
import os
from PIL import Image
import createBitmaps as cb
import epd7in5
import epd7in5b

# Begin parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True,
                    help="The image to be converted. PNG file preferred")
parser.add_argument("-r", "--red", action="store_true",
                    help="Enables red color mode for red screens.")
parser.add_argument("-y", "--yellow", action="store_true",
                    help="Enables yellow color mode for yellow screens.")
parser.add_argument("--no-border", action="store_true",
                    help="Disables the border on the date box.")
parser.add_argument("--margin", 
                    help="Sets the margin on the text in the datebox.")
parser.add_argument("--date-location", 
                    help="topleft | topright | bottomleft | bottomright | manual | detect")
parser.add_argument("--date-coords",
                    help="Manually sets the location of the date box.")
parser.add_argument("--font", help="Select a specific font.")

args = parser.parse_args()

# Validate the argument selection. Certain options are mutally exclusive.

# Validate color selection
if args.red == True and args.yellow == True:
    print("Both red and yellow screencolor arguments were selected!")
    print("Please select only --red or --yellow.")
    print("Script will now exit.")
    exit()

if args.input != "clear":
    try:
        img = Image.open("images/{0}".format(args.input))
    except:
        print("Unable to open {0}".format(args.input))


if args.red == True:
    screencolor = "red"
elif args.yellow == True:
    screencolor = "yellow"
else:
    screencolor = "grayscale"

# Set up the optional keyword arguments for convert_bitmap and add_dateboxes
convert_kwargs = {}
datebox_kwargs = {}
if args.date_location is not None:
    convert_kwargs.update({"date_location":args.date_location})
if args.date_coords is not None:
    convert_kwargs.update({"date_coords":args.date_coords})
if args.no_border == True:
    datebox_kwargs.update({"border":False})
if args.margin is not None:
    datebox_kwargs.update({"margin":args.margin})
if args.font is not None:
    datebox_kwargs.update({"fontname":args.font})

# Generate bitmaps. The colorbit variable is generated even for grayscale, but it is dummy data
if args.input != "clear":
    blackbit, colorbit, secret_pixel = cb.convert_bitmap(img, screencolor, **convert_kwargs)
    blackbit, colorbit = cb.add_dateboxes(screencolor, blackbit, colorbit, secret_pixel, **datebox_kwargs)

# Grayscale and red / yellow have different routines.

if screencolor == "grayscale":
    epd = epd7in5.EPD()
    if args.input == "clear":
        epd.init()
        epd.Clear(0xFF)
    else:
        buffer = epd.getbuffer(blackbit)
        epd.init()
        epd.display(buffer)
    epd.sleep()

else:
    # Do the things for red / yellow. They follow the same process.
    epd = epd7in5b.EPD()
    if args.input == "clear":
        epd.init()
        epd.Clear(0xFF)
    else:
        blackbuff = epd.getbuffer(blackbit)
        colorbuff = epd.getbuffer(colorbit)
        epd.init()
        epd.display(blackbuff, colorbuff)
    epd.sleep()