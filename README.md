# VirtualVideo
VirtualVideo allows you to write simple programs that feed images to a v4l2loopback device.
## Prerequisites 
* [v4l2loopback](https://github.com/umlaeute/v4l2loopback)
* ffmpeg 

## Guide
Install virtualvideo with: 
```pip3 install --user virtualvideo```

Install ffmpeg(preferably with your systems packagemanager) and v4l2loopback. Installing v4l2loopback can be tricky and i suggest using ```dkms``` to install/build it. (If you're using Arch-Linux theres an AUR Package for you: [v4l2loopback-dkms](https://aur.archlinux.org/packages/v4l2loopback-dkms/)).

## Example
[showFish.py](examples/showFish.py) shows how to use the virtualvideo package.

### Running the Example
To run the example:
```
$ sudo modprobe v4l2loopback video_nr=XX exclusive_caps=1
$ cd examples
$ python3 showFish.py
```
Then you should be able to open/view the webcam for example with vlc (or on webcamtest.com).
You then should see a red goldfish getting blurred and unblurred. 
See [example/README.md](examples/README.md) for a gif.

## Errorhandling:
* Check if the user is allowed to access the device, otherwise change permissions of ```/dev/videoXX```

* Use following code to check if ffmpeg is working properly
```$ ffmpeg -loop 1 -re -i foo.jpg -f v4l2 -vcodec rawvideo -pix_fmt yuv420p /dev/videoXXX ```

* If not checkout the v4l2loopback github and wiki

* If the image is distorted try unloading and loading the module, 
maybe check ```$cat /sys/devices/virtual/video4linux/video69/format``` for the format you should use

* If you want to change the format or the pixel format unload the module

* If you cannot unload the module, check processes that access /dev/videoXX ($ fuser /dev/videoXX) and kill them

* If you get an pixel_format not supported error, try yuyv422 as pixelformat e.g.: ```fvd.init_output(...,pix_fmt="yuyv422")``` or ```$ ffmpeg -loop 1 -re -i foo.jpg -f v4l2 -vcodec rawvideo -pix_fmt yuyv422 /dev/videoXXX ```

## Credits
This Module relies heavily on [v4l2loopback](https://github.com/umlaeute/v4l2loopback) 
and [ffmpeg-python](https://github.com/kkroening/ffmpeg-python/)

The fish.jpg used in the examples is ["Goldfish" by Melinda van den Brink](https://www.flickr.com/photos/11750887@N04/4916553401)
