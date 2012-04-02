class Property(object):
    def __init__(self, label = None, validatorType = None):
        self.__label = label
        self.__validatorType = validatorType

    def getLabel(self):
        return self.__label

    def setLabel(self, label):
        self.__label = label

    def getInputType(self):
        return self.__inputType

    def getValidatorType(self):
        return self.__validatorType 

class TextProperty(Property):
    def __init__(self, label = None, maxLength = 0, validatorType = None):
        Property.__init__(self, label, validatorType)
        self.__maxLength = maxLength

    def getMaxLength(self):
        return self.__maxLength

class IntegerProperty(Property):
    def __init__(self, label = None, range = None):
        Property.__init__(self, label)
        self.__range = range

    def getRange(self):
        return self.__range

class PropertiesBase(type):
    """
    Metaclass used for filling properties labels
    """

    def __new__(cls, name, bases, data):
        properties = dict() 

        for (key, value) in data.iteritems():
            if isinstance(value, Property):
                if not value.getLabel():
                    value.setLabel(key.capitalize())
                properties[key] = value

        data['_properties'] = properties

        return type.__new__(cls, name, bases, data)

class Properties(object):
    __metaclass__ = PropertiesBase

    @classmethod
    def getProperties(cls):
        return cls._properties

if __name__ == "__main__":

    class Point(object):
        def __init__(self, x, y):
            self.__x = x
            self.__y = y

        x = property(lambda self: self.__x)
        y = property(lambda self: self.__y)

    class PointProperties(Properties):
        x = IntegerProperty(range = (0, 100))
        y = IntegerProperty()

    print PointProperties.x.getLabel()
