from faker import Faker
import random
from datetime import datetime

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


def pad_with_zeros(number):
    number_str = str(number)
    num_zeros = max(0, 20 - len(number_str))
    padded_str = "0" * num_zeros + number_str
    return padded_str


def read_file_to_list(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                lines.append(line)
    return lines


def read_line(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()  # 读取第一行并去除首尾空白字符
        integer_value = int(first_line)  # 将字符串转换为整数
        return integer_value


def write_line(file_path, text_to_write):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_to_write)


def generate_random_integer_string(min_length=8, max_length=18):
    length = random.randint(min_length, max_length)
    random_integer_string = str(random.randint(1, 9))
    for _ in range(1, length):
        random_integer_string += str(random.randint(0, 9))
    return random_integer_string


def generate_code(integer):
    integer_str = str(integer)
    if len(integer_str) < 6:
        return "输入的整数位数不足6位。", None, None, None
    num = integer_str[-4:]
    layer = integer_str[-5:-4]
    shelf = integer_str[:-5]
    code = f"{shelf}-{layer}-{num}"
    return code, shelf, layer, num


def generate_random_date(year):
    if not isinstance(year, int) or year < 1:
        return "请输入有效的年份。"
    month = random.randint(1, 12)
    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    date = datetime(year, month, day).strftime('%Y-%m-%d')
    return date


def insert_string_to_file(file_path, string_to_insert):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(string_to_insert + '\n')


def gen_package(num_package):
    list_userPhone = read_file_to_list('./data/userPhone.txt')

    id_count = read_line('./data/id.txt') + 1
    code_count = read_line('./data/code.txt') + 1
    query_packages = ("INSERT INTO cainiao.packages "
                      "(id, company, expressNum, packageName, information, "
                      "sendName, sendAddress, receiveName, receiveAddress, "
                      "code, shelf, layer, num, putDate) VALUES ")
    query_storage = "INSERT INTO cainiao.storage (userPhone, id, packageStatus) VALUES "

    for i in range(0, num_package):
        if i % 5000 == 0:
            print(i, "/", num_package)
        userPhone = "\'" + random.choice(list_userPhone) + "\'"
        Id = "\'" + pad_with_zeros(i) + "\'"
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
        if i == num_package - 1:
            query_packages += ';'
            query_storage += ';'
    return query_storage, query_packages

num_package = 500

list_userPhone = read_file_to_list('./data/userPhone.txt')

id_count = read_line('./data/id.txt') + 1
code_count = read_line('./data/code.txt') + 1

insert_string_to_file("./SQL/packages.txt", "INSERT INTO cainiao.packages "
                                            "(id, company, expressNum, packageName, information, "
                                            "sendName, sendAddress, receiveName, receiveAddress, "
                                            "code, shelf, layer, num, putDate) VALUES")
insert_string_to_file("./SQL/storage.txt", "INSERT INTO cainiao.storage (userPhone, id, packageStatus) VALUES")
print("正在生成数据")
for i in range(0, num_package):
    userPhone = "\'" + random.choice(list_userPhone) + "\'"
    Id = "\'" + pad_with_zeros(i) + "\'"
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
    code = "\'" + code + "\'"
    code_count += 1
    putDate = "\'" + generate_random_date(2024) + "\'"
    packageStatus = "\'" + random.choice(status) + "\'"

    query_packages = ("(" + Id + ", " + company + ", " + expressNum + ", " + packageName + ", " + information + ", " +
                      sendName + ", " + sendAddress + ", " + receiveName + ", " + receiveAddress + ", " + code + ", " +
                      shelf + ", " + layer + ", " + num + ", " + putDate + ")"
                      )
    query_storage = ("(" + userPhone + ", " + Id + ", " + packageStatus + ")"
                     )
    if i == num_package - 1:
        query_packages += ';'
        query_storage += ';'
    else:
        query_packages += ','
        query_storage += ','
    insert_string_to_file("./SQL/packages.txt", query_packages)
    insert_string_to_file("./SQL/storage.txt", query_storage)
    write_line('./data/id.txt', str(id_count))
    write_line('./data/code.txt', str(code_count))

    if i % 3000 == 0:
        print("当前已生成数据数量：", i)
