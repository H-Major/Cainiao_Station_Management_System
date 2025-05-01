from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
from PyQt5.QtGui import *
import re
import psycopg2
from faker import Faker
import random
from datetime import datetime

from manage_package_UI import Ui_PackageForm

fake = Faker('zh-CN')

express_companies = [
    "顺丰速运",
    "京东物流",
    "EMS",
    "中通快递",
    "韵达快递",
    "圆通速递",
    "申通快递",
    "极兔速递",
    "德邦快递",
    "跨越速运",
    "百世快递",
    "国通快递"
]

express_num = {
    "顺丰速运": "SF",
    "京东物流": "JD",
    "EMS": "EMS",
    "中通快递": "ZT",
    "韵达快递": "YD",
    "圆通速递": "YT",
    "申通快递": "ST",
    "极兔速递": "JT",
    "德邦快递": "DB",
    "跨越速运": "KY",
    "百世快递": "BS",
    "国通快递": "GT"
}

items = [
    "手机", "笔记本电脑", "耳机", "充电器", "书", "衣服", "鞋子", "面膜", "玩具车", "护肤霜",
    "化妆品", "相机", "手表", "零食", "水杯", "文具", "书包", "鼠标", "键盘", "显示器",
    "路由器", "水果", "蔬菜", "奶粉", "儿童玩具", "宠物食品", "瑜伽垫", "运动鞋", "卫衣",
    "帽子", "围巾", "手套", "袜子", "短裤", "裙子", "皮带", "领带", "项链", "耳环",
    "手链", "戒指", "背包", "行李箱", "茶叶", "咖啡", "红酒", "啤酒", "白酒", "果汁",
    "牛奶", "酸奶", "巧克力", "饼干", "薯片", "糖果", "方便面", "火腿肠", "面包", "蛋糕",
    "果酱", "花生酱", "蜂蜜", "大米", "面粉", "食用油", "调味品", "酱油", "醋", "盐",
    "胡椒", "香料", "调料包", "洗衣粉", "洗洁精", "洗发水", "沐浴露", "香皂", "牙膏", "牙刷",
    "漱口水", "面巾纸", "卫生纸", "湿巾", "纸巾", "餐巾纸", "洗手液", "除臭剂", "洗面奶", "卸妆水",
    "防晒霜", "润肤乳", "面霜", "眼霜", "眼膜", "唇膏", "唇彩", "眉笔", "眼线笔", "眼影",
    "粉底", "腮红", "散粉", "美甲", "指甲油", "假睫毛", "假发", "染发剂", "定型喷雾", "卷发棒",
    "直发器", "梳子", "吹风机", "剃须刀", "电动牙刷", "智能手环", "智能手表", "平板电脑", "电子书", "游戏机",
    "游戏手柄", "蓝牙音箱", "车载充电器", "车载支架", "车载空气净化器", "行车记录仪", "导航仪", "车载冰箱", "车载吸尘器", "行李箱",
    "旅行包", "旅游鞋", "防晒衣", "泳衣", "泳帽", "泳镜", "潜水服", "冲浪板", "帐篷", "睡袋",
    "露营灯", "野餐垫", "保温杯", "保温壶", "烧烤架", "烤肉酱", "木炭", "火柴", "打火机", "打火石",
    "急救包", "药品", "创可贴", "绷带", "体温计", "血压计", "血糖仪", "止痛药", "感冒药", "消炎药",
    "维生素", "钙片", "鱼油", "益生菌", "枕头", "床单", "被子", "毛毯", "蚊帐", "窗帘",
    "地毯", "抱枕", "坐垫", "椅套", "桌布", "餐垫", "刀叉", "勺子", "筷子", "碗",
    "盘子", "杯子", "茶壶", "咖啡机", "微波炉", "电饭煲", "烤箱", "冰箱", "洗衣机", "吸尘器",
    "电熨斗", "电风扇", "空调", "暖风机", "加湿器", "除湿机", "空气净化器", "饮水机", "热水器", "油烟机",
    "煤气灶", "电磁炉", "电热水壶", "咖啡壶", "榨汁机", "搅拌机", "电烤箱", "煎锅", "炖锅", "蒸锅",
    "高压锅", "火锅", "炒锅", "平底锅", "砂锅", "炊具", "厨房秤", "切菜刀", "菜板", "铲子",
    "勺子", "餐具", "碗碟", "锅盖", "保鲜盒", "保鲜膜", "密封袋", "冰袋", "冰盒", "过滤器",
    "水壶", "茶杯", "酒杯", "啤酒杯", "红酒杯", "香槟杯", "威士忌杯", "鸡尾酒杯", "葡萄酒杯", "醒酒器",
    "酒架", "酒桶", "酒瓶", "酒塞", "开瓶器", "酒盒", "酒袋", "酒柜", "红酒架", "红酒杯"
]

