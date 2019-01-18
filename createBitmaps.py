# These functions modify an RGB image into the bitmaps used by the e-paper screen

from PIL import Image, ImageFont, ImageColor, ImageDraw
import datetime

def convertBitmap(RGBImage):
    imgwidth = RGBImage.width
    imgheight = RGBImage.height
    colorscale = Image.new("L", (imgwidth,imgheight), 255)  # Create an empty grayscale image for the color channel
    grayscale = Image.new("L", (imgwidth,imgheight), 255)  # Create an empty grayscale image that will be the black channel
    secret = (0, 0, 255, 255)
    secretPixel = (0,0) # This will be used to figure out where the calendar will be placed on the image
    
    mode = RGBImage.mode
    # Go through the original image pixel by pixel and separate out red and an average of blue/green channels
    for y in range(imgheight):
        for x in range(imgwidth):
            if mode == "RGB":
                r, g, b = RGBImage.getpixel((x,y)) # Gets the RGB values of the pixel at x,y
                a = 255 # Alpha is always totally opaque on an RGB image
            elif mode == "RGBA":
                r, g, b, a = RGBImage.getpixel((x,y)) # Gets the RGBA values of the pixel at x,y.
                # The next two lines fade out images approximating alpha transparency
                inverseAlpha = 255 - a
                r, g, b = (r + inverseAlpha), (g + inverseAlpha), (b + inverseAlpha)
            
            if (r, g, b, a) == secret and secretPixel == (0,0):
                secretPixel = (x,y)
            avg = int((g + b) / 2) # Average the blue and green channels to output it to the black channel
            colorvalue = r - avg 
            colorscale.putpixel((x,y), (255 - colorvalue))
            grayscale.putpixel((x,y), avg)
    
    # Convert the two grayscale images to single color bitmaps
    colorbitmap = colorscale.convert("1")
    blackbitmap = grayscale.convert("1")
    colordate, blackdate = getDateboxes()
    colorbitmap.paste(colordate, secretPixel)
    blackbitmap.paste(blackdate, secretPixel)
    print("Secret pixel: {}".format(secretPixel))
    return colorbitmap, blackbitmap

# This function is largely used for testing. It will save a file a combined output to use as a preview
def mergeBitmaps(colorbitmap, blackbitmap, screencolor = "red"):
    # Define colors that will be used
    color = ImageColor.getcolor(screencolor, "RGB")
    black = ImageColor.getcolor("black", "RGB")
    white = ImageColor.getcolor("white", "RGB")
    
    outputImage = Image.new("RGB", (colorbitmap.width, colorbitmap.height), white)
    
    # Map each pixel to color or black
    for y in range(colorbitmap.height):
        for x in range(colorbitmap.width):
            colorcheck = colorbitmap.getpixel((x,y))
            blackcheck = blackbitmap.getpixel((x,y))
            
            if colorcheck == 0:
                outputImage.putpixel((x,y), color)
            elif blackcheck == 0:
                outputImage.putpixel((x,y), black)
    
    return outputImage

def getDateboxes(border = True, margin = 5):
	today = datetime.datetime.now()
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
	
	indent = margin + 20
	font = ImageFont.truetype("./fonts/LeagueSpartan-Bold.otf", 32)
	dayofweek = weekdays[today.weekday()]
	formattedDate = "{} {}".format(months[today.month], today.day)
	width = max( (margin * 2 + font.getsize(dayofweek)[0]), (margin + indent + font.getsize(formattedDate)[0]))
	newline = margin + font.getsize(dayofweek)[1]
	height = newline + margin + font.getsize(formattedDate)[1]
	
	colordate = Image.new("1", (width, height), 1)
	blackdate = Image.new("1", (width, height), 1)
	colorDraw = ImageDraw.Draw(colordate)
	blackDraw = ImageDraw.Draw(blackdate)
	
	

	colorDraw.text((margin, margin), dayofweek, fill = 0, font = font)
	colorDraw.text((indent - 2, newline + 2), formattedDate, fill = 0, font = font) # Shadow
	colorDraw.text((indent, newline), formattedDate, fill = 1, font = font)
	if border == True:
		blackDraw.rectangle((0,0, blackdate.width, blackdate.height), fill = 1, outline = 0, width = 2)
	blackDraw.text((margin - 2, margin + 2), dayofweek, fill = 0, font = font) # Shadow
	blackDraw.text((margin, margin), dayofweek, fill = 1, font = font)
	blackDraw.text((indent, newline), formattedDate, fill = 0, font = font)
	
	return colordate, blackdate