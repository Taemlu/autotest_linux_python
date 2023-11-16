import pytest
from checkers import checkout
import random, string
import yaml
from datetime import datetime
from checkers import getout

with open('config.yaml') as f: # положили в yaml переменные, которым присвоили пути
    data = yaml.safe_load(f) # безопасная загрузка без лишних данных

@pytest.fixture()
def make_folders():
    return checkout("mkdir -p {} {} {} {}".format(data["tst"], data["out"], data["folder1"], data["folder2"]), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["tst"], data["out"], data["folder1"], data["folder2"]), "")


@pytest.fixture()
def make_files():
    # создаём файл с рандомным именем, размером 1Мб, в директории out,
    # генерирует файл (dd) из специального файла линукса с рандомными данными (if=/dev/urandom),
    # файл с рандомным содержанием, который записывается в выше сгененрированный файл
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"], filename, data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files
@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["tst"], subfoldername), ""):
        return None, None
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["tst"], subfoldername,
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
    checkout("cd {}; 7z a {}/bad_arx".format(data["tst"], data["out"]), "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.7z".format(data["out"]), "") # урезать файл на 1 байт транкейт -с

# homework 3
@pytest.fixture(autouse=True)
def stat():
    stat = getout('cat /proc/loadavg')
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime('%H:%M:%S.%f'),
                                                                             data['count'], data['bs'], stat), '')