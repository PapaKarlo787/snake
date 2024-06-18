'''
Обрабатывает файл уровня и возвращает список списков элементов в формате
установленном в игре (см. документацию).
Если файл пришел неопределенный (None), то возвращает в self.fn None,
если не удалось загрузить файл или он пришел сломанный, то в self.message
сообщение об ошибке, иначе None.
'''


class Level:
    def __init__(self, fn, w, h):
        self.w = w
        self.h = h
        self.fn = fn
        self.timer = 10
        if not fn:
            self.load_empty_level()
            return
        with open(self.fn, 'r') as f:
            self.text = f.read().split('\n')
        self.load_level()

    def load_level(self):
        if not self.text[-1]:
            self.text.pop()
        try:
            self.timer = int(self.text.pop())
        except Exception:
            raise Exception("Can`t load time of level!\nRead documentation")
        if len(self.text) < 3 or len(self.text[0]) < 3:
            raise Exception("Too short lenes!\nRead documentation")
        self.h = len(self.text)
        self.w = len(self.text[0])
        mapkey = {"#": "WALL", " ": "VOID"}
        self.map = []
        for i in range(self.h):
            self.map.append([])
            len_is_ok = len(self.text[i]) == self.w
            for k in range(self.w):
                if self.text[i][k] in mapkey and len_is_ok:
                    self.map[i].append(mapkey[self.text[i][k]])
                else:
                    raise Exception("File broken at line {}".format(i+1))

    def load_empty_level(self):
        self.map = [0] * self.h
        for i in range(self.h):
            self.map[i] = ["VOID"] * self.w
