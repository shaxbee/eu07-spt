from history import History, Command, SetPropertyCommand
import unittest

class DummyCommand(Command):
    def __init__(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def undo(self):
        pass

    def redo(self):
        pass

    def execute(self):
        pass

class DummyData(object):
    def __init__(self, value):
        self.__value = value

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    value = property(getValue, setValue)

class HistoryTestCase(unittest.TestCase):
    def setUp(self):
        self.history = History()

    def testExecute(self):
        self.history.execute(DummyCommand("first"))
        cmd = self.history.getCommands()[0];
        self.assertEqual(cmd.getId(), "first")

        self.history.execute(DummyCommand("second"))
        cmd = self.history.getCommands()[0];
        self.assertEqual(cmd.getId(), "second")

        self.history.undo()
        self.history.execute(DummyCommand("third"))
        cmd = self.history.getCommands()[1];
        self.assertEqual(len(self.history.getCommands()), 2)
        self.assertEqual(cmd.getId(), "first")

    def testUndo(self):
        data = DummyData(0);

        self.history.execute(SetPropertyCommand(data, "value", 1))
        self.assertEqual(data.value, 1)
        self.history.undo()
        self.assertEqual(data.value, 0)

        self.history.execute(SetPropertyCommand(data, "value", 2))
        self.history.execute(SetPropertyCommand(data, "value", 3))
        self.assertEqual(len(self.history.getCommands()), 2)
        self.history.undo()
        self.assertEqual(data.value, 2)
        self.history.undo()
        self.assertEqual(data.value, 0)

if __name__ == "__main__":
    unittest.main()
