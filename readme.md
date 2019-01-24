# Raspberry Pi Daily Calendar

When I was growing up, my dad always got a daily _Far Side_ desk calendar, which showed the date and a  comic. While such analog calendars are still available, I've decided to replicate the idea with my own images on a Raspberry Pi connected to a 7.5 inch Waveshare e-ink display. This will work on any Raspberry Pi that can connect to the e-ink display, and will work with any 7.5 inch Waveshare e-ink display (black and white, 3 colors with red, or 3 colors with yellow).

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

## Authors

* Ben Mooney - [ben-etc](https://github.com/ben-etc)

Consider supporting my work by [buying me a coffee on Ko-Fi](https://ko-fi.com/benmooney) or with a donation through my paypal.me link at [paypal.me/benmooney5](https://paypal.me/benmooney5).

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

The e-paper libraries included with this software are copyright Waveshare and distributed with permission as indicated in the associate files.