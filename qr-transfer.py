import os
import wx

class QRTransfer(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='QR Transfer')

        self.previousSize = self.frame.GetSize()

        self.panel = wx.Panel(self.frame)

        self.imageMaxSize = 240

        self.BOTTOM_HEIGHT = 35
        self.BROWSE_BTN_WIDTH = 90

        self.createWidgets()
        self.frame.Show()

    def createWidgets(self):
        instructions = 'Browse for a file'
        self.emptyImg = wx.EmptyImage(self.imageMaxSize,self.imageMaxSize)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(self.emptyImg))

        self.fileTxt = wx.TextCtrl(self.panel)
        self.browseBtn = wx.Button(self.panel, label='Browse')
        self.browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)

        self.Bind(wx.EVT_SIZE, self.onResize)

        DEFAULT_WIDTH = 500
        self.frame.SetSize( (DEFAULT_WIDTH, DEFAULT_WIDTH+self.BOTTOM_HEIGHT) )

        self.panel.Layout()

    def onBrowse(self, event):
        wildcard = "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.fileTxt.SetValue(dialog.GetPath())
        dialog.Destroy()


        self.onView(emptyImg)

    def onView(self, img):
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.imageMaxSize
            NewH = self.imageMaxSize * H / W
        else:
            NewH = self.imageMaxSize
            NewW = self.imageMaxSize * W / H
        img = img.Scale(NewW,NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
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

        self.onView(self.emptyImg)

if __name__ == '__main__':
    app = QRTransfer()
    app.MainLoop()
