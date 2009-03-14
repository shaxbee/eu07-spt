'''
@author adammo
'''

import datetime
import logging

import wx

SCALE_FACTOR = 1000.0

class SceneryEditor(wx.Panel):
    '''
    Scenery editor control.
    '''

    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id, style = wx.BORDER_SUNKEN)
        self.SetBackgroundColour('BLUE')        

        sizer = wx.FlexGridSizer(2, 2, 1, 1)

        corner = wx.Panel(self, name = "Corner")
        corner.SetBackgroundColour('WHITE')
        leftRuler = wx.Panel(self, name = "Left ruler")
        leftRuler.SetBackgroundColour('GREEN')
        topRuler = wx.Panel(self, name = "Top ruler")
        topRuler.SetBackgroundColour('RED')
        area = PlanePart(self)

        sizer.Add(corner)
        sizer.Add(topRuler, flag = wx.LEFT | wx.EXPAND)
        sizer.Add(leftRuler, flag = wx.TOP | wx.EXPAND)
        sizer.Add(area, 1, wx.EXPAND | wx.ALL)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableRow(1, 1)

        self.SetSizer(sizer)



class PlanePart(wx.ScrolledWindow):
    '''
    Editor Part displaying XZ view of scenery.
    '''

    def __init__(self, parent, id = wx.ID_ANY):
        wx.ScrolledWindow.__init__(self, parent, id, \
            style = wx.VSCROLL | wx.HSCROLL)

        self.SetVirtualSizeHints(1000, 1000, -1, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMoveUpdateStatusBar)

        self.logger = logging.getLogger('Paint')

        self.scale = 1.0

        self.minX = -1000.0
        self.minZ = -1000.0
        self.maxX = 1000.0
        self.maxZ = 1000.0

        self.extentX = 0
        self.extentY = 0

        size = self.ComputePreferredSize() 
        self.SetClientSize(size)


    def ComputeMinMax(self, doScaling = False):
        '''
        Computes bounds of scenery expressed in scenery coordinates.
        '''
        nMinX = -1000.0
        nMinZ = 1000.0
        nMaxX = -1000.0
        nMaxZ = 1000.0

        # tracks
        # switches
        # base point

        # Changes
        if doScaling or nMinX < self.minX or nMinZ < self.minZ \
            or nMaxX > self.maxX or nMaxZ > self.maxZ:
            self.minX = min(self.minX, nMinX)
            self.minZ = min(self.minZ, nMinZ)
            self.maxX = max(self.maxX, nMaxX)
            self.maxZ = max(self.maxZ, nMaxZ)

            # ScaleAll()

            return True
        else:
            return False


    def ViewToModel(self, point):
        '''
        Converts 2D point of UI editor coordinates into 3D point
        of scenery coordinates.
        '''
        return ((point[0] - 100.0) / self.scale * SCALE_FACTOR + self.minX, \
            0.0,
            -((point[1] - 100.0) / self.scale * SCALE_FACTOR + self.minZ))


    def ModelToView(self, point):
        '''
        Converts 3D point of scenery coordiante into 2D point of
        UI editor coordinates.
        '''
        return ((point[0] - self.minX) * self.scale / SCALE_FACTOR + 100, \
            (-point[2] - self.minZ) * self.scale / SCALE_FACTOR + 100)


    def OnSize(self, event):

        self.Refresh()


    def ComputePreferredSize(self):
        (w, h) = self.GetSize()
        
        return (max(w, (self.scale * (self.maxX - self.minX) \
                / SCALE_FACTOR + 200)) + self.extentX,
            max(h + self.extentY, (self.scale * (self.maxZ - self.minZ) \
               / SCALE_FACTOR) + 200) + self.extentY)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)

        clip = self.GetUpdateRegion().GetBox()

        startTime = datetime.datetime.now()
        try:
            self.PaintBackground(dc, clip)
            self.PaintForeground(dc, clip)
        finally:
            delta = datetime.datetime.now() - startTime
            idelta = delta.days * 86400 + delta.seconds * 1000000 \
                + delta.microseconds
            self.logger.debug(u"Paint lasted %d \u00b5s" % idelta)


    def PaintBackground(self, dc, clip):
        '''
        Paints part background.
        '''
        self.PaintGrid(dc, clip)


    def PaintGrid(self, dc, clip):
        '''
        Paints grid.
        '''
        self.PaintAuxiliaryGrid(dc, clip)
        self.PaintMinMaxBounds(dc, clip)


    def PaintAuxiliaryGrid(self, dc, clip):
        '''
        Paints a grid.
        '''
        center2D = self.ModelToView((0.0, 0.0, 0.0))        

        xoffset = clip.x + clip.width
        yoffset = clip.y + clip.height

        x = center2D[0]
        while x > clip.width:
            x = x - 100
            dc.DrawLine(x, clip.y, x, yoffset)
        x = center2D[0]
        while x < xoffset:
            dc.DrawLine(x, clip.y, x, yoffset)
            x = x + 100
        
        y = center2D[1]
        while y > clip.height:
            y = y - 100
            dc.DrawLine(clip.x, y, xoffset, y)
        y = center2D[1]
        while y < clip.height:
            dc.DrawLine(clip.x, y, xoffset, y)
            y = y + 100


    def PaintMinMaxBounds(self, dc, clip):
        '''
        Paints the borders around min/max.
        '''
        x = (self.maxX - self.minX) * self.scale / SCALE_FACTOR + 100
        y = (self.maxZ - self.minZ) * self.scale / SCALE_FACTOR + 100

        dc.DrawLine(clip.x, 100, clip.x + clip.width, 100)

        dc.DrawLine(x, clip.y, x, clip.x + clip.height)

        dc.DrawLine(clip.x + clip.width, y, clip.x, y)

        dc.DrawLine(100, clip.y + clip.height, 100, clip.y)


    def PaintForeground(self, dc, clip):
        '''
        Paints foreground
        '''
        self.PaintScale(dc, clip)


    def PaintScale(self, dc, clip):
        '''
        Paints a scale.
        '''

        # TODO: Draw scale in upper, right corner

        dc.DrawText("%.2f" % self.scale, 5, 5)


    def OnMoveUpdateStatusBar(self, event):
        '''
        Updates 3D coordinates in case of mouse movement on frame status bar.
        '''

        (x, y) = event.GetPosition()        
        (a, b, c) = self.ViewToModel((x, y))

        bar = self.GetParent().GetParent().GetStatusBar()
        bar.SetStatusText("%.3f, %.3f, %.3f" % (a, b, c))

