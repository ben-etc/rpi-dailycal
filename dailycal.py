__version__ = "1.2"

import argparse
import sys
from PIL import Image
import createBitmaps as cb
import shuffler

# Begin parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image",
                    help="The image to be converted. PNG file preferred")
parser.add_argument("-v", "--version", action="store_true",
                    help="Print version, then exit.")
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
parser.add_argument("--date-coords", nargs="+", type=int,
                    help="Manually sets the location of the date box.")
parser.add_argument("--font", help="Select a specific font.")
parser.add_argument("--letterbox-color",
                    help="Sets the color of letterbox if the image is too small")
parser.add_argument("--holiday-file",
                    help="Location of txt file containing holidays.")
parser.add_argument("--language",
                    help="Two letter language code for localization, e.g. 'en'")

args = parser.parse_args()

# If --version is supplied, print __version__ and exit
if args.version == True:
    print("Daily Pi Calendar version {0}".format(__version__))
    sys.exit(0)
# If --version is not supplied, load the drivers.
# This way, the SPIDEV module does not need to be loaded on test systems
else:
    import epd7in5
    import epd7in5b
# Validate the argument selection.

# Check to see if an --image argument was supplied. If not, exit
if args.image is None:
    print("No image name was supplied. Program will now exit.")
    sys.exit(1)
# Validate color selection
if args.red == True and args.yellow == True:
    print("Both red and yellow screencolor arguments were selected!")
    print("Please select only --red or --yellow.")
    print("Script will now exit.")
    sys.exit(2)

if args.image != "clear":
    if args.image == "shuffle":
        input_image = shuffler.shuffle_images()
        print("Input image detected as {0}".format(input_image))
    else:
        input_image = args.image
    try:
        img = Image.open("images/{0}".format(input_image))
    except:
        print("Unable to open {0}".format(input_image))
    # Check to make sure the image is the right size, otherwise resize it.
    epaper_width = epd7in5.EPD_WIDTH
    epaper_height = epd7in5.EPD_HEIGHT
    if args.letterbox_color is None:
        letterbox = "black"
    else:
        letterbox = args.letterbox_color
    img = cb.fix_size(img, (epaper_width, epaper_height), letterbox)

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
    convert_kwargs.update({"date_location": args.date_location})
if args.date_coords is not None:
    coords = tuple(args.date_coords)
    convert_kwargs.update({"date_coords": args.date_coords})
if args.no_border == True:
    datebox_kwargs.update({"border": False})
if args.margin is not None:
    datebox_kwargs.update({"margin": args.margin})
if args.font is not None:
    datebox_kwargs.update({"fontname": args.font})
if args.holiday_file is not None:
    datebox_kwargs.update({"holiday_file": args.holiday_file})
if args.language is not None:
    datebox_kwargs.update({"language": args.language})

# Generate bitmaps. The colorbit variable is generated even for grayscale, but it is dummy data
if args.image != "clear":
    blackbit, colorbit, secret_pixel = cb.convert_bitmap(
        img, screencolor, **convert_kwargs)
    blackbit, colorbit = cb.add_dateboxes(
        screencolor, blackbit, colorbit, secret_pixel, **datebox_kwargs)

# Grayscale and red / yellow have different routines.

# Send screen commands for graysale
if screencolor == "grayscale":
    epd = epd7in5.EPD()
    if args.image == "clear":
        try:
            epd.init()
            epd.Clear(0xFF)
        except:
            print("Error writing buffer. Putting display to sleep")
            epd.sleep()
    else:
        try:
            blackbit.save("buffer.bmp")
            # Saving the black bitmap and reloading it fixes a blank date box bug
            # I don't know what causes it, but this fixes it.
            new_blackbit = Image.open("buffer.bmp")
            blackbuffer = epd.getbuffer(new_blackbit)
            epd.init()
            epd.display(blackbuffer)
        except:
            print("Error writing buffer. Putting display to sleep")
    epd.sleep()

else:
    # Send screen commands for color screens. Both red and yellow have the same routine.
    epd = epd7in5b.EPD()
    if args.image == "clear":
        try:
            epd.init()
            epd.Clear(0xFF)
        except:
            print("Error writing buffer. Putting display to sleep")
            epd.sleep()
    else:
        try:
            blackbuff = epd.getbuffer(blackbit)
            colorbuff = epd.getbuffer(colorbit)
            epd.init()
            epd.display(blackbuff, colorbuff)
        except:
            print("Error writing buffer. Putting display to sleep")
            epd.sleep()
    epd.sleep()
