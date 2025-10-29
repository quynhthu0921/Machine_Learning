from PyQt6.QtWidgets import QApplication, QMainWindow
from retail_project.uis.MainWindowEx import Ui_MainWindow

app = QApplication([])

main_window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(main_window)

main_window.show()
app.exec()
