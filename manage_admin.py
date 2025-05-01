from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
import psycopg2
from psycopg2 import sql
from manage_admin_UI import Ui_manage_admin_window

class ManageAdmin(QMainWindow, Ui_manage_admin_window):
    def __init__(self):
        super(ManageAdmin, self).__init__()
        self.setupUi(self)

        # 数据库连接与游标
        self.connection = None
        self.cur_data_base = None

        self.logout()

        # 连接按钮与函数
        self.btn_create.clicked.connect(self.create_admin)
        self.btn_edit.clicked.connect(self.edit_admin)
        self.btn_delete.clicked.connect(self.delete_admin)

    def set_connection(self, conn, cur):
        print("连接数据库及游标")
        self.connection = conn
        self.cur_data_base = cur
        self.btn_create.setEnabled(True)
        self.btn_delete.setEnabled(True)
        self.btn_edit.setEnabled(True)

    def logout(self):
        self.btn_create.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_edit.setEnabled(False)

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information if title == "成功" else QMessageBox.Critical)
        msg_box.exec_()

    def create_admin(self):
        username = self.line_username.text()
        password = self.line_password.text()

        if not username or not password:
            self.show_message_box("错误", "用户名和密码不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(username)), [password])
            self.connection.commit()
            self.show_message_box("成功", "用户创建成功")
        except psycopg2.errors.DuplicateObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户已存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限创建用户")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")

    def edit_admin(self):
        username = self.line_username.text()
        password = self.line_password.text()

        if not username or not password:
            self.show_message_box("错误", "用户名和密码不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("ALTER USER {} WITH PASSWORD %s").format(sql.Identifier(username)), [password])
            self.connection.commit()
            self.show_message_box("成功", "密码修改成功")
        except psycopg2.errors.UndefinedObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户不存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限修改用户")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")

    def delete_admin(self):
        username = self.line_username.text()

        if not username:
            self.show_message_box("错误", "用户名不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("DROP USER {}").format(sql.Identifier(username)))
            self.connection.commit()
            self.show_message_box("成功", "用户删除成功")
        except psycopg2.errors.UndefinedObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户不存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限删除用户")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ManageAdmin()
    mainWindow.show()
    sys.exit(app.exec_())
