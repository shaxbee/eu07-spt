'''
Created on 2010-01-30

@author: gfirlejczyk
'''
#import datetime
import logging
#from decimal import Decimal

import wx
from wx.lib.evtmgr import eventManager
import wx.glcanvas
import osg, osgGA, osgViewer

#import model.tracks
#import ui.views
#from sptmath import Vec3

#SCALE_FACTOR = 1000.0

class SceneryEditor(wx.Frame):
    '''
    Scenery editor OSG Control
    '''


    def __init__(self, parent, id = wx.ID_ANY):
#        wx.Panel.__init__(self, parent, id, style = wx.BORDER_SUNKEN)
        wx.Frame.__init__(self,parent,id,"",wx.DefaultPosition,parent.GetClientSize(),wx.BORDER_SUNKEN,"")
        
        width,height = self.GetClientSize()
        self.canvas = OSGCanvas(self, wx.ID_ANY, 0, 0, 400, 600)

        root = osg.Node()
        
#        model = osgDB.readNodeFile( filename.encode() )
#        telepointer = createTelepointer(subcontroller, 600, 400)
        
#        self.subcontroller.rootNode = root
#        self.subcontroller.telepointerNode = telepointer
#       self.subcontroller.modelNode = model
    
        root.addChild( root )
        root.__disown__()
#        root.addChild( telepointer, False )
        self.canvas.viewer.setSceneData( root )
        
#        wx.EVT_WINDOW_DESTROY(self, self.OnDestroy)
        
        self.Show()
         

class OSGCanvas(wx.glcanvas.GLCanvas):
    def __init__(self,parent,id,x,y,width,height):
        size = wx.wxSize(width,height)
        style = wx.WANTS_CHARS | wx.FULL_REPAINT_ON_RESIZE
        wx.glcanvas.GLCanvas.__init__(self,parent,id,wx.DefaultPosition,size,style)

        width,height = self.GetClientSize()

        self.viewer = osgViewer.Viewer()

        self.viewer.addEventHandler(osgViewer.StatsHandler())
#        self.viewer.setCameraManipulator(osg.MyTrackballManipulator())
#        stateSetManipulator = osgGA.StateSetManipulator()
#        getController().stateSetManipulator = stateSetManipulator
#        self.viewer.addEventHandler(stateSetManipulator)

        self.graphicswindow = self.viewer.setUpViewerAsEmbeddedInWindow(0,0,width,height)

        if self.graphicswindow.valid():

            self.old_cursor = wx.STANDARD_CURSOR

            self.Bind(wx.EVT_SIZE, self.OnSize)
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

            self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
            self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
            self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)


    def OnPaint(self, evt):
        wx.PaintDC(self)
        
        if (not self.GetContext() or not self.graphicswindow.valid()):
            return

        self.SetCurrent()
        self.viewer.frame()
        self.SwapBuffers()
        
#    def OnOpenFile(self, evt):
#        self.
             
        
    def OnSize(self, evt):

        w,h = self.GetClientSize()

        if self.GetParent().IsShown():
            self.SetCurrent()

        if self.graphicswindow.valid():
            self.graphicswindow.getEventQueue().windowResize(0, 0, w, h)
            self.graphicswindow.resized(0,0,w,h)

        evt.Skip()


    def OnEraseBackground(self, evt):
        pass

    def GetConvertedKeyCode(self, evt):
        """in wxWidgets, key is always an uppercase
           if shift is not pressed convert to lowercase
        """
        key = evt.GetKeyCode()
        if key >= ord('A') and key <= ord('Z'):
            if not evt.ShiftDown():
                key += 32
        return key

    def OnKeyDown(self,evt):
        key = self.GetConvertedKeyCode(evt)
        self.graphicswindow.getEventQueue().keyPress(key)
        evt.Skip()

    def OnKeyUp(self,evt):        
        key = self.GetConvertedKeyCode(evt)
        self.graphicswindow.getEventQueue().keyRelease(key)
        evt.Skip()
    

    def OnMouse(self,event):
        if (event.ButtonDown()):
            button = event.GetButton()
            self.graphicswindow.getEventQueue().mouseButtonPress(event.GetX(), event.GetY(), button)
        elif (event.ButtonUp()):
            button = event.GetButton()
            self.graphicswindow.getEventQueue().mouseButtonRelease(event.GetX(), event.GetY(), button)
        elif (event.Dragging()):
            self.graphicswindow.getEventQueue().mouseMotion(event.GetX(), event.GetY())
            pass
        elif (event.Moving()):
            self.graphicswindow.getEventQueue().mouseMotion(event.GetX(), event.GetY())
            pass
        event.Skip()
        