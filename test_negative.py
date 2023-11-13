import subprocess

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step1():
    # test1
    assert checkout("cd {}; 7z e bad_arx.7z -o{} -y".format(out, folder1), "ERRORS"), "test1 FAIL"


def test_step2():
    # test2
    assert checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "test2 FAIL"


