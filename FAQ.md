# Frequently Asked Questions

Nobody has actually asked any questions, but these are the the questions I imagine people will have.

### Can I send a grayscale image to a red or yellow display?

Yes! If you don't use the `--red` or `--yellow` arguments, it will make a grayscale image on the e-paper display, even if you have a red or yellow display.

### What if I send a --red or --yellow command to a grayscale display?

I have no idea what would happen. I have only been able to test this on a red display. Whatever the results are, I imagine they will be pretty unexpected.

### What image format should I use?

PNG files at 640x384 are recommended. JPG files will work, but the way the Python image library converts to monocolor bitmaps generally does not handle the compression artifacts from JPG files very well. Text will generally have jagged halos around it.

Images larger than 640x384 will be scaled down, but will make the `--date-location detect` mode ineffective, as usually a single pixel will be interpolated to a slightly different color.

Additionally, higher contrast images tend to produce better results. Red screens will tend to pick up some color from bright yellows in images and may not come out as expected.

### How do I make it run every day with a new image?

The script itself does not have this feature, but you can place the command in your crontab to run at a specific time every day. Using the `--image shuffle` argument will cause it to randomly pick a new image each day.

### Can I use a different size screen?

The drivers __epd7in5.py__ and __epd7in5b.py__ expect the screen to be 640x384. The script itself references the sizes provided by those drivers, so you could conceivably alter the script to load different drivers. I only have the 7.5" display so I cannot test anything other than this size.

### Can you add [feature]?

Maybe, but I wouldn't count on it. I'm not a programmer by trade, so this was always intended to be a small hobby project. There are a few other features I may add, but I'm not going to promise anything.