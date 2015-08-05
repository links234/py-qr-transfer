import os
import wx
import png
import zlib

from subprocess import call

def deflate(data, compresslevel=9):
    compress = zlib.compressobj(
            compresslevel,
            zlib.DEFLATED
    )
    deflated = compress.compress(str(data))
    deflated += compress.flush()
    return bytearray(deflated)

CACHE_DIR = "cache"

class QRTransfer(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='QR Transfer')

        self.previousSize = self.frame.GetSize()

        self.panel = wx.Panel(self.frame)

        self.BOTTOM_HEIGHT = 35
        self.BROWSE_BTN_WIDTH = 90

        self.createWidgets()
        self.frame.Show()

    def createWidgets(self):
        self.emptyImg = wx.EmptyImage(50,50)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(self.emptyImg))

        self.fileTxt = wx.TextCtrl(self.panel)
        self.browseBtn = wx.Button(self.panel, label='Browse')
        self.browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)

        self.Bind(wx.EVT_SIZE, self.onResize)

        self.image = self.emptyImg

        DEFAULT_WIDTH = 500
        self.frame.SetSize( (DEFAULT_WIDTH, DEFAULT_WIDTH+self.BOTTOM_HEIGHT) )

        self.panel.Layout()

    def onBrowse(self, event):
        wildcard = "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            self.fileTxt.SetValue(filename)
            if os.path.isfile(filename):
                self.makeQR(filename)

        dialog.Destroy()

    def encode(self, data):
        dataSize = len(data)
        header = [ (dataSize>>24)&0xFF, (dataSize>>16)&0xFF, (dataSize>>8)&0xFF,
                    dataSize&0xFF]
        headerData = bytearray(header)
        return bytearray(headerData+deflate(data))

    def makeQR(self, filename):
        with open(filename, 'rb') as file:
            fileData = bytearray(file.read())

            data = bytearray(self.encode(fileData))

            if not os.path.exists(CACHE_DIR):
                os.makedirs(CACHE_DIR)

            filenameTemp = CACHE_DIR + "/temp_file"
            with open(filenameTemp, 'wb') as file:
                file.write(data)

            filenameQrImage = CACHE_DIR + "/" + "qr1.png"

            call(["python3", "qr-encode.py", "-i", filenameTemp, "-o", filenameQrImage])

            qrImage = wx.Image(filenameQrImage, wx.BITMAP_TYPE_ANY)
            self.setImage(qrImage)

    def setImage(self, img):
        self.image = img
        self.onView()

    def onView(self):
        # scale the image, preserving the aspect ratio
        W = self.image.GetWidth()
        H = self.image.GetHeight()
        if W > H:
            NewW = self.imageMaxSize
            NewH = self.imageMaxSize * H / W
        else:
            NewH = self.imageMaxSize
            NewW = self.imageMaxSize * W / H
        self.image = self.image.Scale(NewW,NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.image))
        self.panel.Refresh()

    def onResize(self, event):
        event.Skip()
        width, height = size = self.frame.GetSize()
        if size != self.previousSize:
            self.doResize(width, height)

            self.previousSize = size

    def doResize(self, width, height):
        if width < height-self.BOTTOM_HEIGHT:
            self.imageMaxSize = width
        else:
            self.imageMaxSize = height-self.BOTTOM_HEIGHT

        self.browseBtn.SetPosition( (width-self.BROWSE_BTN_WIDTH,
                                    height-self.BOTTOM_HEIGHT) )
        self.browseBtn.SetSize( (self.BROWSE_BTN_WIDTH,self.BOTTOM_HEIGHT) )

        self.fileTxt.SetPosition( (0,height-self.BOTTOM_HEIGHT) )
        self.fileTxt.SetSize( (width-self.BROWSE_BTN_WIDTH,self.BOTTOM_HEIGHT) )

        self.onView()

if __name__ == '__main__':
    app = QRTransfer()
    app.MainLoop()
