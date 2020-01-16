import virtualvideo

import cv2

class MyVideoSource(virtualvideo.VideoSource):
    def __init__(self):
        self.img = cv2.imread("fish.jpg")
        size = self.img.shape
        #opencv's shape is y,x,channels
        self._size = (size[1],size[0])

    def img_size(self):
        return self._size

    def fps(self):
        return 10

    def generator(self):
        while True:
           for i in range(1,100,2):
            #processes the image a little bit
                x = abs(50-i)
                yield cv2.blur(self.img,(x,x))


vidsrc = MyVideoSource()
fvd = virtualvideo.FakeVideoDevice()
fvd.init_input(vidsrc)
fvd.init_output(69, 1280, 720, fps=30)
fvd.run()