remarks = [
    "请放置门口", "货到电话联系", "无需签收", "尽快配送", "周末送达", "请勿放快递柜", "签收时开箱验货",
    "送至公司前台", "请帮忙送到楼下", "请勿折叠", "小心轻放", "避免暴晒", "请尽量下午送", "邻居代收",
    "可放保安室", "请提前电话联系", "需要本人签收", "请勿压货", "请勿放门口", "送到学校宿舍", "请确保包装完好",
    "周五之前送达", "确认电话后送", "请勿摇晃", "假期送达", "请放置指定地点", "请务必联系本人", "送货上门",
    "请勿放快递箱", "请加急配送", "易碎品", "请在上午送达", "签收时请拍照", "放置在收发室", "请投放到信箱",
    "注意防潮", "周一到周五送", "请先电话通知", "请注意防雨", "周末勿送", "不要放自提柜", "请勿暴力投递",
    "送至地下停车场", "需要签收人签字", "白天送达", "请避免挤压", "请勿送至办公室", "确认收货再送", "请勿暴力拆包",
    "请快递员注意安全", "不要放置楼梯间", "提前联系后送", "送至物业前台", "无需签收证明", "勿在夜间送达",
    "确认电话再送", "周五后勿送", "包装要牢固", "注意隔热", "请勿折叠包装", "周六送达", "包装完好",
    "请确保货物完好", "请联系物业代收", "送到家门口", "可放在快递柜", "请勿弄湿", "请联系后送", "注意易碎",
    "请勿挤压", "放置到信报箱", "送到后请短信通知", "请确保包装完整", "请注意防晒", "下午送达最佳", "需要本人收取",
    "放在门卫室", "送到指定收货人", "请尽量早点送", "注意保温", "提前通知再送", "请放置在楼下", "请勿暴力搬运",
    "货到短信通知", "注意防震", "请勿直接放快递柜", "请放置办公室", "提前通知", "送到指定地点", "确保货物完好",
    "请勿拆包检查", "避免损坏", "请通知后送", "送达请电话联系", "尽量避开高温", "需要收货人签名", "快递员注意安全",
    "确认电话联系"
]

status = ["待入库", "待取件", "已取件"]

from datetime import datetime


def generate_set(list_set):
    # 使用逗号将列表中的字符串连接成一个字符串
    str_set = ','.join(list_set)
    return str_set


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def is_valid_code(code):
    pattern = r'^(\d+)-(\d)-(\d{4})$'
    match = re.match(pattern, code)
    if match:
        X, Y, Z = int(match.group(1)), int(match.group(2)), int(match.group(3))
        return True, X, Y, Z
    else:
        return False, 0, 0, 0


def is_valid_phone_number(phone_number: str) -> bool:
    pattern = r"^1\d{10}$"
    return bool(re.match(pattern, phone_number))


def is_valid_id(num):
    if isinstance(num, str) and num.isdigit():
        return len(num) == 20
    return False


def generate_id_query(id):
    query = f"SELECT * FROM cainiao.packages WHERE id = '{id}' LIMIT 1;"
    return query


