from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
from PyQt5.QtGui import *
import sys
import psycopg2
import ipaddress
import re
import time

from manage_grant import ManageGrant
from window_UI import Ui_MainWindow
from manage_user import ManageUser
from manage_package import ManagePackage
from manage_admin import ManageAdmin

from UsersCreater import *
from PackagesCreater import *

create_ui = ["python -m PyQt5.uic.pyuic window.ui -o window_UI.py ",
             "python -m PyQt5.uic.pyuic manage_user.ui -o manage_user_UI.py ",
             "python -m PyQt5.uic.pyuic manage_package.ui -o manage_package_UI.py ",
             "python -m PyQt5.uic.pyuic manage_admin.ui -o manage_admin_UI.py ",
             "python -m PyQt5.uic.pyuic manage_grant.ui -o manage_grant_UI.py "
            ]
def generate_where_clause(expressions):
    if not expressions:
        return ""
    where_clause = " AND ".join(expressions)
    return f"WHERE {where_clause}"


def is_valid_num(num: str) -> bool:
    return num.isalnum()


def is_valid_id(id_str: str) -> bool:
    return id_str.isdigit() and len(id_str) == 20


def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def is_valid_phone_number(phone_number: str) -> bool:
    pattern = r"^1\d{10}$"
    return bool(re.match(pattern, phone_number))


def is_valid_code(code):
    parts = code.split('-')
    if len(parts) != 3:
        return False, None, None, None
    try:
        x, y, z = map(int, parts)
        if z != 0 and (x == 0 or y == 0):
            return False, None, None, None
        elif (y != 0) and (x == 0):
            return False, None, None, None
        elif y == 0 and x == 0 and z == 0:
            return False, None, None, None
        elif y > 9 or z > 9999:
            return False, None, None, None
        else:
            return True, x, y, z
    except ValueError:
        return False, None, None, None


