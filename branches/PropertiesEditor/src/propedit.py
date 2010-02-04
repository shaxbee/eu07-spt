class PropertesEdtitorError(NameError):
    pass

class PropertiesEditor(wx.Panel):
    __descriptors = dict()

    def __init__(self, context):
        contextCls = context.__class__.__name__

        if not contextCls in self.__descriptors:
            raise PropertiesEditorError("Properties descriptor for %s not found")

        self.__descriptor = self.__descriptors[contextCls]
        self.__createControls()

    @classmethod
    def register(cls, contextCls, descriptorCls):
        cls.__descriptors[contextCls] = descriptorCls

