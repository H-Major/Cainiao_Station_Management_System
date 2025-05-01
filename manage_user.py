from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
from PyQt5.QtGui import *
import re
import psycopg2

from manage_user_UI import Ui_MainWindow


def is_valid_phone_number(phone_number: str) -> bool:
    pattern = r"^1\d{10}$"
    return bool(re.match(pattern, phone_number))


def generate_query(userPhone):
    query = f"SELECT * FROM cainiao.users WHERE userPhone = '{userPhone}' LIMIT 1;"
    return query


class ManageUser(QMainWindow, Ui_MainWindow):
    # 构造函数
    def __init__(self):
        super(ManageUser, self).__init__()
        self.setupUi(self)

        self.userPhone = ""
        self.userName = ""

        # 数据库连接与游标
        self.connection = None
        self.cur_data_base = None

        # 按钮使能
        self.btn_create.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_rename.setEnabled(False)

        # 信号槽连接
        self.btn_rename.clicked.connect(self.rename_user)
        self.btn_delete.clicked.connect(self.delete_user)
        self.btn_create.clicked.connect(self.create_user)

    def logout(self):
        self.btn_create.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_rename.setEnabled(False)

    def set_connection(self, conn, cur):
        self.connection = conn
        self.cur_data_base = cur
        self.btn_create.setEnabled(True)
        self.btn_delete.setEnabled(True)
        self.btn_rename.setEnabled(True)

    def rename_user(self):
        Legal = True
        Error_Info = ""
        self.userPhone = ""
        self.userName = ""
        if self.line_userPhone.text() != "":
            if is_valid_phone_number(self.line_userPhone.text()):
                if self.user_exists(self.line_userPhone.text()):
                    self.userPhone = "\'" + self.line_userPhone.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "用户手机号不存在\n"
                    print("用户手机号不存在")
            else:
                Legal = False
                Error_Info += "手机号格式有误\n"
                print("手机号格式有误")
        if self.line_userName.text() == "":
            Legal = False
            Error_Info = "用户名不能为空"
        else:
            self.userName = "\'" + self.line_userName.text() + "\'"

        if Legal:
            query = ("UPDATE cainiao.users " +
                     " SET userName = " + self.userName +
                     " WHERE userPhone = " + self.userPhone +
                     ";")
            try:
                # 执行
                print("执行更新：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "重命名成功。")
            except psycopg2.Error as e:
                print(f"数据库更新错误: {e}")
        else:
            QMessageBox.warning(self, "错误", Error_Info)

    def delete_user(self):
        Legal = True
        Error_Info = ""
        self.userPhone = ""
        self.userName = ""
        if self.line_userPhone.text() != "":
            if is_valid_phone_number(self.line_userPhone.text()):
                if self.user_exists(self.line_userPhone.text()):
                    self.userPhone = "\'" + self.line_userPhone.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "用户手机号不存在\n"
            else:
                Legal = False
                Error_Info += "手机号格式有误\n"
        if Legal:
            query = ("DELETE FROM cainiao.users " +
                     " WHERE userPhone = " + self.userPhone +
                     ";")

            query += ("DELETE FROM cainiao.storage " +
                      " WHERE userPhone = " + self.userPhone +
                      ";")
            try:
                # 执行
                print("执行删除：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "用户删除成功。")
            except psycopg2.Error as e:
                print(f"数据库更新错误: {e}")
        else:
            QMessageBox.warning(self, "错误", Error_Info)

    def create_user(self):
        Legal = True
        Error_Info = ""
        self.userPhone = ""
        self.userName = ""
        if self.line_userPhone.text() != "":
            if is_valid_phone_number(self.line_userPhone.text()):
                if not self.user_exists(self.line_userPhone.text()):
                    self.userPhone = "\'" + self.line_userPhone.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "用户手机号已存在\n"
            else:
                Legal = False
                Error_Info += "手机号格式有误\n"
        if self.line_userName.text() == "":
            Legal = False
            Error_Info = "用户名不能为空"
        else:
            self.userName = "\'" + self.line_userName.text() + "\'"

        if Legal:
            query = ("INSERT INTO cainiao.users VALUES(" + self.userPhone + " , " + self.userName + ");")
            try:
                # 执行
                print("执行更新：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "用户创建成功。")
            except psycopg2.Error as e:
                print(f"数据库更新错误: {e}")
        else:
            QMessageBox.warning(self, "错误", Error_Info)

    def user_exists(self, userPhone):
        query = generate_query(userPhone)
        try:
            self.cur_data_base.execute(query)
            result = self.cur_data_base.fetchone()
            return result is not None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False
