from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
import psycopg2
from psycopg2 import sql
from manage_grant_UI import Ui_manage_grant


class ManageGrant(QMainWindow, Ui_manage_grant):
    def __init__(self):
        super(ManageGrant, self).__init__()
        self.setupUi(self)

        # 数据库连接与游标
        self.connection = None
        self.cur_data_base = None

        # 连接按钮与函数
        self.btn_grant_select.clicked.connect(self.grant_select)
        self.btn_grant_edit.clicked.connect(self.grant_edit)
        self.btn_revoke_select.clicked.connect(self.revoke_select)
        self.btn_revoke_edit.clicked.connect(self.revoke_edit)

    def set_connection(self, conn, cur):
        print("连接数据库及游标")
        self.connection = conn
        self.cur_data_base = cur
        self.btn_grant_select.setEnabled(True)
        self.btn_revoke_select.setEnabled(True)
        self.btn_grant_edit.setEnabled(True)
        self.btn_revoke_edit.setEnabled(True)

    def logout(self):
        self.btn_grant_select.setEnabled(False)
        self.btn_revoke_select.setEnabled(False)
        self.btn_grant_edit.setEnabled(False)
        self.btn_revoke_edit.setEnabled(False)

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information if title == "成功" else QMessageBox.Critical)
        msg_box.exec_()

    def grant_select(self):
        username = self.line_username.text()

        if not username:
            self.show_message_box("错误", "用户名不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("GRANT package_check TO {}").format(sql.Identifier(username)))
            self.connection.commit()
            self.show_message_box("成功", "授予查询权限成功")
        except psycopg2.errors.UndefinedObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户不存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限授予查询权限")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")

    def revoke_select(self):
        username = self.line_username.text()

        if not username:
            self.show_message_box("错误", "用户名不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("REVOKE package_check FROM {}").format(sql.Identifier(username)))
            self.connection.commit()
            self.show_message_box("成功", "收回查询权限成功")
        except psycopg2.errors.UndefinedObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户不存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限收回查询权限")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")

    def grant_edit(self):
        username = self.line_username.text()

        if not username:
            self.show_message_box("错误", "用户名不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("GRANT package_edit TO {}").format(sql.Identifier(username)))
            self.connection.commit()
            self.show_message_box("成功", "授予修改权限成功")
        except psycopg2.errors.UndefinedObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户不存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限授予修改权限")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")

    def revoke_edit(self):
        username = self.line_username.text()

        if not username:
            self.show_message_box("错误", "用户名不能为空")
            return

        try:
            self.cur_data_base.execute(sql.SQL("REVOKE package_edit FROM {}").format(sql.Identifier(username)))
            self.connection.commit()
            self.show_message_box("成功", "收回修改权限成功")
        except psycopg2.errors.UndefinedObject:
            self.connection.rollback()
            self.show_message_box("错误", "用户不存在")
        except psycopg2.errors.InsufficientPrivilege:
            self.connection.rollback()
            self.show_message_box("错误", "当前用户没有权限收回修改权限")
        except Exception as e:
            self.connection.rollback()
            self.show_message_box("错误", f"发生错误: {str(e)}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ManageGrant()
    MainWindow.show()
    sys.exit(app.exec_())
