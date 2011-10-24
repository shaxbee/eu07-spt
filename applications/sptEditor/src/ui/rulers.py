"""
Separate module for editor rulers.
"""

import wx


class Ruler(wx.Control):
    """
    A ruler for scenery editor.
    """

    def __init__(self, parent, orientation, id = wx.ID_ANY, name = None):
        wx.Window.__init__(self, parent, id = id, name = name)
        self.SetBackgroundColour((255, 220, 153))
        self.SetMinSize((24, 24))

        self.orientation = orientation

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.offset = 0
        self.pick = None


    def OnSize(self, event):        
        """
        Refresh.
        """
        self.Refresh()


    def OnPaint(self, event):
        """
        Paints a control.
        """
        dc = wx.PaintDC(self)
        clip = self.GetUpdateRegion().GetBox()

        self.PaintScale(dc, clip)
        self.PaintMousePointer(dc, clip)


    def PaintScale(self, dc, clip):
        """
        Paints scale.
        """
        oldPen = dc.GetPen()
        oldTextFg = dc.GetTextForeground()
        oldFont = dc.GetFont()
        try:
            dc.SetPen(wx.Pen((0, 51, 153)))
            dc.SetTextForeground((0, 51, 153))
            dc.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL))

            part = self.GetParent().parts[0]
            (unitX, unitY) = part.GetScrollPixelsPerUnit()
            # Here is a problem with GetViewStart method under wxGTK
            (vx, vy) = part.GetViewStart()
            (w, h) = self.GetSize()
            if self.orientation == wx.VERTICAL:
                self.offset = vy
            elif self.orientation == wx.HORIZONTAL:
                self.offset = vx
            (p2x, p2y) = part.CalcUnscrolledPosition((vx, vy))

            if self.orientation == wx.VERTICAL:

                y = -(self.offset * unitY % 100)
                while y < h:
                    p3d = part.ViewToModel((p2x,
                        y + self.offset * unitY))
                    label = "%.2f" % p3d.y
                    (tw, th) = dc.GetTextExtent(label)
                    if y >= clip.y-tw/2-1 and y <= clip.y+clip.height+tw/2+1:
                        dc.DrawRotatedText(label, 15-th, y + tw/2, 90)
                        dc.DrawLine(16, y, clip.width, y)
                    y += 100

            elif self.orientation == wx.HORIZONTAL:

                x = -(self.offset * unitX % 100)
                while x < w:
                    p3d = part.ViewToModel(
                         (x + self.offset*unitX, p2y))
                    label = "%.2f" % p3d.x
                    (tw, th) = dc.GetTextExtent(label)
                    if x >= clip.x-tw/2-1 and x <= clip.x+clip.width+tw/2+1:
                        dc.DrawText(label, x - tw/2, 15 - th)
                        dc.DrawLine(x, 16, x, clip.height)
                    x += 100

        finally:
            dc.SetPen(oldPen)
            dc.SetTextForeground(oldTextFg)
            dc.SetFont(oldFont)
    

    def PaintMousePointer(self, dc, clip):
        """
        Draws mouse pointer on ruler.
        """
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen('BLACK'))
            if self.orientation == wx.HORIZONTAL and self.pick is not None: 
                dc.DrawLine(self.pick, 8, self.pick, 24)
            elif self.orientation == wx.VERTICAL and self.pick is not None:
                dc.DrawLine(8, self.pick, 24, self.pick)
        finally:
            dc.SetPen(oldPen)


    def HandleOnScroll(self, event):
        """
        Handles scrolled window events.
        """
        if event.GetOrientation() == self.orientation:
            self.Refresh()
        event.Skip()


    def UpdateMousePointer(self, point):
        """
        Updates mouse pointers and requests repaint events.
        """
        if self.orientation == wx.HORIZONTAL:
            if self.pick == None:
                self.pick = point.x
                self.RefreshRect(wx.Rect(point.x, 0, 1, 24))
            else:
                oldPick = self.pick
                self.pick = point.x
                self.RefreshRect(wx.Rect(min(self.pick, oldPick), 0,
                    abs(self.pick - oldPick)+1, 24))

        elif self.orientation == wx.VERTICAL:
            if self.pick == None:
                self.pick = point.y
                self.RefreshRect(wx.Rect(0, point.y, 24, 1))
            else:
                oldPick = self.pick
                self.pick = point.y
                self.RefreshRect(wx.Rect(0, min(self.pick, oldPick), 24,
                    abs(self.pick - oldPick)+1))
