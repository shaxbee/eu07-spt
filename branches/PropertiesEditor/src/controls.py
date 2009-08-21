'''
Created on 2009-08-19

@author: mandziej
'''

import wx

RETURN_TRUE = lambda x: True

class Input:
    def __init__(self, label, value = None, onChange = None):
        self.__label = label
        self.__value = value
        self.__onChange = onChange
        
    def setValue(self, value):
        oldValue = self.__value
        self.__value = value
        
        if self.__onChange:
            try:
                if not self.__onChange(oldValue, value):
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
        raise NotImplementedError()

    def handleOnChange(self, event):
        try:
            self.value = self.getControl().GetValue()
        except Exception, e:
            event.Skip()
            raise e
   
    def addToSizer(self, sizer, label, control):
        sizer.AddSpacer(5)
        sizer.Add(label, flag = wx.ALIGN_LEFT | wx.RIGHT | wx.LEFT, border = 5)
        sizer.Add(control, flag = wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, border = 5)
    
    enabled = property(isEnabled, setEnabled)
    visible = property(isVisible, setVisible)
    
    label = property(lambda self: self.__label)
    value = property(lambda self: self.__value, setValue)
    
    onChange = property(lambda self: self.__onChange)

class TextInput(Input):
    def __init__(self, label, value = "", onKeyPress = None, **kwargs):
        Input.__init__(self, label, str(value), **kwargs)
        self.__onKeyPress = onKeyPress
        
    def handleOnKeyPress(self, event):
        if self.__onKeyPress(event.GetKeyCode()) == False:
            event.Skip()
            
    def getControl(self): return self.__control
        
    def render(self, parent):
        control = wx.TextCtrl(parent, -1, style = 0)
        
        # attach event handlers
        control.Bind(wx.EVT_KILL_FOCUS, self.handleOnChange)        
        if self.__onKeyPress:
            control.Bind(wx.EVT_CHAR, self.handleOnKeyPress)
            
        label = wx.StaticText(parent, -1)
        label.SetLabel(self.label)

        self.addToSizer(parent.GetSizer(), label, control)
        self.__control = control
    
    onKeyPress = property(lambda self: self.__onKeyPress)
    
class IntegerInput(Input):
    def __init__(self, label, value = 0, range = None, **kwargs):
        Input.__init__(self, label, value, **kwargs)
        self.__range = range
        
    def render(self, parent):
        # create and configure control
        control = wx.SpinCtrl(parent, -1,)
        if self.__range:
            control.SetRange(*self.__range)
        
        # attach event handlers
        if self.onChange:
            control.Bind(wx.EVT_KILL_FOCUS, self.handleOnChange)
        
        label = wx.StaticText(parent, -1)
        label.SetLabel(self.label)
        
        self.addToSizer(parent.GetSizer(), label, control)
        self.__control = control
        
    range = property(lambda self: self.__range)