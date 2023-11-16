import yaml
from checkers import checkout_negative

with open('config.yaml') as f: # положили в yaml переменные, которым присвоили пути
    data = yaml.safe_load(f) # безопасная загрузка без лишних данных


class TestNegative:
    def test_step1(self, make_bad_arx):
        # test1
        assert checkout_negative("cd {}; 7z e bad_arx.7z -o{} -y".format(data["out"], data["folder1"]), "ERRORS"), "test1 FAIL"

    def test_step2(self):
        # test2
        assert checkout_negative("cd {}; 7z t bad_arx.7z".format(data["out"]), "ERRORS"), "test2 FAIL"


