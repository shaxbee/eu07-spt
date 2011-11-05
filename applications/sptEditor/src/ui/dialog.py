"""
This module contains all dialogs defined in editor application.

@author adammo
"""

import math
import wx
import wx.xrc
import wx.lib.delayedresult as delayed
import yaml
from sptmath import Decimal
import os.path
import sys
import traceback
import logging

from model.tracks import Track, Switch
import ui.editor
import ui.trackfc
from sptmath import Vec3
import sptyaml
import db.export




class CenterAtDialog(wx.Dialog):
    """
    Dialog box for centering view at specified scenery point.
    """
    
    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "CenterAtDialog")
        self.PostCreate(w)

        editor = parent.editor

        self.x = wx.xrc.XRCCTRL(self, "x")
        self.y = wx.xrc.XRCCTRL(self, "y")
        self.z = wx.xrc.XRCCTRL(self, "z")
        self.zoom = wx.xrc.XRCCTRL(self, "zoom")
        self.zoom.SetValue(str(editor.parts[0].GetScale().get())) 

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
            px = Decimal(str(self.x.GetValue()))
            py = Decimal(str(self.y.GetValue()))
            pz = Decimal(str(self.z.GetValue()))
            pScale = float(self.zoom.GetValue())

            editor = self.GetParent().editor
            editor.parts[0].SetScale(ui.editor.Scale(pScale))
            (vx, vy) = editor.parts[0].ModelToView(Vec3(px, py, pz))
            editor.parts[0].CenterViewAt((vx, vy))

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
            editor.SetBasePoint(ui.editor.BasePoint(Vec3(px, py, pz), alpha, gradient), True)

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
            if name.strip() != "":
                t.name = name.strip()

            # Remember entered values
            config = wx.FileConfig.Get()
            config.Write("/InsertStraightTrack/length", self.length.GetValue())

            editor = self.GetParent().editor
            editor.scenery.AddRailTracking(t)

            self.Destroy()
        except ValueError:
            # Swallow the exception
            pass



         
class InsertCurveTrack(wx.Dialog):
    """
    Dialog for inserting straight track
    """

    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "InsertCurveTrack")
        self.PostCreate(w)

        self.length = wx.xrc.XRCCTRL(self, "length")
        self.radius = wx.xrc.XRCCTRL(self, "radius")
        self.leftOrRight = wx.xrc.XRCCTRL(self, "leftOrRight")
        self.name = wx.xrc.XRCCTRL(self, "name")

        config = wx.FileConfig.Get()
        defaultLength = config.Read("/InsertCurveTrack/length", "0.000")
        defaultRadius = config.Read("/InsertCurveTrack/radius", "300.000")
        defaultLeftOrRight = config.ReadInt("/InsertCurveTrack/leftOrRight", 0)
        self.length.SetValue(defaultLength)
        self.radius.SetValue(defaultRadius)
        self.leftOrRight.SetSelection(defaultLeftOrRight)

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def OnButton(self, event):
        try:
            length = float(self.length.GetValue())
            radius = float(self.radius.GetValue())
            leftOrRight = self.leftOrRight.GetSelection()
            name = self.name.GetValue().strip()            

            if length <= 0.0 or radius <= 0.0:
                # we don't accept non-positive values
                return

            editor = self.GetParent().editor
            tf = ui.trackfc.TrackFactory(editor)
            t = tf.CreateCurve(length, radius, leftOrRight == 0)
            if name.strip() != "":
                t.name = name.strip()

            config = wx.FileConfig.Get()
            config.Write("/InsertCurveTrack/length", self.length.GetValue())
            config.Write("/InsertCurveTrack/radius", self.radius.GetValue())
            config.WriteInt("/InsertCurveTrack/leftOrRight", leftOrRight)

            editor.scenery.AddRailTracking(t)

            self.Destroy()
        except ValueError:
            # Swallow the exception
            pass



