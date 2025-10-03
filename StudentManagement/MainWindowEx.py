import base64
import traceback
import mysql.connector
from pathlib import Path

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QTableWidgetItem, QFileDialog, QMessageBox, QAbstractItemView
)
from MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.BASE_DIR = Path(__file__).resolve().parent
        self.default_avatar = str(self.BASE_DIR / "img" / "ic_no_avatar.png")
        self.logo_path = self.BASE_DIR / "img" / "ic_logo.png"

        self.conn = None
        self.id = None
        self.code = None
        self.name = None
        self.age = None
        self.avatar = None  # base64-encoded bytes or None
        self.intro = None

    # -------------------- UI --------------------
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Dock icon (macOS title bar không show icon)
        if self.logo_path.exists():
            self.MainWindow.setWindowIcon(QIcon(str(self.logo_path)))

        # Cấu hình bảng
        self.tableWidgetStudent.setColumnCount(4)
        self.tableWidgetStudent.setHorizontalHeaderLabels(["ID", "Code", "Name", "Age"])
        self.tableWidgetStudent.setSelectionBehavior(self.tableWidgetStudent.SelectionBehavior.SelectRows)
        self.tableWidgetStudent.setSelectionMode(self.tableWidgetStudent.SelectionMode.SingleSelection)
        self.tableWidgetStudent.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidgetStudent.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetStudent.setSortingEnabled(True)  # cho phép sort khi click header

        # CHỈ load detail khi user tương tác
        self.tableWidgetStudent.cellClicked.connect(self.onCellClicked)       # click chuột
        self.tableWidgetStudent.itemActivated.connect(self.onItemActivated)   # Enter/phím

        # Buttons
        self.pushButtonNew.clicked.connect(self.onNewClicked)                 # <-- NEW: nút New
        self.pushButtonAvatar.clicked.connect(self.pickAvatar)
        self.pushButtonRemoveAvatar.clicked.connect(self.removeAvatar)
        self.pushButtonInsert.clicked.connect(self.processInsert)
        self.pushButtonUpdate.clicked.connect(self.processUpdate)
        self.pushButtonRemove.clicked.connect(self.processRemove)

        # ID read-only
        if hasattr(self, "lineEditId"):
            self.lineEditId.setReadOnly(True)

        # Form rỗng + ảnh mặc định lúc mở
        self.clearData()

    def show(self):
        self.MainWindow.show()

    def _setDefaultAvatarToLabel(self):
        pm = QPixmap(self.default_avatar)
        if pm.isNull():
            print(f"[WARN] Không nạp được ảnh default: {self.default_avatar}")
            self.labelAvatar.clear()
        else:
            self.labelAvatar.setScaledContents(True)
            self.labelAvatar.setPixmap(pm)

    # -------------------- MySQL --------------------
    def connectMySQL(self):
        server = "localhost"
        port = 3306
        database = "studentmanagement"
        username = "root"
        password = "@Obama123"

        self.conn = mysql.connector.connect(
            host=server, port=port, database=database, user=username, password=password
        )

    # -------------------- Load bảng --------------------
    def selectAllStudent(self):
        cursor = self.conn.cursor()
        # Thứ tự tăng dần theo ID
        cursor.execute("SELECT Id, Code, Name, Age FROM student ORDER BY Id ASC")
        rows = cursor.fetchall()
        cursor.close()

        self.tableWidgetStudent.setRowCount(0)
        for r in rows:
            row = self.tableWidgetStudent.rowCount()
            self.tableWidgetStudent.insertRow(row)
            self.tableWidgetStudent.setItem(row, 0, QTableWidgetItem(str(r[0]) if r[0] is not None else ""))
            self.tableWidgetStudent.setItem(row, 1, QTableWidgetItem(r[1] if r[1] is not None else ""))
            self.tableWidgetStudent.setItem(row, 2, QTableWidgetItem(r[2] if r[2] is not None else ""))
            self.tableWidgetStudent.setItem(row, 3, QTableWidgetItem(str(r[3]) if r[3] is not None else ""))

        # KHÔNG auto-select, để form trống chờ user chọn
        self.clearData()

    # -------------------- Bảng → Form (chỉ khi user chọn) --------------------
    def onCellClicked(self, row, col):
        self.loadDetailByRow(row)

    def onItemActivated(self, item):
        self.loadDetailByRow(item.row())

    def loadDetailByRow(self, row: int):
        try:
            id_item = self.tableWidgetStudent.item(row, 0)
            if id_item is None:
                return
            id_text = (id_item.text() or "").strip()
            if not id_text:
                return
            student_id = int(id_text)

            cursor = self.conn.cursor()
            cursor.execute("SELECT Id, Code, Name, Age, Avatar, Intro FROM student WHERE Id=%s", (student_id,))
            rec = cursor.fetchone()
            cursor.close()
            if not rec:
                return

            self.id, self.code, self.name, self.age, self.avatar, self.intro = rec

            self.lineEditId.setText(str(self.id) if self.id is not None else "")
            self.lineEditCode.setText(self.code or "")
            self.lineEditName.setText(self.name or "")
            self.lineEditAge.setText(str(self.age) if self.age is not None else "")
            self.lineEditIntro.setText(self.intro or "")

            # Avatar
            if self.avatar:
                raw = bytes(self.avatar)  # phòng khi là memoryview
                try:
                    imgdata = base64.b64decode(raw)
                    pm = QPixmap()
                    if pm.loadFromData(imgdata):
                        self.labelAvatar.setScaledContents(True)
                        self.labelAvatar.setPixmap(pm)
                    else:
                        self._setDefaultAvatarToLabel()
                except Exception:
                    traceback.print_exc()
                    self._setDefaultAvatarToLabel()
            else:
                self._setDefaultAvatarToLabel()
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không đọc được bản ghi đã chọn.")

    # -------------------- Helper: sinh Code tiếp theo --------------------
    def _next_code(self) -> str:
        """Tạo code kiểu sv01, sv02... dựa trên dữ liệu hiện có (nếu để trống)."""
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(CAST(SUBSTRING(Code, 3) AS UNSIGNED)) FROM student WHERE Code LIKE 'sv%'")
        maxnum = cur.fetchone()[0] or 0
        cur.close()
        return f"sv{maxnum + 1:02d}"

    # -------------------- Avatar --------------------
    def pickAvatar(self):
        filters = "Image Files (*.png *.jpg *.jpeg *.webp *.bmp);;All files (*)"
        filename, _ = QFileDialog.getOpenFileName(self.MainWindow, "Chọn ảnh đại diện", "", filters)
        if not filename:
            return
        pm = QPixmap(filename)
        if pm.isNull():
            QMessageBox.warning(self.MainWindow, "Ảnh lỗi", "Không mở được ảnh đã chọn.")
            return
        self.labelAvatar.setScaledContents(True)
        self.labelAvatar.setPixmap(pm)
        with open(filename, "rb") as f:
            self.avatar = base64.b64encode(f.read())

    def removeAvatar(self):
        self.avatar = None
        self._setDefaultAvatarToLabel()

    # -------------------- CRUD --------------------
    def processInsert(self):
        try:
            self.code = (self.lineEditCode.text() or "").strip()
            self.name = (self.lineEditName.text() or "").strip()
            age_text = (self.lineEditAge.text() or "").strip()
            self.intro = self.lineEditIntro.text() or ""

            # Tự sinh code nếu để trống
            if not self.code:
                self.code = self._next_code()

            self.age = int(age_text) if age_text else None
            if not hasattr(self, "avatar"):
                self.avatar = None

            sql = "INSERT INTO student (Code, Name, Age, Avatar, Intro) VALUES (%s, %s, %s, %s, %s)"
            val = (self.code, self.name, self.age, self.avatar, self.intro)

            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            self.conn.commit()
            self.lineEditId.setText(str(cursor.lastrowid))
            cursor.close()

            self.selectAllStudent()  # nạp lại bảng, form sẽ rỗng theo đúng yêu cầu
            QMessageBox.information(self.MainWindow, "Thành công", "Đã thêm 1 sinh viên.")
        except ValueError:
            QMessageBox.warning(self.MainWindow, "Giá trị sai", "Age phải là số nguyên.")
        except Exception:
            traceback.print_exc()
            QMessageBox.critical(self.MainWindow, "Lỗi", "Chèn dữ liệu thất bại.")

    def processUpdate(self):
        try:
            id_text = (self.lineEditId.text() or "").strip()
            if not id_text:
                QMessageBox.warning(self.MainWindow, "Thiếu ID", "Hãy chọn bản ghi để cập nhật.")
                return
            self.id = int(id_text)

            self.code = (self.lineEditCode.text() or "").strip()
            self.name = (self.lineEditName.text() or "").strip()
            age_text = (self.lineEditAge.text() or "").strip()
            self.age = int(age_text) if age_text else None
            self.intro = self.lineEditIntro.text() or ""
            if not hasattr(self, "avatar"):
                self.avatar = None

            sql = "UPDATE student SET Code=%s, Name=%s, Age=%s, Avatar=%s, Intro=%s WHERE Id=%s"
            val = (self.code, self.name, self.age, self.avatar, self.intro, self.id)

            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            self.conn.commit()
            cursor.close()

            self.selectAllStudent()  # reload bảng; form rỗng theo đúng hành vi
            QMessageBox.information(self.MainWindow, "Thành công", "Đã cập nhật sinh viên.")
        except ValueError:
            QMessageBox.warning(self.MainWindow, "Giá trị sai", "Age phải là số nguyên.")
        except Exception:
            traceback.print_exc()
            QMessageBox.critical(self.MainWindow, "Lỗi", "Cập nhật dữ liệu thất bại.")

    def processRemove(self):
        id_text = (self.lineEditId.text() or "").strip()
        if not id_text:
            QMessageBox.warning(self.MainWindow, "Thiếu ID", "Hãy chọn bản ghi để xoá.")
            return

        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Confirmation Deleting")
        dlg.setText("Are you sure you want to delete?")
        dlg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        if dlg.exec() == QMessageBox.StandardButton.No:
            return

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM student WHERE Id=%s", (id_text,))
        self.conn.commit()
        cursor.close()

        self.selectAllStudent()
        self.clearData()
        QMessageBox.information(self.MainWindow, "Thành công", "Đã xoá sinh viên.")

    # -------------------- NEW --------------------
    def onNewClicked(self):
        """Xoá dữ liệu form để nhập mới (theo yêu cầu nút New)."""
        self.clearData()
        # Đưa con trỏ vào ô Code để gõ ngay
        if hasattr(self, "lineEditCode"):
            self.lineEditCode.setFocus()

    # -------------------- Utilities --------------------
    def clearData(self):
        # Xoá sạch form, reset state nội bộ & trả ảnh mặc định
        self.id = None
        self.code = None
        self.name = None
        self.age = None
        self.avatar = None
        self.intro = None

        self.lineEditId.clear()
        self.lineEditCode.clear()
        self.lineEditName.clear()
        self.lineEditAge.clear()
        self.lineEditIntro.clear()
        self._setDefaultAvatarToLabel()


# -------------------- MAIN --------------------
if __name__ == "__main__":
    import sys
    from PyQt6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    # Dock icon (đặc biệt hữu ích trên macOS)
    base_dir = Path(__file__).resolve().parent
    logo = base_dir / "img" / "ic_logo.png"
    if logo.exists():
        app.setWindowIcon(QIcon(str(logo)))

    win = QtWidgets.QMainWindow()
    ui = MainWindowEx()
    ui.setupUi(win)

    try:
        ui.connectMySQL()
        ui.selectAllStudent()
    except Exception:
        sys.exit(1)

    win.show()
    sys.exit(app.exec())
