'''
@author adammo
'''

import wx

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
            style = wx.VSCROLL | wx.HSCROLL | wx.ALWAYS_SHOW_SB)
        self.SetBackgroundColour('BLACK')
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, event):

        dc = wx.WindowDC(self)
        oldPen = dc.GetPen()
        dc.SetPen(wx.WHITE_PEN)
        array = [ \
            wx.Point(4, 4), wx.Point(5, 7), wx.Point(29, 30), \
            wx.Point(59, 189)]

        dc.DrawSpline(array)

        dc.SetPen(oldPen)
        
