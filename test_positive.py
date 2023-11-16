from checkers import checkout, getout
import yaml

with open('config.yaml') as f: # положили в yaml переменные, которым присвоили пути
    data = yaml.safe_load(f) # безопасная загрузка без лишних данных

class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        result1 = checkout("cd {}; 7z a {}/arx2 -t{}".format(data["tst"], data["out"], data["type"]), "Everything is Ok")
        result2 = checkout("ls {}".format(data["out"]), "arx2.{}".format(data["type"]))
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data["tst"], data["out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.{} -o{} -y".format(data["out"], data["type"], data["folder1"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; ls".format(data["folder1"]), item))

        assert all(res), "test2 FAIL"


    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx2.{}".format(data["out"], data["type"]), "Everything is Ok"), "test3 FAIL"


    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u ../out/arx2.{}".format(data["tst"], data["type"]), "Everything is Ok"), "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data["tst"], data["out"], data["type"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arx2.{}".format(data["out"], data["type"]), item))

        assert all(res), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["tst"], data["out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["out"], data["type"], data["folder2"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder2"]), item))

        res.append(checkout("ls {}".format(data["folder2"]), make_subfolder[0])) # обратились по индексу ноль, така имя сабфолдера шло первым
        res.append(checkout("ls {}/{}".format(data["folder2"], make_subfolder[0]), make_subfolder[1])) # обратились к индексу 1, так как имя файлов шло вторым в фикситуре
        assert all(res), "test6 FAIL"


    def test_step7(self):
        # test7
        assert checkout("cd {}; 7z d arx.{}".format(data["out"], data["type"]), "Everything is Ok"), "test7 FAIL"

    # Hash
    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["tst"], item), "Everything is Ok"))
            get_hash = getout("cd {}; crc32 {}".format(data["tst"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["tst"], item), get_hash))
        assert all(res), "test8 FAIL"