def generate_phone_query(userPhone):
    query = f"SELECT * FROM cainiao.users WHERE userPhone = '{userPhone}' LIMIT 1;"
    return query


def generate_id(length=20):
    """Generate a random string of specified length consisting of digits."""
    return ''.join(random.choices('0123456789', k=length))


def generate_num(min_length=8, max_length=18):
    length = random.randint(min_length, max_length)
    random_integer_string = str(random.randint(1, 9))
    for _ in range(1, length):
        random_integer_string += str(random.randint(0, 9))
    return random_integer_string


def generate_code():
    integer = random.randint(100000, 999999)
    integer_str = str(integer)
    if len(integer_str) < 6:
        return "输入的整数位数不足6位。", None, None, None
    num = integer_str[-4:]
    layer = integer_str[-5:-4]
    shelf = integer_str[:-5]
    code = f"{shelf}-{layer}-{num}"
    return code, shelf, layer, num


class ManagePackage(QMainWindow, Ui_PackageForm):
    # 构造函数
    def __init__(self):
        super(ManagePackage, self).__init__()
        self.setupUi(self)

        # 数据库连接与游标
        self.connection = None
        self.cur_data_base = None

        # 包裹信息
        self.userPhone = ""
        self.id = ""  # 菜鸟包裹单号
        self.company = ""  # 快递公司
        self.expressNum = ""  # 快递单号
        self.packageName = ""  # 包裹名称
        self.information = ""  # 包裹备注信息
        self.sendName = ""  # 发件人
        self.sendAddress = ""  # 发件地址
        self.receiveName = ""  # 收件人
        self.receiveAddress = ""  # 收件地址
        self.code = ""  # 取件码
        self.packageStatus = ""
        self.putDate = ""

        self.shelf = 0
        self.layer = 0
        self.num = 0

        # 信号连接
        self.btn_random.clicked.connect(self.random_create_data)
        self.btn_create.clicked.connect(self.create_package)
        self.btn_delete_id.clicked.connect(self.delete_package_id)
        self.btn_delete_phone.clicked.connect(self.delete_package_phone)
        self.btn_update.clicked.connect(self.update_package)

        self.logout()

    def init_info(self):
        self.userPhone = ""
        self.id = ""  # 菜鸟包裹单号
        self.company = ""  # 快递公司
        self.expressNum = ""  # 快递单号
        self.packageName = ""  # 包裹名称
        self.information = ""  # 包裹备注信息
        self.sendName = ""  # 发件人
        self.sendAddress = ""  # 发件地址
        self.receiveName = ""  # 收件人
        self.receiveAddress = ""  # 收件地址
        self.code = ""  # 取件码
        self.packageStatus = ""
        self.putDate = ""

        self.shelf = 0
        self.layer = 0
        self.num = 0


    def set_connection(self, conn, cur):
        print("连接manage_package界面")
        self.connection = conn
        self.cur_data_base = cur
        self.btn_create.setEnabled(True)
        self.btn_delete_id.setEnabled(True)
        self.btn_delete_phone.setEnabled(True)
        self.btn_update.setEnabled(True)

    def create_package(self):
        print("正在添加包裹")
        self.init_info()
        Legal = True
        Error_Info = ""

        if self.line_userPhone.text() == "":
            Legal = False
            Error_Info += "手机号不能为空\n"
            print("用户手机号不存在")
        elif not is_valid_phone_number(self.line_userPhone.text()):
            Legal = False
            Error_Info += "手机号格式有误\n"
            print("手机号格式有误")
        elif not self.user_exists(self.line_userPhone.text()):
            Legal = False
            Error_Info += "手机号不存在\n"
            print("手机号不存在")
        else:
            self.userPhone = self.line_userPhone.text()
            print("userPhone:", self.userPhone)
        if self.line_id.text() == "":
            Legal = False
            Error_Info += "包裹编号不能为空\n"
        elif not is_valid_id(self.line_id.text()):
            Legal = False
            Error_Info += "包裹编号格式有误\n"
        elif self.id_exists(self.line_id.text()):
            Legal = False
            Error_Info += "包裹编号已存在\n"
        else:
            self.id = self.line_id.text()
            print("id:", self.id)

        if self.line_company.text() == "":
            Legal = False
            Error_Info += "快递公司不能为空\n"
        else:
            self.company = self.line_company.text()
            print("company:", self.company)

        if self.line_expressNum.text() == "":
            Legal = False
            Error_Info += "快递单号不能为空\n"
        else:
            self.expressNum = self.line_expressNum.text()
            print("expressNum:", self.expressNum)

        if self.line_packageName.text() == "":
            Legal = False
            Error_Info += "包裹名称不能为空\n"
        else:
            self.packageName = self.line_packageName.text()
            print("packageName:", self.packageName)

        if self.line_information.text() == "":
            Legal = False
            Error_Info += "包裹备注信息不能为空\n"
        else:
            self.information = self.line_information.text()
            print("information:", self.information)

        if self.line_sendName.text() == "":
            Legal = False
            Error_Info += "发件人不能为空\n"
        else:
            self.sendName = self.line_sendName.text()
            print("sendName:", self.sendName)

        if self.line_sendAddress.text() == "":
            Legal = False
            Error_Info += "发件地址不能为空\n"
        else:
            self.sendAddress = self.line_sendAddress.text()
            print("sendAddress:", self.sendAddress)

        if self.line_receiveName.text() == "":
            Legal = False
            Error_Info += "收件人不能为空\n"
        else:
            self.receiveName = self.line_receiveName.text()
            print("receiveName:", self.receiveName)

        if self.line_receiveAddress.text() == "":
            Legal = False
            Error_Info += "收件地址不能为空\n"
        else:
            self.receiveAddress = self.line_receiveAddress.text()
            print("receiveAddress:", self.receiveAddress)

        if self.line_code.text() == "":
            Legal = False
            Error_Info += "取件码不能为空\n"
        elif self.code_exist(self.line_code.text()):
            Legal = False
            Error_Info += "取件码不能重复\n"
        else:
            flag, self.shelf, self.layer, self.num = is_valid_code(self.line_code.text())
            if not flag:
                Legal = False
                Error_Info += "取件码格式有误\n"
            else:
                self.code = self.line_code.text()
                print("code:", self.code)
        self.packageStatus = status[self.combo_packageStatus.currentIndex()]
        print("packageStatus:", self.packageStatus)
        self.putDate = get_current_datetime()
        print("putDate:", self.putDate)

        if not Legal:
            QMessageBox.warning(self, "错误", Error_Info)
        else:
            query = f'''
                    INSERT INTO cainiao.packages (
                        id, company, expressNum, packageName, information, sendName, sendAddress,
                        receiveName, receiveAddress, code, shelf, layer, num, putDate) 
                    VALUES (
                        '{self.id}', '{self.company}', '{self.expressNum}', '{self.packageName}',
                        '{self.information}', '{self.sendName}', '{self.sendAddress}',
                        '{self.receiveName}', '{self.receiveAddress}', '{self.code}',
                        {self.shelf}, {self.layer}, {self.num}, '{self.putDate}'
                    );
                    '''
            query += f'''
                   INSERT INTO cainiao.storage (id, userPhone, packageStatus)
                   VALUES ('{self.id}', '{self.userPhone}', '{self.packageStatus}');
                   '''
            # 执行插入操作
            try:
                print("执行插入：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "创建包裹成功。")
            except psycopg2.Error as e:
                print("Error inserting data:", e)
                self.connection.rollback()

    def delete_package_phone(self):
        self.init_info()
        Legal = True
        Error_Info = ""

        if self.line_userPhone.text() == "":
            Legal = False
            Error_Info += "手机号不能为空\n"
        elif not is_valid_phone_number(self.line_userPhone.text()):
            Legal = False
            Error_Info += "手机号格式有误\n"
        elif not self.user_exists(self.line_userPhone.text()):
            Legal = False
            Error_Info += "手机号不存在\n"
        else:
            self.userPhone = self.line_userPhone.text()

        if not Legal:
            QMessageBox.warning(self, "错误", Error_Info)
        else:
            query = ("DELETE FROM cainiao.storage " +
                     " WHERE userPhone = " + self.userPhone +
                     ";")
            try:
                print("执行删除：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "该用户所有包裹删除成功。")
            except psycopg2.Error as e:
                print(f"数据库更新错误: {e}")

    def delete_package_id(self):
        self.init_info()
        Legal = True
        Error_Info = ""
        if self.line_id.text() == "":
            Legal = False
            Error_Info += "包裹编号不能为空\n"
        elif not is_valid_id(self.line_id.text()):
            Legal = False
            Error_Info += "包裹编号格式有误\n"
        elif not self.id_exists(self.line_id.text()):
            Legal = False
            Error_Info += "包裹编号不存在\n"
        else:
            self.id = self.line_id.text()

        if not Legal:
            QMessageBox.warning(self, "错误", Error_Info)
        else:
            query = ("DELETE FROM cainiao.storage " +
                     " WHERE id = \'" + self.id +
                     "\';")
            try:
                print("执行删除：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "包裹删除成功。")
            except psycopg2.Error as e:
                print(f"数据库更新错误: {e}")

    def update_package(self):
        self.init_info()
        Legal = True
        Error_Info = ""
        list_set_storage = []
        list_set_packages = []

        if not self.line_id.text() == "":
            if not is_valid_id(self.line_id.text()):
                Legal = False
                Error_Info += "包裹编号格式有误\n"
            elif not self.id_exists(self.line_id.text()):
                Legal = False
                Error_Info += "包裹编号不存在\n"
            else:
                self.id = self.line_id.text()

        if not self.line_userPhone.text() == "":
            if not is_valid_phone_number(self.line_userPhone.text()):
                Legal = False
                Error_Info += "手机号格式有误\n"
            elif not self.user_exists(self.line_userPhone.text()):
                Legal = False
                Error_Info += "手机号不存在\n"
            else:
                self.userPhone = self.line_userPhone.text()
                list_set_storage.append(" userPhone = \'" + self.userPhone + "\' ")

        if not self.line_company.text() == "":
            self.company = self.line_company.text()
            list_set_packages.append(" company = \'" + self.company + "\' ")

        if not self.line_expressNum.text() == "":
            self.expressNum = self.line_expressNum.text()
            list_set_packages.append(" expressNum = \'" + self.expressNum + "\' ")

        if not self.line_packageName.text() == "":
            self.packageName = self.line_packageName.text()
            list_set_packages.append(" packageName = \'" + self.packageName + "\' ")

        if not self.line_information.text() == "":
            self.information = self.line_information.text()
            list_set_packages.append(" information = \'" + self.information + "\' ")

        if not self.line_sendName.text() == "":
            self.sendName = self.line_sendName.text()
            list_set_packages.append(" sendName = \'" + self.sendName + "\' ")

        if not self.line_sendAddress.text() == "":
            self.sendAddress = self.line_sendAddress.text()
            list_set_packages.append(" sendAddress = \'" + self.sendAddress + "\' ")

        if not self.line_receiveName.text() == "":
            self.receiveName = self.line_receiveName.text()
            list_set_packages.append(" receiveName = \'" + self.receiveName + "\' ")

        if not self.line_receiveAddress.text() == "":
            self.receiveAddress = self.line_receiveAddress.text()
            list_set_packages.append(" receiveAddress = \'" + self.receiveAddress + "\' ")

        if not self.line_code.text() == "":
            flag, self.shelf, self.layer, self.num = is_valid_code(self.line_code.text())
            if not flag:
                Legal = False
                Error_Info += "取件码格式有误\n"
            else:
                self.code = self.line_code.text()
                list_set_packages.append(" code = \'" + self.code + "\' ")
                list_set_packages.append(" shelf = " + str(self.shelf) + " ")
                list_set_packages.append(" layer = " + str(self.layer) + " ")
                list_set_packages.append(" num = " + str(self.num) + " ")

        self.packageStatus = status[self.combo_packageStatus.currentIndex()]
        list_set_storage.append(" packageStatus = \'" + self.packageStatus + "\' ")

        if not Legal:
            QMessageBox.warning(self, "错误", Error_Info)
        else:
            query = "UPDATE cainiao.storage SET "
            query += generate_set(list_set_storage)
            query += " WHERE id = \'" + self.id + "\';"
            if list_set_packages:
                query += "UPDATE cainiao.packages SET "
                query += generate_set(list_set_packages)
                query += " WHERE id = \'" + self.id + "\';"
            try:
                print("执行更新：\n", query)
                self.cur_data_base.execute(query)
                self.connection.commit()
                QMessageBox.information(self, "提示", "包裹信息更新成功。")
            except psycopg2.Error as e:
                print(f"数据库更新错误: {e}")

    def code_exist(self, code):
        query = "SELECT * FROM cainiao.packages WHERE code = \'" + code + "\';"
        try:
            self.cur_data_base.execute(query)
            result = self.cur_data_base.fetchone()
            return result is not None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False

    def id_exists(self, id):
        query = generate_id_query(id)
        try:
            self.cur_data_base.execute(query)
            result = self.cur_data_base.fetchone()
            return result is not None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False

    def user_exists(self, userPhone):
        query = generate_phone_query(userPhone)
        print("执行查询", query)
        try:
            self.cur_data_base.execute(query)
            result = self.cur_data_base.fetchone()
            print(result)
            return result is not None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False

    def random_create_data(self):
        # self.line_userPhone.clear()
        '''
        self.line_id.clear()
        self.line_company.clear()
        self.line_expressNum.clear()
        self.line_packageName.clear()
        self.line_information.clear()
        self.line_sendName.clear()
        self.line_sendAddress.clear()
        self.line_receiveName.clear()
        self.line_receiveAddress.clear()
        self.line_code.clear()
        self.combo_packageStatus.setCurrentIndex(0)
        '''

        # 使用变量存储生成的字符串值
        id_value = generate_id()
        print(f"Setting id to: {id_value}")
        self.line_id.setText(id_value)
        company_value = random.choice(express_companies)
        print(f"Setting company to: {company_value}")
        self.line_company.setText(company_value)
        expressNum_value = express_num[company_value] + generate_num()
        print(f"Setting expressNum to: {expressNum_value}")
        self.line_expressNum.setText(expressNum_value)
        packageName_value = random.choice(items)
        print(f"Setting packageName to: {packageName_value}")
        self.line_packageName.setText(packageName_value)
        information_value = random.choice(remarks)
        print(f"Setting information to: {information_value}")
        self.line_information.setText(information_value)
        sendName_value = fake.name()
        print(f"Setting sendName to: {sendName_value}")
        self.line_sendName.setText(sendName_value)
        sendAddress_value = fake.address()
        print(f"Setting sendAddress to: {sendAddress_value}")
        self.line_sendAddress.setText(sendAddress_value)
        receiveName_value = fake.name()
        print(f"Setting receiveName to: {receiveName_value}")
        self.line_receiveName.setText(receiveName_value)
        receiveAddress_value = fake.address()
        print(f"Setting receiveAddress to: {receiveAddress_value}")
        self.line_receiveAddress.setText(receiveAddress_value)
        code_value, x, y, z = generate_code()
        print(f"Setting code to: {code_value}")
        self.line_code.setText(code_value)

    def logout(self):
        self.btn_create.setEnabled(False)
        self.btn_delete_id.setEnabled(False)
        self.btn_delete_phone.setEnabled(False)
        self.btn_update.setEnabled(False)
