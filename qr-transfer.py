import os
import wx
import png

from subprocess import call

import bk1
import anim

CACHE_DIR = "cache"
QR_INTERVAL = 300

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

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)

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

    def getQRPath(self, id):
        return CACHE_DIR+"/qr"+str(id)+".png"

    def makeQR(self, filename):
        self.timer.Stop()

        with open(filename, 'rb') as ifile:
            fileData = bytearray(ifile.read())

            if not os.path.exists(CACHE_DIR):
                os.makedirs(CACHE_DIR)

            dataArray = bk1.encode(fileData)

            filenameTemp = CACHE_DIR + "/temp_file"

            for i in range(0,len(dataArray)):
                with open(filenameTemp, 'wb') as ofile:
                    ofile.write(dataArray[i])

                    ofile.close()
                    call(["python3", "qr-encode.py", "-i", filenameTemp, "-o", self.getQRPath(i+1)])

            self.state = anim.Anim(1,4)
            self.tortoise = anim.Anim(1,len(dataArray))
            self.rabbit = anim.Anim(1,len(dataArray))

            qrImage = wx.Image(self.getQRPath(1), wx.BITMAP_TYPE_ANY)
            self.setImage(qrImage)

            self.timer.Start(QR_INTERVAL)

            ifile.close()

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

    def onTimer(self, event):
        self.state.Next()

        img = 1
        if self.state.Get() == 1:
            img = self.rabbit.Get()
            self.rabbit.Next()
        if self.state.Get() == 2:
            img = self.rabbit.Get()
            self.rabbit.Next()
        if self.state.Get() == 3:
            img = self.tortoise.Get()
        if self.state.Get() == 4:
            img = self.tortoise.Get()
            self.tortoise.Next()

        qrImage = wx.Image(self.getQRPath(img), wx.BITMAP_TYPE_ANY)
        self.setImage(qrImage)

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