class InsertRailSwitch(wx.Dialog):
    """
    Dialog for inserting rail switch
    """

    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "InsertRailSwitch")
        self.PostCreate(w)

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)

        self.PrepareList()
        self.FillContent(parent)

        config = wx.FileConfig.Get()
        defaultPrefabric = config.ReadInt("/InsertRailSwitch/prefabric", 0)
        defaultHandle = config.ReadInt("/InsertRailSwitch/handle", 0)
        self.predefinedList.SetSelection(defaultPrefabric)
        self.handles.SetSelection(defaultHandle)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def PrepareList(self):
        pd_types = yaml.load(file("prefabric.yaml", "r"), Loader=sptyaml.SptLoader)        
        self.predefined = pd_types['right_switches'] + pd_types['left_switches']


    def FillContent(self, parent):
        self.predefinedList = wx.xrc.XRCCTRL(self, "predefined")
        self.predefinedList.SetItems(map(lambda item: unicode(item), self.predefined))
        self.handles = wx.xrc.XRCCTRL(self, "handles")
        self.name = wx.xrc.XRCCTRL(self, "name")


    def OnButton(self, event):
        try:
            index = self.predefinedList.GetSelection()
            handle = self.handles.GetSelection()
            name = self.name.GetValue().strip()

            if index == wx.NOT_FOUND:
                return
            if name.strip() == "":
                wx.MessageBox("Rail switch must have a name.",
                    self.GetTitle(), wx.OK | wx.ICON_ERROR, self)
                return

            editor = self.GetParent().editor
            tf = ui.trackfc.TrackFactory(editor)
            template = self.predefined[index].railTracking
            s = tf.CopyRailTracking(template, self.GetStartPoint(template, handle))
            s.name = name

            config = wx.FileConfig.Get()
            config.WriteInt("/InsertRailSwitch/prefabric", index)
            config.WriteInt("/InsertRailSwitch/handle", handle)

            editor.scenery.AddRailTracking(s)

            self.Destroy()
        except ValueError:
            # Swallow the exception
            pass


    def GetStartPoint(self, switch, index):
        if index == 0:
            return switch.pc
        elif index == 1:
            return switch.p1
        elif index == 2:
            return switch.p2
        else:
            raise ValueError, "Cannot find startPoint"




class NameDialog(wx.Dialog):
    """
    Very simple dialog for filling the name.
    """

    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "NameDialog")
        self.PostCreate(w)

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)

        self.FillContent()

        self.Fit()
        self.Centre()
      

    def FillContent(self):
        self.nameCtrl = wx.xrc.XRCCTRL(self, "name")
 

    def OnButton(self, event):
        name = self.nameCtrl.GetValue()
        if name.strip() == "":
            wx.MessageBox("This rail tracking must have a name.",
                self.GetTitle(), wx.OK | wx.ICON_ERROR, self)
            return

        self.EndModal(wx.ID_OK)


    def GetName(self):
        return self.nameCtrl.GetValue().strip()




class ExportDialog(wx.Dialog):
    """Export dialog that contains the name of scenery to export and
    the directory to export.
    """

    def __init__(self, parent):
        w = parent.xRes.LoadDialog(parent, "ExportDialog")
        self.PostCreate(w)

        self.FillContent()

        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=wx.xrc.XRCID("directorySelect"))

        self.Fit()
        self.Centre()


    def FillContent(self):
        self.nameCtrl = wx.xrc.XRCCTRL(self, "name")
        self.dirCtrl = wx.xrc.XRCCTRL(self, "directory")
        self.progress = wx.xrc.XRCCTRL(self, "progress")

        config = wx.FileConfig.Get()
        lastName = config.Read("/ExportDialog/name", "untitled")
        self.lastDir = config.Read("/ExportDialog/dir", wx.GetHomeDir())
        self.nameCtrl.SetValue(lastName)
        self.dirCtrl.SetValue(self.lastDir)


    def OnButton(self, event):
        name = self.nameCtrl.GetValue()
        
        if name.strip() == "":
            wx.MessageBox("Missing scenery name.",
                self.GetTitle(), wx.OK | wx.ICON_ERROR, self)
            return
            
        dir = self.dirCtrl.GetValue()
        if dir.strip() == "":
            wx.MessageBox("Missing directory.",
                self.GetTitle(), wx.OK | wx.ICON_ERROR, self)
            return
            
        if not os.path.isdir(dir):
            wx.MessageBox("Invalid directory.",
                self.GetTitle(), wx.OK | wx.ICON_ERROR, self)
            return
            
        dest = os.path.join(dir, name)
        if not os.path.exists(dest):
            os.mkdir(dest)

        self.Export(dest, dir, name)

        

    def OnSelect(self, event):
        defaultPath = self.dirCtrl.GetValue()
        if not os.path.isdir(defaultPath):
            defaultPath = self.lastDir
        dirDialog = wx.DirDialog(self, defaultPath=defaultPath)
        ret = dirDialog.ShowModal()
        if ret == wx.ID_OK:
            self.dirCtrl.SetValue(dirDialog.GetPath())
            self.lastPath = dirDialog.GetPath()


    def Export(self, dest, dir, name):
        """Does the right export."""
        self.Enable(False)

        trackings = self.GetParent().editor.GetScenery().tracks
        delayed.startWorker(self.ExportComplete,
            self.ExportWorkerJob,
            cargs = (dir, name),
            wargs = (dest, trackings.tracks(), trackings.switches(),
                self.UpdatePercent))
