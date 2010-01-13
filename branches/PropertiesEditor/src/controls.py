'''
Created on 2009-08-19

@author: mandziej
'''

import wx
import sys

class Input:
    def __init__(self, label, value = None):
        self.__label = label
        self.__value = value
        self.onChange = None
        
    def setValue(self, value):
        oldValue = self.__value
        self.__value = value
        
        if self.onChange:
            try:
                if not self.onChange(oldValue, value):
                    self.__value = oldValue
                    raise ValueError()
            except Exception, e:
                self.__value = oldValue
                raise e
        
    def enable(self): self.getControl().Enable(true)
    def disable(self): self.getControl().Disable()
    def setEnabled(self, value): self.getControl().Enable(value)
    def isEnabled(self): self.getControl().IsEnabled()
    
    def show(self): self.getControl().Show(true)
    def hide(self): self.getControl().Hide()
    def setVisible(self, value): self.getControl().Show(value)
    def isVisible(self): return self.getControl().IsShown()

    def render(self, parent):
	self.__labelControl = wx.StaticText(parent, -1)
	self.__labelControl.SetLabel(self.__label)

	self.__control = self.createControl(parent)
	self.__control.Bind(wx.EVT_KILL_FOCUS, self.__handleOnChange)

	sizer = parent.GetSizer()

        sizer.AddSpacer(5)
        sizer.Add(self.__labelControl, flag = wx.ALIGN_LEFT | wx.RIGHT | wx.LEFT, border = 5)
        sizer.Add(self.__control, flag = wx.EXPAND | wx.HORIZONTAL, border = 5)

    def createControl(self, parent):
        raise NotImplementedError()

    def __handleOnChange(self, event):
        try:
            self.setValue(self.control.GetValue())
            event.Skip()
        except Exception, e:
            event.StopPropagation()
            raise e
   
    enabled = property(isEnabled, setEnabled)
    visible = property(isVisible, setVisible)
    
    label = property(lambda self: self.__label)
    value = property(lambda self: self.__value, setValue)
   
    control = property(lambda self: self.__control) 

class TextInput(Input):
    def __init__(self, label, value = ""):
        Input.__init__(self, label, str(value))
        self.onKeyPress = None
        
    def __handleOnKeyPress(self, event):
        if self.onKeyPress and not self.onKeyPress(event.GetKeyCode()):
            print "nok"
            event.StopPropagation()
        else:
            event.Skip()
            
    def createControl(self, parent):
        control = wx.TextCtrl(parent, -1, style = 0)
        control.Bind(wx.EVT_CHAR, self.__handleOnKeyPress)
        return control
    
class IntegerInput(Input):
    def __init__(self, label, value = 0):
        Input.__init__(self, label, value)
        self.__range = self.__defaultRange
        
    def createControl(self, parent):
        # create and configure control
        control = wx.SpinCtrl(parent, -1)
        control.SetRange(*self.__range)
	return control        

    def setRange(self, min, max):
        self.__range = (min, max)
        
        if self.control:
            self.control.setRange(*self.__range)

    def disableRange(self):
        self.setRange(*self.__defaultRange)

    __defaultRange = (-sys.maxint - 1, sys.maxint)
 
    range = property(lambda self: self.__range, setRange)
