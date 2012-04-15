import wx
from collections import namedtuple

from model.properties import Properties, IntegerProperty
from ui.propedit import PropertiesEditor, Formatter

Point = namedtuple('Point', ['x', 'y'])

class PointProperties(Properties):
    x = IntegerProperty()
    y = IntegerProperty()

    propertyOrder = ['x', 'y']

PropertiesEditor.registerType(Point, PointProperties)

def makeIntegerInput(parent, getter, setter):
    validator = Formatter(getter, setter, int, int)
    ctrl = wx.SpinCtrl(parent)
    ctrl.SetValidator(validator)

    return ctrl
    
PropertiesEditor.registerFactory(IntegerProperty, makeIntegerInput)

app = wx.App()
frame = wx.Frame(None)

e = PropertiesEditor(frame, Point)
e.SetContext(Point(0, 100))

frame.Show()
app.MainLoop()
