from retail_project.uis.MainWindow import Ui_MainWindow

class LoginMainWindowEx(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def showWindow(self):
        self.MainWindow.show()
