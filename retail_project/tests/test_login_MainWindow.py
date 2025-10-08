from PyQt6.QtWidgets import QApplication, QMainWindow
from retail_project.uis.MainWindowEx import LoginMainWindowEx

app = QApplication([])
main_window = QMainWindow()
login_ui = LoginMainWindowEx(main_window)
login_ui.setupUi(main_window)
login_ui.showWindow()

app.exec()
