import wx
from abc import ABCMeta, abstractmethod

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

    def __init__(self, parent, context, **args):
        super(PropertiesEditor, self).__init__(parent, **args)

        contextType = type(context)

        if contextType not in PropertiesEditor.__descriptors:
            raise PropertiesEditorError("No descriptor found for %s type" % contextType)

        descriptor = PropertiesEditor.__descriptors[contextType]
        properties = descriptor.getProperties()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.FlexGridSizer(len(properties), 2, 9, 9)

        for name, prop in descriptor.getProperties().iteritems():
            propertyType = type(prop)
            if propertyType not in PropertiesEditor.__factories:
                raise PropertiesEditorError("No property input factory found for %s type" % propertyType)

            label = wx.StaticText(self, label = prop.getLabel())

            value = getattr(context, name)
            ctrl = PropertiesEditor.__factories[propertyType](self, prop, value)

            sizer.Add(label, flag = wx.ALIGN_RIGHT)
            sizer.Add(ctrl, proportion = 1, flag = wx.EXPAND)

        sizer.AddGrowableCol(1, 1)
        hbox.Add(sizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 9)

        self.SetSizer(hbox)

    def update(self, context):
        raise NotImplementedError()
#        for child in self.__inputs():

    def __inputs(self):
        return (child for child in self.getChildren() if type(child) is not wx.StaticText);

    @classmethod
    def registerType(cls, contextType, descriptor, policy = NoopPolicy()):
        cls.__descriptors[contextType] = descriptor

    @classmethod
    def registerFactory(cls, propertyType, factory):
        cls.__factories[propertyType] = factory
