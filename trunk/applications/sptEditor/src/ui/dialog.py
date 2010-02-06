"""
This module contains all dialogs defined in editor application.

@author adammo
"""

import math
import wx
import wx.xrc
from decimal import Decimal

from model.tracks import Track
import ui.editor
import ui.trackfc
from sptmath import Vec3




class CenterAtDialog(wx.Dialog):
    """
    Dialog box for centering view at specified scenery point.
    """
    
    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "CenterAtDialog")
        self.PostCreate(w)

        self.x = wx.xrc.XRCCTRL(self, "x")
        self.y = wx.xrc.XRCCTRL(self, "y")
        self.z = wx.xrc.XRCCTRL(self, "z")

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def OnButton(self, event):
        """
        Sets the scroll to the editor part.
        """       
        try: 
            px = Decimal(self.x.GetValue())
            py = Decimal(self.y.GetValue())
            pz = Decimal(self.z.GetValue())

            editor = self.GetParent().editor
            (vx, vy) = editor.parts[0].ModelToView(Vec3(px, py, pz))
            editor.parts[0].CenterViewAt(vx, vy)

            self.Destroy()
        except ValueError: 
            # Swallow number parsing error
            pass




class BasePointDialog(wx.Dialog):
    """
    Dialog for manipulating base point positions and angles.
    """
    
    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "BasePointDialog")
        self.PostCreate(w)

        self.FillContent(parent)

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def FillContent(self, parent):
        basePoint = parent.editor.basePoint
        if basePoint == None:
            basePoint = ui.editor.BasePoint((0.0, 0.0, 0.0), 0, 0)

        self.x = wx.xrc.XRCCTRL(self, "x")
        self.y = wx.xrc.XRCCTRL(self, "y")
        self.z = wx.xrc.XRCCTRL(self, "z")
        self.alpha = wx.xrc.XRCCTRL(self, "alpha")
        self.gradient = wx.xrc.XRCCTRL(self, "gradient")

        self.x.SetValue("%.3f" % basePoint.point.x)
        self.y.SetValue("%.3f" % basePoint.point.y)
        self.z.SetValue("%.3f" % basePoint.point.z)
        self.alpha.SetValue("%.2f" % basePoint.alpha)
        self.gradient.SetValue("%.2f" % basePoint.gradient)


    def OnButton(self, event):
        '''
        Sets the scroll to the editor part.
        '''
        try: 
            px = Decimal(self.x.GetValue())
            py = Decimal(self.y.GetValue())
            pz = Decimal(self.z.GetValue())
            alpha = float(self.alpha.GetValue())
            gradient = float(self.gradient.GetValue())

            editor = self.GetParent().editor
            editor.SetBasePoint(ui.editor.BasePoint(Vec3(px, py, pz), alpha, gradient))
            #(vx, vy) = editor.parts[0].ModelToView((px, py, pz))
            #editor.parts[0].CenterViewAt(vx, vy)

            self.Destroy()
        except ValueError: 
            # Swallow number parsing error
            pass




class InsertStraightTrack(wx.Dialog):
    """
    Dialog for inserting straight track
    """

    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "InsertStraightTrack")
        self.PostCreate(w)

        self.length = wx.xrc.XRCCTRL(self, "length")
        self.name = wx.xrc.XRCCTRL(self, "name")

        config = wx.FileConfig.Get()
        defaultLength = config.Read("/InsertStraightTrack/length", "0.000")
        self.length.SetValue(defaultLength)

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def OnButton(self, event):
        try:
            length = Decimal(self.length.GetValue())
            name = self.name.GetValue().strip()

            if length <= Decimal(0):
                # we don't accept non-positive values
                return

            editor = self.GetParent().editor
            tf = ui.trackfc.TrackFactory(editor)
            t = tf.CreateStraight(length)
            if len(name) > 0:
                t.name = name

            # Remember entered values
            config = wx.FileConfig.Get()
            config.Write("/InsertStraightTrack/length", self.length.GetValue())

            editor = self.GetParent().editor
            editor.scenery.AddRailTracking(t)

            self.Destroy()
        except ValueError:
            # Swallow the exception
            pass
         
