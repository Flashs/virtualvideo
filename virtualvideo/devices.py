"""
v2l is an easy way to feed images to the v4l2loopback device
"""
import time

import ffmpeg
import numpy as np

class VideoSource():
    """
    Abstract class of a VideoSource

    Check WebcamSource for an example

    Syntax:
        class MyVideoSource(VideoSource):
            ...
    """
    def img_size(self):
        """Should return the size of the input image as a tuple e.g. return (1280,720)"""
        raise NotImplementedError("Please overwrite")

    def fps(self):
        """Should return the FPS/or how fast an image can be generated"""
        raise NotImplementedError("Please overwrite")

    def fmt(self):
        """
        Should return the ffmpeg format of the image.
        Opencv uses bgr24 (8 bits per color, blue,green,red), rgb24 is common too
        """
        return "bgr24"

    def generator(self):
        """Should return an generator which yields the next image"""
        raise NotImplementedError("Please overwrite")


class FakeVideoDevice():
    """Takes an input and feeds a v4l2loopback device"""
    VIDEODEV_STR = "/dev/video{}"

    def __init__(self):
        self.vid_source = None
        self.input = None
        self.output = None
        self.last_frame_time = 0
        self.running = False
        self.ffmpeg_proc = False

    def init_input(self, vid_source):
        """Initialises the input for the device, the Videosource holds all necessary information"""
        self.vid_source = vid_source
        #input over stdin, format are raw frames, with pixformat,size and fps
        self.input = ffmpeg.input("pipe:0",
                                  format="rawvideo",
                                  pix_fmt=vid_source.fmt(),
                                  video_size=vid_source.img_size(),
                                  framerate=vid_source.fps())

    def init_output(self, dev_nr, camx=1280, camy=720, fps=30,pix_fmt="yuv420p"):
        """
        Initialises the output for the device

        devNr is the devicenr of the v4l2loopback device e.g. (/dev/video1 -> 1).
        To check the format of the device use cat /sys/devices/video4linux/video<<devNr>>/format).
        If its empty you can specify it as you like

        Syntax:
            fakeVideoDev.initOutput(69,1920,1080,fps=30)

        Args:
            devNr: deviceNr
            camx: width of the v4l2loopback device
            camy: height of the v4l2loopback device
            fps : fps of the v4l2loopback device

        Raises:
            Exception: If the input wasnt specified first, you cannot specify the output
        """
        #check if input exists
        if self.input is None:
            raise Exception("Specify input first")

        self.output = ffmpeg.output(self.input,
                                    self.VIDEODEV_STR.format(dev_nr),
                                    format="v4l2",
                                    vcodec="rawvideo",
                                    pix_fmt=pix_fmt,
                                    framerate=fps,
                                    s="{}x{}".format(camx, camy))

    def __delay_til_next_frame(self):
        """delays reading of the next frame to match ingoing fps"""
        timediff = (time.time() - self.last_frame_time)
        
        time.sleep(max((1 / self.vid_source.fps() - timediff), 0))
        
        self.last_frame_time = time.time()

    def stop(self):
        """
        Stops if run was called
        """
        self.running = False
        self.ffmpeg_proc.terminate()

    def run(self,quiet = True):
        """
        Runs an endless loop of consuming images from the source and sending them to the Device

        Syntax:
            webcam = WebcamSource()
            fvd.initInput(webcam)
            fvd.initOutput(69, 1920, 1080)
            fvd.run()
        """

        if self.output is None:
            raise Exception("Specify output first")

        self.running = True

        self.ffmpeg_proc = ffmpeg.run_async(self.output,
                                            pipe_stdin=True,
                                            quiet=quiet)
        img_gen = self.vid_source.generator()

        while self.running:
            image = next(img_gen).astype(np.uint8)

            if image is None:
                self.ffmpeg_proc.terminate()
                self.running = False
                break

            self.ffmpeg_proc.stdin.write(image.tobytes())

            self.__delay_til_next_frame()