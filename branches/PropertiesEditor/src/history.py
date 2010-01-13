class Command(object):
    def getName(self):
        raise NotImplementedError()

    def execute(self):
        raise NotImplementedError()

    def undo(self):
        raise NotImplementedError()

    def redo(self):
        raise NotImplementedError()

class MetaCommand(Command):
    def __init__(self, name, commands = list()):
        Command.__init__(self, name)
        self.__commands = commands

    def execute(self):
        for command in self.__commands:
            command.execute()

    def undo(self):
        for command in self.__commands:
            command.undo()

    def redo(self):
        for command in self.__commands.reverse():
            command.redo()
        
class History(object):
    def __init__(self):
        self.__commands = list()
        self.__offset = 0

    def execute(self, command):
        if self.__offset:
             # remove newer actions
             del self.__commands[:self.__offset]
             self.__offset -= 1
        # insert command at beginning
        self.__commands.insert(0, command)
        command.execute()

    def getCommands(self):
        return self.__commands

    def undo(self):
        if self.__offset < len(self.__commands):
            self.__commands[self.__offset].undo()    
            self.__offset += 1
    
   
    def redo(self):
        if self.__offset > 0:
            self.__offset -= 1
            self.__commands[self.__offset].redo()

class SetPropertyCommand(Command):
    def __init__(self, object, property, value, label = None):
        self.__object = object
        self.__property = property
        self.__oldValue = getattr(object, property)
        self.__newValue = value;
        self.__label = label if label else property.capitalize()

    def getName(self):
        return "Set %s of %s" % (self.__label, self.__object.__class__.__name__)

    def execute(self):
        setattr(self.__object, self.__property, self.__newValue)

    def undo(self):
        setattr(self.__object, self.__property, self.__oldValue)

    def redo(self):
        setattr(self.__object, self.__property, self.__newValue)
