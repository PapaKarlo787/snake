import configparser
import copy


'''
Обрабатывает конфигурационный файл и возвращает структуру содержащую
конфигурационную информацию.
Если не удалось прочитать файл или файл содержит ошибки, то грузим
значения по умолчанию из blocks и пытаемся сохранить в конфигурационный
файл, в случае неудачи, ничего не делаем.
'''


class Config:
    def __init__(self, fn, blocks):
        self.blocks = copy.deepcopy(blocks)
        self.fn = fn
        self.config = configparser.ConfigParser()
        self.config.read(self.fn)
        try:
            self.check()
        except Exception as e:
            self.create()
        self.create_result()

    def check(self):
        for block in self.blocks:
            self.check_block(block, self.blocks[block])

    def check_block(self, name, checklist):
        for item in checklist:
            if item not in self.config[name]:
                mes = "Field {} in block {} is not exist!".format(item, name)
                raise KeyError(mes)
            elif self.config[name].getint(item) < 0:
                mes = "Negative valuse of {} in block {}".format(item, name)
                raise ValueError(mes)

    def create_result(self):
        self.result = {section: self.parse_section(self.config[section])
                       for section in self.config.sections()}

    def parse_section(self, section):
        return {key: section.getint(key) for key in section}

    def create(self):
        self.config = configparser.ConfigParser()
        for block in self.blocks:
            self.config[block] = copy.deepcopy(self.blocks[block])
        try:
            with open(self.fn, 'w') as configfile:
                self.config.write(configfile)
        except Exception:
            return
