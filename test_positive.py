import subprocess

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def getout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


def test_step1():
    # test1
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "test2 FAIL"


def test_step2():
    # test2
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok"),
    result2 = checkout("cd {}; ls".format(folder1), "qwe")
    result3 = checkout("cd {}; ls".format(folder1), "rty")
    assert result1 and result2 and result3, "test2 FAIL"


def test_step3():
    # test3
    assert checkout("cd {}; 7z t arx2.7z".format(out), "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout("cd {}; 7z u ../out/arx2.7z".format(tst), "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    result1 = checkout("cd {}; 7z l arx2.7z".format(out), "qwe")
    result2 = checkout("cd {}; 7z l arx2.7z".format(out), "rty")
    assert result1 and result2, "test5 FAIL"


def test_step6():
    # test6
    result1 = checkout("cd {}; 7z h qwe".format(tst), "Everything is Ok")
    get_hash = getout("cd {}; crc32 qwe".format(tst)).upper()
    result2 = checkout("cd {}; 7z h qwe".format(tst), get_hash)
    assert result1 and result2, "test6 FAIL"


def test_step7():
    # test7
    result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(out, folder2), "Everything is Ok")
    result2 = checkout("ls {}".format(folder2), "qwe")
    result3 = checkout("ls {}".format(folder2), "rty")
    assert result1 and result2 and result3, "test7 FAIL"


def test_step8():
    # test8
    assert checkout("cd {}; 7z d arx2.7z".format(out), "Everything is Ok"), "test8 FAIL"