#            writer = db.sctwriter.SectorWriter(file(filename, "w"), sptmath.Vec3())
#            scenery = self.editor.GetScenery()
#            for t in scenery.tracks.tracks():
#                writer.addTrack(t)
#            writer.writeToFile()


    def UpdatePercent(self, percent):
        """Callback that updates progress bar in GUI thread."""
        # Optimise it by making event handler for this
        wx.CallAfter(self.__UpdatePercent, percent)


    def __UpdatePercent(self, *args):
        """Updates progress bar."""
        self.progress.SetValue(args[0])


    def ExportWorkerJob(self, *wargs):
        """Job run in separate thread."""
        (directory, tracks, switches, updateCallback) = wargs
        db.export.exportScenery(directory, tracks, switches, updateCallback)
        return True

    
    def ExportComplete(self, delayedResult, *cargs):
        """Completes the scenery export routine."""
        try:
            delayedResult.get()
            self.__UpdatePercent(100)

            config = wx.FileConfig.Get()
            config.Write("/ExportDialog/name", cargs[1])
            config.Write("/ExportDialog/dir", cargs[0])

        except Exception, inst:
            self.__UpdatePercent(100)
            logging.exception("Error during scenery export")
            logging.error("Scenery error Traceback", inst.extraInfo)
            wx.MessageBox("Error during scenery export.",
                "Export scenery error", wx.OK | wx.ICON_ERROR, self)
        finally:
            self.Enable(True)




class TracingBackProducer(delayed.Producer):
    """Custom Producer that provides traceback from producer thread."""

    def __init__(self, sender, workerFn, args=(), kwargs={},
            name=None, group=None, daemon=False,
            sendReturn=True, senderArg=None):
        delayed.Producer.__init__(self, sender, workerFn,
            args, kwargs, name, group, daemon, sendReturn, senderArg)


    def _extraInfo(self, exception):
        return traceback.extract_tb(sys.exc_info()[2])


def startWorker(
    consumer, workerFn, 
    cargs=(), ckwargs={}, 
    wargs=(), wkwargs={},
    jobID=None, group=None, daemon=False, 
    sendReturn=True, senderArg=None):
    """
    See for reference delayed.startWorker procedure.
    This is a derived method.
    """
    
    if isinstance(consumer, wx.EvtHandler):
        eventClass = cargs[0]
        sender = delayed.SenderWxEvent(consumer, eventClass,
            jobID=jobID, **ckwargs)
    else:
        sender = delayed.SenderCallAfter(consumer, jobID,
            args=cargs, kwargs=ckwargs)
        
    thread = TracingBackProducer(
        sender, workerFn, args=wargs, kwargs=wkwargs, 
        name=jobID, group=group, daemon=daemon, 
        senderArg=senderArg, sendReturn=sendReturn)
        
    thread.start() 
    return thread

