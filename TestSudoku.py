import unittest
from Pydoku import *
import os

class Test(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.gui = SudokuGUI(self.root)
        self.mainWindow = MainWindow(self.gui.master, self.gui)

    def tearDown(self):
        self.root.quit()
        if os.path.exists('tempFile.sdk'):
            os.remove('tempFile.sdk')

    def testAttach(self):
        
        self.assertIn(self.mainWindow, self.gui.observers,"Attached succesfully!")
        
    def testDetach(self):
        
        self.mainWindow.onClose()
        self.assertNotIn(self.mainWindow, self.gui.observers, "Detached succesfully!")
        
    def testNotifyAndUpdate(self):
        
        tempWindow1 = MainWindow(self.gui.master, self.gui)
        tempWindow2 = RowWindow(self.gui.master, self.gui, 0, 0)
        
        self.gui.enterValue((0,0), 5)
        
        self.assertEqual(int(tempWindow1.canvas.itemcget(tempWindow1.text[(0,0)],"text")),5, "First window updated itself!")
        self.assertEqual(int(tempWindow2.canvas.itemcget(tempWindow2.text[(0,0)],"text")),5, "Second window updated itself!")
        
    def testEnterValueCommand(self):
        
        self.gui.getState().state[(1,1)] = 5
        
        tempCommand = EnterValueCommand(self.gui.getState(), (1,1), 4)
        
        tempCommand.execute()
        self.assertEqual(self.gui.getState().state[(1,1)], 4, "Command executed succesfully!")
        
        tempCommand.undo()
        self.assertEqual(self.gui.getState().state[(1,1)], 5, "Command undone succesfully!")
        
        tempCommand.redo()
        self.assertEqual(self.gui.getState().state[(1,1)], 4, "Command redone succesfully!")
        
    def testLoadAndSave(self):
        
        tempState = SudokuBoardState()
        tempState.generate() #Generation takes a bit longer
        saveVisitor = SaveVisitor("tempFile.sdk")
        tempState.accept(saveVisitor)
        
        newState = SudokuBoardState()
        loadVisitor = LoadVisitor("tempFile.sdk")
        newState.accept(loadVisitor)
        
        self.assertEqual(tempState.state, newState.state, "Generated state and loaded state are same!")
        
if __name__ == "__main__":
    unittest.main()
