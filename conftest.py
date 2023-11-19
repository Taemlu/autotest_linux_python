import pytest
from checkers import ssh_checkout, ssh_get
import random, string
import yaml
from datetime import datetime
from files import upload_files

with open('config.yaml') as f:  # положили в yaml переменные, которым присвоили пути
    data = yaml.safe_load(f)  # безопасная загрузка без лишних данных


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "mkdir -p {} {} {} {}".format(data["tst"], data["out"], data["folder1"],
                                                      data["folder2"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["tst"], data["out"], data["folder1"], data["folder2"]),
                        "")


@pytest.fixture()
def make_files():
    # создаём файл с рандомным именем, размером 1Мб, в директории out,
    # генерирует файл (dd) из специального файла линукса с рандомными данными (if=/dev/urandom),
    # файл с рандомным содержанием, который записывается в выше сгененрированный файл
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"], filename,
                                                                                               data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}; mkdir {}".format(data["tst"], subfoldername), ""):
        return None, None
    if not ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["tst"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "11",
                 "cd {}; 7z a {}/bad_arx".format(data["tst"], data["out"]), "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "11",
                 "truncate -s 1 {}/bad_arx.7z".format(data["out"]), "")  # урезать файл на 1 байт транкейт -с


# homework 3
# @pytest.fixture(autouse=True)
# def stat():
#     stat = ssh_getout("0.0.0.0", "user2", "11",'cat /proc/loadavg')
#     ssh_checkout("0.0.0.0", "user2", "11",
#                  "echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime('%H:%M:%S.%f'),
#                                                                              data['count'], data['bs'], stat), '')

# ДЗ №4 Загрузка логов в файл.
@pytest.fixture(autouse=True)
def stat():
    with open('stat.txt', 'a') as f:
        stat_ssh = ssh_get("0.0.0.0", "user2", "11",
                           "journalctl --since '{}'".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        f.write(f'Journal of logs:\n{stat_ssh}')


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "11", "/home/user/p7zip-full.deb",
                 "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)


@pytest.fixture(autouse=True, scope='module')
def deploy_apt():
    res = []
    res.append(ssh_checkout("0.0.0.0", "user2", "11",
                            "echo '111' | sudo -S apt install libarchive-zip-perl",
                            'Настраивается пакет'))
    res.append(
        ssh_checkout("0.0.0.0", "user2", "11", "echo '111' | sudo -S apt list libarchive-zip-perl",
                     'установлен'))
    print(f'{res}')
    return all(res)


@pytest.fixture(autouse=True, scope="module")
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_log(start_time):
    with open("stat.txt", "w") as f:
        f.write(ssh_get("0.0.0.0", "user2", "11", "journalctl --since {}".format(start_time)))
        f.write(ssh_get("0.0.0.0", "user2", "11", "echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(
            datetime.now().strftime('%H:%M:%S.%f'),
            data['count'], data['bs'], stat)))
