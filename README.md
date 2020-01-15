# VirtualVideo
VirtualVideo allows you to write simple programs that feed images to a v4l2loopback device.
## Prerequisites 
* [v4l2loopback](https://github.com/umlaeute/v4l2loopback)
* ffmpeg 
## Example
Checkout the [example](examples/showFish.py) for the code.

To run the example:
```
$ sudo modprobe v4l2loopback
$ python3 showFish.py
```

## F.A.Q.:
* Check if the user is allowed to access the device, otherwise change permissions
* Use following code to check if ffmpeg is working properly
```$ ffmpeg -loop 1 -re -i foo.jpg -f v4l2 -vcodec rawvideo -pix_fmt yuv420p /dev/video1 ```
* If not checkout the v4l2loopback github and wiki
* If the image is distorted try unloading and loading the module, maybe check ```$cat /sys/devices/virtual/video4linux/video69/format``` for the format you should use

## Credits
This Module relies heavily on [v4l2loopback](https://github.com/umlaeute/v4l2loopback) 
and [ffmpeg-python](https://github.com/kkroening/ffmpeg-python/)

The fish.jpg used in the examples is ["Goldfish" by Melinda van den Brink](https://www.flickr.com/photos/11750887@N04/4916553401)