class CaiNiaoWindow(QMainWindow, Ui_MainWindow):
    # 构造函数
    def __init__(self):
        super(CaiNiaoWindow, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("icon.ico"))

        # 开关变量 是否已连接数据库
        self.Logged_In = False

        # 输入信息 数据库连接
        self.host = ""
        self.port = ""
        self.database = ""
        self.user = ""
        self.password = ""
        self.CONFIG_FILE = "./config/config_file.txt"

        # 数据库连接与游标
        self.connection = None
        self.cur_data_base = None

        # 信号槽连接
        # 按钮
        self.btn_connect.clicked.connect(self.connect_clicked)  # 连接
        self.btn_disconnect.clicked.connect(self.disconnect_clicked)  # 断开连接
        self.btn_select_package.clicked.connect(self.select_package_clicked)  # 查询包裹
        self.btn_select_user.clicked.connect(self.select_user_clicked)  # 查询用户
        self.btn_out.clicked.connect(self.package_out)
        self.btn_up.clicked.connect(self.range_up)
        self.btn_down.clicked.connect(self.range_down)
        # 菜单栏-视图
        self.ac_userName.triggered.connect(self.check_ac_userName)
        self.ac_packageName.triggered.connect(self.check_ac_packageName)
        self.ac_company.triggered.connect(self.check_ac_company)
        self.ac_expressNum.triggered.connect(self.check_ac_expressNum)
        self.ac_information.triggered.connect(self.check_ac_information)
        self.ac_sendName.triggered.connect(self.check_ac_sendName)
        self.ac_sendAddress.triggered.connect(self.check_ac_sendAddress)
        self.ac_receiveName.triggered.connect(self.check_ac_receiveName)
        self.ac_receiveAddress.triggered.connect(self.check_ac_receiveAddress)
        self.ac_putDate.triggered.connect(self.check_ac_putDate)
        # checkBox
        self.check_have_package.clicked.connect(self.check_have_package_clicked)
        # menu
        self.action_manage_user.triggered.connect(self.action_manage_user_clicked)
        self.action_manage_package.triggered.connect(self.action_manage_package_clicked)
        self.action_sql.triggered.connect(self.quick_insert_from_txt)
        self.action_ran_gen_package.triggered.connect(self.action_ran_gen_package_clicked)
        self.action_ran_gen_user.triggered.connect(self.action_ran_gen_user_clicked)
        self.action_delete_all.triggered.connect(self.delete_all)
        self.action_count_package.triggered.connect(self.action_count_package_clicked)
        self.action_count_user.triggered.connect(self.action_count_user_clicked)
        self.action_count_shelf.triggered.connect(self.action_count_shelf_clicked)
        self.action_check_all.triggered.connect(self.action_check_all_clicked)
        self.action_manage_admin.triggered.connect(self.action_manage_admin_clicked)
        self.action_manage_grant.triggered.connect(self.action_manage_grant_clicked)

        # 窗口初始化
        self.window_init()

        # 视图-开关变量
        self.check_userName = True
        self.check_packageName = True
        self.check_company = False
        self.check_expressNum = True
        self.check_information = False
        self.check_sendName = False
        self.check_sendAddress = False
        self.check_receiveName = True
        self.check_receiveAddress = False
        self.check_putDate = True

        # 查询数据
        self.userPhone = ""
        self.code = ""
        self.shelf = -1
        self.layer = -1
        self.num = -1
        self.id = ""
        self.expressNum = ""
        self.company = ""
        self.packageStatus = ""

        # 开关变量-是否只查询有包裹的
        self.Select_Have_Package = False

        # 用户管理界面
        self.window_manage_user = ManageUser()
        self.window_manage_user.hide()

        # 包裹管理界面
        self.window_manage_package = ManagePackage()
        self.window_manage_package.hide()

        # 管理员管理界面
        self.window_manage_admin = ManageAdmin()
        self.window_manage_admin.hide()

        # 权限管理界面
        self.window_manage_grant = ManageGrant()
        self.window_manage_grant.hide()

    def range_up(self):
        begin = int(self.line_begin.text())
        end = int(self.line_end.text())
        dert = end - begin
        begin = end
        end += dert
        self.line_begin.setText(str(begin))
        self.line_end.setText(str(end))

    def range_down(self):
        begin = int(self.line_begin.text())
        end = int(self.line_end.text())
        if begin == 0:
            return 0
        else:
            dert = end - begin
            end = begin
            begin -= dert
            if begin < 0:
                begin = 0
            self.line_begin.setText(str(begin))
            self.line_end.setText(str(end))



    def action_manage_grant_clicked(self):
        print("显示窗口:window_manage_grant")
        self.window_manage_grant.show()

    def delete_out(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            msg_box = QMessageBox()
            msg_box.setText("你确定要删除所有已取件的包裹记录吗？")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            reply = msg_box.exec()
            if reply == QMessageBox.Yes:
                query = "DELETE FROM cainiao.storage WHERE packageStatus = '已取件';"
                self.update_action(query)

    def action_manage_admin_clicked(self):
        print("显示窗口：window_manage_admin")
        self.window_manage_admin.show()

    def package_out(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            Legal = True
            Error_Info = ""
            if self.line_code_out.text() == "":
                Legal = False
                Error_Info += "取件码不能为空\n"
            else:
                flag, x, y, z = is_valid_code(self.line_code_out.text())
                if not flag:
                    Legal = False
                    Error_Info += "取件码格式有误\n"
                else:
                    code = self.line_code_out.text()

            if Legal:
                try:
                    query_id = f"SELECT id FROM cainiao.packages WHERE code = '{code}';"
                    self.cur_data_base.execute(query_id)
                    result = self.cur_data_base.fetchone()
                    if result:
                        package_id = result[0]
                        print("取件id:", package_id)
                        update_status = (f"UPDATE cainiao.storage "
                                         f"SET packageStatus = '已取件' "
                                         f"WHERE id = '{package_id}';")
                        self.cur_data_base.execute(update_status)
                        self.connection.commit()
                        QMessageBox.information(self, "提示", f"包裹{code}取件成功。")
                    else:
                        print("No package found with the specified code.")
                        Error_Info += "取件码不存在"
                        QMessageBox.warning(self, "错误", Error_Info)
                except psycopg2.connector.Error as err:
                    print(f"Error: {err}")
                    self.connection.rollback()
            else:
                QMessageBox.warning(self, "错误", Error_Info)

    def action_check_all_clicked(self):
        if self.action_check_all.isChecked():
            self.check_userName = True
            self.check_packageName = True
            self.check_company = True
            self.check_expressNum = True
            self.check_information = True
            self.check_sendName = True
            self.check_sendAddress = True
            self.check_receiveName = True
            self.check_receiveAddress = True
            self.check_putDate = True
            self.ac_userPhone.setChecked(True)
            self.ac_userName.setChecked(True)
            self.ac_packageName.setChecked(True)
            self.ac_company.setChecked(True)
            self.ac_expressNum.setChecked(True)
            self.ac_information.setChecked(True)
            self.ac_sendName.setChecked(True)
            self.ac_sendAddress.setChecked(True)
            self.ac_receiveName.setChecked(True)
            self.ac_receiveAddress.setChecked(True)
            self.ac_putDate.setChecked(True)
        else:
            self.check_userName = False
            self.check_packageName = False
            self.check_company = False
            self.check_expressNum = False
            self.check_information = False
            self.check_sendName = False
            self.check_sendAddress = False
            self.check_receiveName = False
            self.check_receiveAddress = False
            self.check_putDate = False
            self.ac_userPhone.setChecked(False)
            self.ac_userName.setChecked(False)
            self.ac_packageName.setChecked(False)
            self.ac_company.setChecked(False)
            self.ac_expressNum.setChecked(False)
            self.ac_information.setChecked(False)
            self.ac_sendName.setChecked(False)
            self.ac_sendAddress.setChecked(False)
            self.ac_receiveName.setChecked(False)
            self.ac_receiveAddress.setChecked(False)
            self.ac_putDate.setChecked(False)

    def action_count_shelf_clicked(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            query = "SELECT shelf, COUNT(id) FROM cainiao.packages GROUP BY shelf ORDER BY shelf;"
            headers = ["货架号", "包裹数"]
            self.select_action(query, headers)
            self.table.setColumnWidth(0, 100)
            self.table.setColumnWidth(1, 150)

    def action_count_user_clicked(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            query = "SELECT COUNT(userPhone) FROM cainiao.users;"
            headers = ["快递站用户总数"]
            self.select_action(query, headers)
            self.table.setColumnWidth(0, 150)

    def action_count_package_clicked(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            query = "SELECT COUNT(id) FROM cainiao.storage;"
            headers = ["快递站包裹总数"]
            self.select_action(query, headers)
            self.table.setColumnWidth(0, 150)

    def select_action(self, query, headers):
        try:
            # 执行查询
            print("执行查询：\n", query)
            self.statusbar.showMessage("正在查询", 3000)
            qApp.processEvents()
            start_time = time.time()
            self.cur_data_base.execute(query)
            results = self.cur_data_base.fetchall()
            end_time = time.time()
            execution_time = end_time - start_time
            execution_time = str(round(execution_time, 1))
            self.statusbar.showMessage(f"查询完毕  用时: {execution_time}s")
            qApp.processEvents()
            print(f"查询完毕  用时: {execution_time}s")
            # 获取结果的列数
            column_count = len(self.cur_data_base.description)
            # 设置表的行数和列数
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.setRowCount(len(results))
            self.table.setColumnCount(column_count)
            # 设置表头
            self.table.setHorizontalHeaderLabels(headers)
            # 填充表数据
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except psycopg2.Error as e:
            self.connection.rollback()
            QMessageBox.warning(self, "错误", f"数据库查询错误: {e}")

    def update_action(self, query):
        try:
            print("执行SQL语句：\n", query)
            start_time = time.time()
            self.cur_data_base.execute(query)
            self.connection.commit()
            end_time = time.time()
            execution_time = end_time - start_time
            execution_time = str(int(execution_time))
            self.statusbar.showMessage(f"操作完毕  用时: {execution_time}s")
        except psycopg2.Error as e:
            QMessageBox.warning(self, "错误", f"数据库操作错误: {e}")
            self.connection.rollback()

    def gen_package(self, num_package):
        print("随机生成", num_package, "条包裹数据")
        list_userPhone = read_file_to_list('./data/userPhone.txt')
        id_count = read_line('./data/id.txt') + 1
        code_count = read_line('./data/code.txt') + 1
        query_packages = ("INSERT INTO cainiao.packages "
                          "(id, company, expressNum, packageName, information, "
                          "sendName, sendAddress, receiveName, receiveAddress, "
                          "code, shelf, layer, num, putDate) VALUES ")
        query_storage = "INSERT INTO cainiao.storage (userPhone, id, packageStatus) VALUES "
        start_time = time.time()

        for i in range(0, num_package):
            userPhone = "\'" + random.choice(list_userPhone) + "\'"
            Id = "\'" + pad_with_zeros(id_count) + "\'"
            id_count += 1
            company = random.choice(express_companies)
            expressNum = "\'" + express_num[company] + generate_random_integer_string() + "\'"
            company = "\'" + company + "\'"
            packageName = "\'" + random.choice(items) + "\'"
            information = "\'" + random.choice(remarks) + "\'"
            sendName = "\'" + fake.name() + "\'"
            sendAddress = "\'" + fake.address() + "\'"
            receiveName = "\'" + fake.name() + "\'"
            receiveAddress = "\'" + fake.address() + "\'"
            code, shelf, layer, num = generate_code(code_count)
            num = str(int(num))
            code = "\'" + code + "\'"
            code_count += 1
            putDate = "\'" + generate_random_date(2024) + "\'"
            packageStatus = "\'" + random.choice(status) + "\'"

            query_packages += ("(" + Id + ", " + company + ", " + expressNum + ", " + packageName + ", " + information + ", " +
                               sendName + ", " + sendAddress + ", " + receiveName + ", " + receiveAddress + ", " + code + ", " +
                               shelf + ", " + layer + ", " + num + ", " + putDate + ")"
                               )
            query_storage += ("(" + userPhone + ", " + Id + ", " + packageStatus + ")"
                              )
            if i != 0 and (i % 100 == 0 or i == num_package - 1):
                query_packages += ';'
                query_storage += ';'
                self.cur_data_base.execute(query_packages)
                self.cur_data_base.execute(query_storage)
                self.connection.commit()
                print(i, "/", num_package)
                elapsed_time = time.time() - start_time
                avg_time_per_iteration = elapsed_time / (i + 1)
                remaining_iterations = num_package - i - 1
                estimated_remaining_time = remaining_iterations * avg_time_per_iteration

                # 将剩余时间转换为hh:mm:ss格式
                hrs, rem = divmod(estimated_remaining_time, 3600)
                mins, secs = divmod(rem, 60)
                estimated_remaining_time_str = "{:02}:{:02}:{:02}".format(int(hrs), int(mins), int(secs))

                print("预计剩余时间：{}".format(estimated_remaining_time_str))
                self.statusbar.showMessage("正在生成包裹 " + str(i) + "/" + str(num_package) + "，预计剩余时间：{}".format(estimated_remaining_time_str))
                qApp.processEvents()
                write_line('./data/id.txt', str(id_count))
                write_line('./data/code.txt', str(code_count))
                query_packages = ("INSERT INTO cainiao.packages "
                                  "(id, company, expressNum, packageName, information, "
                                  "sendName, sendAddress, receiveName, receiveAddress, "
                                  "code, shelf, layer, num, putDate) VALUES ")
                query_storage = "INSERT INTO cainiao.storage (userPhone, id, packageStatus) VALUES "
            else:
                query_packages += ','
                query_storage += ','

        self.statusbar.showMessage("完成", 3000)

    def delete_all(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            msg_box = QMessageBox()
            msg_box.setText("你确认你知道自己在做什么？\n这将直接清空所有表中的数据！")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            reply = msg_box.exec()
            if reply == QMessageBox.Yes:
                query = ("DELETE FROM cainiao.storage;" +
                         "DELETE FROM cainiao.packages;" +
                         "DELETE FROM cainiao.users;")
                self.cur_data_base.execute(query)
                self.connection.commit()
                self.statusbar.showMessage("数据已清空。", 3000)

    def action_ran_gen_user_clicked(self):
        print("正在生成用户数据")
        u = self.gen_user(100)
        self.cur_data_base.execute(u)
        self.connection.commit()

    def action_ran_gen_package_clicked(self):
        print("正在生成包裹数据")
        self.gen_package(1000)
        print("完成")

    def gen_user(self, num_userPhone):
        print("随机生成", num_userPhone, "条用户数据")
        list_userPhone = read_file_to_list('./data/userPhone.txt')
        query = "INSERT INTO cainiao.users (userPhone, userName) VALUES "
        for i in range(0, num_userPhone):
            if i % 10 == 0:
                print(i, "/", num_userPhone)
                self.statusbar.showMessage("正在生成用户" + str(i) + "/" + str(num_userPhone))
                qApp.processEvents()
            while True:
                userPhone = fake.phone_number()
                if userPhone not in list_userPhone:
                    break
            list_userPhone.append(userPhone)
            insert_string_to_file('./data/userPhone.txt', userPhone)
            userName = fake.name()
            query += '(\'' + userPhone + '\', \'' + userName + '\')'
            if i == num_userPhone - 1:
                query += ';'
            else:
                query += ','
        return query

    def load_sql_file(self, file):
        print("load_sql")
        line_count = 0
        with open(file, "r") as f:
            print("start_load_sql")
            for line in f:
                self.cur_data_base.execute(line)
                print(line)
                line_count += 1
                self.statusbar.showMessage("正在导入文件  " + str(line_count), 1)
                qApp.processEvents()
            self.connection.commit()
            self.statusbar.showMessage("文件导入完成。", 3000)

    def quick_insert_from_txt(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            pth, file = QFileDialog.getOpenFileName()
            if pth:
                msg_box = QMessageBox()
                msg_box.setText("你确认你知道自己在做什么？\n这将直接执行文件内的SQL语句！")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.Yes)
                reply = msg_box.exec()
                if reply == QMessageBox.Yes:
                    self.load_sql_file(pth)

    def action_manage_user_clicked(self):
        print("debug:显示窗口")
        self.window_manage_user.show()
        self.window_manage_user.raise_()

    def action_manage_package_clicked(self):
        print("debug:显示窗口")
        self.window_manage_package.show()
        self.window_manage_package.raise_()

    def check_have_package_clicked(self):
        if self.check_have_package.isChecked():
            self.Select_Have_Package = True
        else:
            self.Select_Have_Package = False

    def check_ac_userName(self):
        if self.ac_userName.isChecked():
            self.check_userName = True
        else:
            self.check_userName = False

    def check_ac_packageName(self):
        if self.ac_packageName.isChecked():
            self.check_packageName = True
        else:
            self.check_packageName = False

    def check_ac_company(self):
        if self.ac_company.isChecked():
            self.check_company = True
        else:
            self.check_company = False

    def check_ac_expressNum(self):
        if self.ac_expressNum.isChecked():
            self.check_expressNum = True
        else:
            self.check_expressNum = False

    def check_ac_information(self):
        if self.ac_information.isChecked():
            self.check_information = True
        else:
            self.check_information = False

    def check_ac_sendName(self):
        if self.ac_sendName.isChecked():
            self.check_sendName = True
        else:
            self.check_sendName = False

    def check_ac_sendAddress(self):
        if self.ac_sendAddress.isChecked():
            self.check_sendAddress = True
        else:
            self.check_sendAddress = False

    def check_ac_receiveName(self):
        if self.ac_receiveName.isChecked():
            self.check_receiveName = True
        else:
            self.check_receiveName = False

    def check_ac_receiveAddress(self):
        if self.ac_receiveAddress.isChecked():
            self.check_receiveAddress = True
        else:
            self.check_receiveAddress = False

    def check_ac_putDate(self):
        if self.ac_putDate.isChecked():
            self.check_putDate = True
        else:
            self.check_putDate = False

    def select_user_clicked(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            Legal = True
            Error_Info = ""
            self.userPhone = ""
            if self.line_userPhone.text() != "":
                if is_valid_phone_number(self.line_userPhone.text()):
                    self.userPhone = "\'" + self.line_userPhone.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "电话号格式有误\n"

            if Legal:
                self.select_user()
            else:
                QMessageBox.warning(self, "错误", Error_Info)

    def select_user(self):
        query = ("SELECT userPhone, userName, packageCount"
                 " FROM cainiao.user_package_count ")
        headers = ["手机号", "用户名", "包裹数"]
        list_where = []
        if self.userPhone != "":
            list_where.append(" user_package_count.userPhone = " + self.userPhone)
        if self.Select_Have_Package:
            list_where.append(" packageCount > 0 ")
        query += generate_where_clause(list_where)
        if self.check_range.isChecked():
            begin = int(self.line_begin.text())
            end = int(self.line_end.text())
            dert = end - begin
            query += f" LIMIT {dert} OFFSET {begin} "
        query += ";"
        self.select_action(query, headers)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 85)

    def select_package_clicked(self):
        if not self.Logged_In:
            QMessageBox.warning(self, "提示", "请先连接数据库。")
        else:
            Legal = True
            Error_Info = ""
            self.userPhone = ""
            self.code = ""
            self.shelf = 0
            self.layer = 0
            self.num = 0
            self.id = ""
            self.expressNum = ""
            self.company = ""
            self.packageStatus = ""
            # 检查电话号输入
            if self.line_userPhone.text() != "":
                if is_valid_phone_number(self.line_userPhone.text()):
                    self.userPhone = "\'" + self.line_userPhone.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "电话号格式有误\n"
            # 检查取件码输入
            if self.line_code.text() != "":
                Flag, self.shelf, self.layer, self.num = is_valid_code(self.line_code.text())
                if Flag:
                    self.code = "\'" + self.line_code.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "取件码格式有误\n"

            # 检查包裹编号输入
            if self.line_id.text() != "":
                if is_valid_id(self.line_id.text()):
                    self.id = "\'" + self.line_id.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "包裹编号格式有误\n"
            # 检查快递单号输入
            if self.line_expressNum.text() != "":
                if is_valid_num(self.line_expressNum.text()):
                    self.expressNum = "\'" + self.line_expressNum.text() + "\'"
                else:
                    Legal = False
                    Error_Info += "快递单号格式有误\n"
            # 检查快递公司输入
            if self.line_company.text() != "":
                self.company = "\'" + self.line_company.text() + "\'"
            # 检查包裹状态
            self.packageStatus = self.combo_packageStatus.currentIndex()

            # 判断是否合法
            if Legal:
                self.select_package()
            else:
                QMessageBox.warning(self, "错误", Error_Info)

    def select_package(self):
        query = "SELECT code, users.userPhone, packages.id, packageStatus"
        headers = ['取件码', '手机号', '包裹编号', '状态']
        if self.check_userName:
            query += ", userName"
            headers.append("用户名")
        if self.check_packageName:
            query += ", packageName"
            headers.append("包裹名称")
        if self.check_company:
            query += ", company"
            headers.append("快递公司")
        if self.check_expressNum:
            query += ", expressNum"
            headers.append("快递单号")
        if self.check_information:
            query += ", information"
            headers.append("包裹信息")
        if self.check_sendName:
            query += ", sendName"
            headers.append("发件人")
        if self.check_sendAddress:
            query += ", sendAddress"
            headers.append("发件地址")
        if self.check_receiveName:
            query += ", receiveName"
            headers.append("收件人")
        if self.check_receiveAddress:
            query += ", receiveAddress"
            headers.append("收件地址")
        if self.check_putDate:
            query += ", putDate"
            headers.append("入库日期")

        query += (" FROM cainiao.storage "
                  "JOIN cainiao.packages ON storage.id = packages.id "
                  "JOIN cainiao.users ON storage.userPhone = users.userPhone ")

        list_where = []
        if self.userPhone != "":
            list_where.append(" users.userPhone = " + self.userPhone + " ")
        if self.shelf:
            list_where.append(" shelf = " + str(self.shelf) + " ")
            if self.layer:
                list_where.append(" layer = " + str(self.layer) + " ")
                if self.num:
                    list_where.append(" num = " + str(self.num) + " ")
        if self.id != "":
            list_where.append(" packages.id = " + self.id + " ")
        if self.expressNum != "":
            list_where.append(" expressNum = " + self.expressNum + " ")
        if self.company != "":
            list_where.append(" company = " + self.company + " ")
        if self.packageStatus == 1:
            list_where.append(" packageStatus = \'待入库\' ")
        elif self.packageStatus == 2:
            list_where.append(" packageStatus = \'待取件\' ")
        elif self.packageStatus == 3:
            list_where.append(" packageStatus = \'已取件\' ")
        query += generate_where_clause(list_where)
        query += " ORDER BY code "
        if self.check_range.isChecked():
            begin = int(self.line_begin.text())
            end = int(self.line_end.text())
            dert = end - begin
            query += f" LIMIT {dert} OFFSET {begin} "
        query += ";"
        self.select_action(query, headers)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 65)

    def legal_input(self):  # 判断用户信息输入是否合法
        print("正在检查用户信息合法性")
        Legal = True
        Error_Info = ""
        self.read_line_edit()
        if self.host == "":
            Legal = False
            Error_Info += "host不能未空\n"
        elif not is_valid_ip(self.host):
            Legal = False
            Error_Info += "host应为合法的ip格式\n"
        if self.port == "":
            Legal = False
            Error_Info += "port不能为空\n"
        if self.database == "":
            Legal = False
            Error_Info += "database不能为空\n"
        if self.user == "":
            Legal = False
            Error_Info += "user不能为空\n"
        if self.password == "":
            Legal = False
            Error_Info += "password不能为空\n"
        return Legal, Error_Info

    def window_init(self):  # 窗口初始化
        self.read_config()
        self.write_line_edit()
        self.line_code.clear()
        self.line_company.clear()
        self.line_userPhone.clear()
        self.line_expressNum.clear()
        self.line_id.clear()
        self.combo_packageStatus.setCurrentIndex(0)
        self.lb_status.setStyleSheet("""
                                    QLabel {
                                        color: red;
                                        font-size: 18px;
                                        font-family: "PingFang SC";
                                    }
                                """)

    def connect_clicked(self):  # 点击连接数据库
        if self.Logged_In:
            QMessageBox.warning(self, "提示", "请先断开与数据库的连接。")
        else:  # 当前未连接数据库
            Legal, Error_Info = self.legal_input()
            if not Legal:
                QMessageBox.warning(self, "错误", Error_Info)
            else:  # 输入字符串合法
                self.read_line_edit()
                if self.connect_database():
                    self.lb_status.setText(" [已连接]")
                    self.lb_status.setStyleSheet("""
                                            QLabel {
                                                color: green;
                                                font-size: 18px;
                                                font-family: "PingFang SC";
                                            }
                                        """)
                    self.Logged_In = True

    def disconnect_clicked(self):  # 点击断开连接
        if self.Logged_In:
            self.disconnect_database()
            self.lb_status.setText(" [未连接]")
            self.lb_status.setStyleSheet("""
                QLabel {
                    color: red;
                    font-size: 18px;
                    font-family: "PingFang SC";
                }
            """)
            self.window_manage_user.logout()
            self.window_manage_package.logout()
            self.window_manage_admin.logout()
            self.window_manage_grant.logout()
            QMessageBox.information(self, "提示", "已断开与数据库的连接。")

    def connect_database(self):  # 执行 连接数据库
        print("尝试连接数据库")
        try:
            self.connection = psycopg2.connect(database=self.database,
                                               user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port
                                               )
            self.cur_data_base = self.connection.cursor()
            self.window_manage_user.set_connection(self.connection, self.cur_data_base)
            self.window_manage_package.set_connection(self.connection, self.cur_data_base)
            self.window_manage_admin.set_connection(self.connection, self.cur_data_base)
            self.window_manage_grant.set_connection(self.connection, self.cur_data_base)

            return True
        except Exception as e:
            QMessageBox.warning(self, "连接数据库出错，请重新连接", str(e))
            return False

    def disconnect_database(self):  # 执行 断开数据库的连接
        self.Logged_In = False
        self.connection.close()
        self.cur_data_base.close()

    def refresh_database(self):
        self.disconnect_database()
        self.connect_database()

    def read_config(self):
        try:
            with open(self.CONFIG_FILE, 'r') as file:
                lines = file.readlines()
                # 去除每行末尾的换行符
                cleaned_lines = [line.strip() for line in lines]
                self.host = cleaned_lines[0]
                self.port = cleaned_lines[1]
                self.database = cleaned_lines[2]
                self.user = cleaned_lines[3]
                self.password = cleaned_lines[4]

                print("成功读取配置:" + '\n' +
                      "host:" + self.host + '\n' +
                      "port:" + self.port + '\n' +
                      "database:" + self.database + '\n' +
                      "user:" + self.user + '\n' +
                      "password:" + "********"
                      )
        except FileNotFoundError:
            print(f"文件 '{self.CONFIG_FILE}' 不存在。")

    def write_config(self):
        config_list = [
            str(self.host),
            str(self.port),
            str(self.database),
            str(self.user),
            str(self.password)
        ]
        try:
            with open(self.CONFIG_FILE, 'w') as file:
                for item in config_list:
                    file.write(item + '\n')
            print(f"配置已成功写入文件 '{self.CONFIG_FILE}'。")
        except FileNotFoundError:
            print(f"文件 '{self.CONFIG_FILE}' 不存在。")

    def read_line_edit(self):
        self.host = self.line_host.text()
        self.port = self.line_port.text()
        self.database = self.line_database.text()
        self.user = self.line_user.text()
        self.password = self.line_password.text()

    def write_line_edit(self):
        self.line_host.setText(self.host)
        self.line_port.setText(self.port)
        self.line_database.setText(self.database)
        self.line_user.setText(self.user)
        self.line_password.setText(self.password)

    # 重写调整窗口大小函数
    def resizeEvent(self, event):
        x = self.width() - self.table.x() - 30
        y = self.height() - self.table.y() - 60
        self.table.setFixedSize(x, y)


if __name__ == '__main__':  # 运行主函数
    QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    Window = CaiNiaoWindow()
    Window.show()

    sys.exit(app.exec_())
