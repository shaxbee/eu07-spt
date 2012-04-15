import wx
import functools
import logging

from abc import ABCMeta, abstractmethod

logger = logging.getLogger('PropertiesEditor')

class Policy:
    """
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, subject):
        """
        """

        pass

    @abstractmethod
    def commit(self, subject):
        """
        """

        pass

class NoopPolicy(Policy):
    """
    """

    def accept(self, subject):
        return subject

    def commit(self, subject):
        pass

class PropertiesEditorError(NameError):
    """
    """

    pass

class PropertiesEditor(wx.Panel):
    """
    """

    __factories = dict()
    __descriptors = dict()

    def __init__(self, parent, contextType, **args):
        super(PropertiesEditor, self).__init__(parent, **args)
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)

        if contextType not in PropertiesEditor.__descriptors:
            raise PropertiesEditorError("No descriptor found for %s type" % str(contextType))

        self.__context = None
        self.__contextType = contextType

        # fetch list of properties for contextType
        properties = PropertiesEditor.__descriptors[contextType].getProperties()

        # create sizer with enough rows to hold all properties
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.FlexGridSizer(rows = len(properties), cols = 2, vgap = 9, hgap = 9)

        def propGetter(name):
            return getattr(self.GetContext(), name)

        def propSetter(name, value):
            return setattr(self.GetContext(), name, value)

        for name, prop in properties.iteritems():
            propertyType = type(prop)
            if propertyType not in PropertiesEditor.__factories:
                raise PropertiesEditorError("No property input factory found for %s type" % propertyType)

            # create property label
            label = wx.StaticText(self, label = prop.getLabel())

            # bind property name to accessors
            getter = functools.partial(propGetter, name)
            setter = functools.partial(propSetter, name)

            # create input control
            ctrl = PropertiesEditor.__factories[propertyType](self, getter, setter)

            # add label and input to sizer
            sizer.Add(label, flag = wx.ALIGN_RIGHT)
            sizer.Add(ctrl, proportion = 1, flag = wx.EXPAND)

        # make inputs column growable
        sizer.AddGrowableCol(idx = 1, proportion = 1)
        hbox.Add(sizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 9)

        self.SetSizer(hbox)

        # bind context-checking initialization code
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInit)

    def GetContext(self):
        return self.__context

    def SetContext(self, context):
        if type(context) is not self.__contextType:
            raise TypeError("Expected context to be of type %s, got %s" % (self.__contextType, type(context)))

        self.__context = context

        # if properties dialog is visible force updating control values
        if(self.IsShown()):
            self.TransferDataToWindow()

    def OnInit(self, event):
        if self.__context is None:
            raise ValueError("Context for properties editor is not set")

        self.Validate()

    @classmethod
    def registerType(cls, contextType, descriptor, policy = NoopPolicy()):
        cls.__descriptors[contextType] = descriptor

    @classmethod
    def registerFactory(cls, propertyType, factory):
        cls.__factories[propertyType] = factory

class Formatter(wx.PyValidator):
    """
    """

    def __init__(self, getter, setter, coercer, formatter = str):
        wx.PyValidator.__init__(self)

        self.__formatter = formatter
        self.__coercer = coercer
        self.__getter = getter
        self.__setter = setter

    def Clone(self):
        return Formatter(self.__getter, self.__setter, self.__coercer, self.__formatter)

    def Validate(self, parent):
        return True 

    def TransferFromWindow(self):
        try:
            # convert control value to a storage-formatted value 
            value = self.__coercer(self.GetControlValue())
            self.__setter(value)
        except TypeError, e:
            logger.info("Failed to convert value \"%s\": %s" % (self.GetControlValue(), str(e)))
            return False
        except Exception, e:
            logger.error(e)
            return False

        return True

    def TransferToWindow(self):
        try:
            # convert storage value to presentation-formatted value
            value = self.__formatter(self.__getter())
            self.SetControlValue(value)
        except Exception, e:
            logger.error(e)
            return False

        return True

    def GetControlValue(self):
        ctrl = self.GetWindow()
        if not hasattr(ctrl, GetValue):
            raise AttributeError("Control doesn't define GetValue method")
            
        return ctrl.GetValue()

    def SetControlValue(self, value):
        ctrl = self.GetWindow()
        if not hasattr(ctrl, "SetValue"):
            raise AttributeError("Control doesn't define SetValue method")

        ctrl.SetValue(value)
