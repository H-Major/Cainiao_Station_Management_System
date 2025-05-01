from faker import Faker

fake = Faker('zh_CN')


def read_file_to_list(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                lines.append(line)
    return lines


def insert_string_to_file(file_path, string_to_insert):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(string_to_insert + '\n')


num_userPhone = 50

list_userPhone = read_file_to_list('./data/userPhone.txt')

insert_string_to_file('./SQL/users.txt', "INSERT INTO cainiao.users (userPhone, userName) VALUES")
for i in range(0, num_userPhone):
    while True:
        userPhone = fake.phone_number()
        if userPhone not in list_userPhone:
            break
    list_userPhone.append(userPhone)
    insert_string_to_file('./data/userPhone.txt', userPhone)
    userName = fake.name()
    query = '(\'' + userPhone + '\', \'' + userName + '\')'
    if i == num_userPhone - 1:
        query += ';'
    else:
        query += ','
    insert_string_to_file('./SQL/users.txt', query)