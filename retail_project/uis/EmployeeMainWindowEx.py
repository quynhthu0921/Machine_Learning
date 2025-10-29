from retail_project.uis.EmployeeMainWindow import Ui_MainWindow


class EmployeeMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
    def showWindow(self):
        self.MainWindow.show()
