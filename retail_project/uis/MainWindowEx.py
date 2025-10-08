from PyQt6.QtWidgets import QMessageBox
from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.uis.MainWindow import Ui_MainWindow

class LoginMainWindowEx(Ui_MainWindow):
    def __init__(self, MainWindow):  # Thêm tham số MainWindow
        super().__init__()
        self.MainWindow = MainWindow

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)

    def process_login(self):
        email = self.lineEditEmail.text()
        pwd = self.lineEditPassword.text()

        # Tạo đối tượng EmployeeConnector và thực hiện kết nối
        ec = EmployeeConnector()
        try:
            ec.connect()  # Kiểm tra kết nối cơ sở dữ liệu
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(f"Connection failed: {e}")
            msg.setWindowTitle("Connection Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        # Thực hiện đăng nhập
        em = ec.login(email, pwd)

        # Kiểm tra kết quả đăng nhập và hiển thị thông báo
        msg = QMessageBox()

        if em is None:
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Login Failed, please check your account again")
            msg.setWindowTitle("Login Failed")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            msg.setIcon(QMessageBox.Icon.Information)  # Đổi biểu tượng thành thông tin khi thành công
            msg.setText("Congratulations! Login Successful!!!")
            msg.setWindowTitle("Login OK")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg.exec()  # Hiển thị hộp thoại
