class Command(object):
    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def undo(self):
        raise NotImplementedError()

    def redo(self):
        raise NotImplementedError()

class MetaCommand(Command):
    def __init__(self, name, commands = list()):
        Command.__init__(self, name)
        self.__commands = commands

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

    def addCommand(self, command):
        if self.__offset:
             # remove newer actions
             del self.__commands[:self.__offset]
        # insert command at beginning
        self.__commands.insert(0, command)

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
