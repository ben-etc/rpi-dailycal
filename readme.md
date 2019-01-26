# Raspberry Pi Daily Calendar

When I was growing up, my dad always got a daily _Far Side_ desk calendar, which showed the date and a  comic. While such analog calendars are still available, I've decided to replicate the idea with my own images on a Raspberry Pi connected to a 7.5 inch Waveshare e-ink display. This will work on any Raspberry Pi that can connect to the e-paper display, and will work with any 7.5 inch Waveshare e-ink display (black and white, 3 colors with red, or 3 colors with yellow).

## What this _is_

Simply put, this program takes a .png or .jpg file and converts it into a format useable by the Waveshare 7.5 inch e-paper display. It then adds the current date on top of the image to be displayed as a calendar. It is designed to bypass the need to manually construct your own monocolor bitmaps required by the display, which can be tricky particularly if you are using one of the 3-color displays. Once it is set up, you should be able to simply supply it with the name of an image and it will do the rest, with little to no image manipulation on your part.

## What this is _not_

This program is _not_ designed to sync calendar appointments, task lists, weather, or any other information. The reason behind this is that — aside from syncing its clock over the internet due to the lack of persistent clock — it should be useable in an environment without a network connection. Some people and offices are okay with random Raspberry Pi devices accessing the wireless network, but many are not comfortable with this situation. The program itself needs no internet connection to run as long as the current date is correct. If you're looking for something to sync with your Google calendar or task list, this isn't it.

## Getting Started

This software requires a Raspberry Pi 2, Raspberry Pi 3, or Raspberry Pi Zero and a 7.5 inch Waveshare e-ink display. The code will only work with the 7.5 inch displays, as the code provided by Waveshare that interacts with the screen expects a specific image resolution.

### Prerequisites

The Waveshare display requires several libraries. Per the Waveshare manual, the following needs to be installed.

```bash
sudo apt-get install python3 python3-pip python-imaging libopenjp2-7-dev
sudo pip3 install spidev
sudo pip3 install RPi.GPIO
sudo pip3 install Pillow
```

Additionally, if you are not running the Raspberry Pi as the default user __Pi__, you will need to make sure your account is a member of the same groups as __Pi__. Notably there are groups which allow access to spidev and GPIO. If you just want to get started as soon as possible, it's advised that you run this software as the user __Pi__.

## Usage

##### Note: this section is currently changing rapidly as the frontend script is written and new features are added.

The program can be invoked with `python3 dailycal.py`. The only required argument is `--image`, which points the script to the image you would like to use.

Example:

```bash
python3 dailycal.py --image example.png
```

The program assumes by default that you are using a single color, e.g., grayscale screen. The arguments `--red` and `--yellow` should be used in order to indicate that you are using that type of screen:

```bash
python3 dailycal.py --image example.png --red
```

There are a number of optional arguments that control the location of the date box, fonts, etc. All the following examples are valid:

```bash
python3 dailycal --image example.png --red --date-location topright --no-border
python3 dailycal --image example.png --yellow --date-location manual --date-coords 45 20
python3 dailycal --image example.png --red --margin 10 --font arial.ttf
```

## About --date_location and "the secret pixel"

By default, the date is placed in the bottom right. However, using the `--date-location detect`argument, the script looks for a "secret pixel", which is the _first_ instance of a totally blue pixel (0, 0, 255) in the image. This allows a user preparing images to simply place one blue pixel to represent the upper left bound of the date box. If it does not find such a pixel, it defaults to the upper left of the image.

If this behavior is not desired, either because you are using an image with solid blue pixels or simply to avoid having to manually place this pixel on your image, the date box can be placed with any of the following `--date-location` arguments:

`topleft` place the date box in the upper left corner

`topright` place the date box in the upper right corner

`bottomleft` place the date box in the lower left corner

`bottomright` place the date box in the lower right corner

`detect` place the date box at the secret pixel, as described above.

`manual` uses the (x, y) coordinates provided by the `--date_coords` argument. Note that (0, 0) is the upper left of the image; increasing values for x move to the right, and increasing values for y move down.

The script is also designed to never allow the date box to extend off the side of the image, so don't worry too much about figuring out the size of the date box for your manual placement.

## About --image

The `--image` argument will automatically look for the name of that image in the images/ directory. Because the program can run with either .jpg or .png images, you will need to make sure you include the extension. `python3 dailycal.py --image hello.png` looks for the image __images/hello.png__.

Although the image can be in .jpg format, this is discouraged, as the image converter does some unexpected things with .jpg compression artifacts. Images work best at 640x384, but large images will be resized, and small images will be pasted onto a border. 640x384 images are therefore recommended, but any size image should work.

Supplying the argument `--image clear` will cause the display to clear to white.

Supplying the argument `--image shuffle` will pick the next image in the pre-shuffled list, or generate a new shuffled list if the list is empty. Every .jpg and .png file in the __images/__ directory will be shuffled together into a list.

## About --font

The `--font` argument will look for fonts in the font/ directory. Additional fonts can be installed into this directory, and it _does not_ look for fonts elsewhere on the system. `python3 dailycal.py --image hello.png --font arial.ttf` will attempt to use __fonts/arial.ttf__. If Arial is _not_ in that directory, the script will fail even if Arial is elsewhere on the system. Just like with images, the extension must be supplied, as it can use .ttf and .otf fonts.

## Authors

* Ben Mooney - [ben-etc](https://github.com/ben-etc)

Consider supporting my work by [buying me a coffee on Ko-Fi](https://ko-fi.com/benmooney) or with a donation through my paypal.me link at [paypal.me/benmooney5](https://paypal.me/benmooney5).

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details

The e-paper libraries included with this software are copyright Waveshare and distributed with permission as indicated in the associate files.

The font League Spartan is from the [League of Movable Type](https://www.theleagueofmoveabletype.com) and can be found on GitHub at [https://github.com/theleagueof/league-spartan](github.com/theleagueof/league-spartan). It is distributed under the OFL license included in the fonts/ directory.