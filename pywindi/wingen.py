from pywindi.winclient import Winclient

class Generator:
    def __init__(self, name):
        self.name = name
        self._lines = []
        self.client = Winclient()


    def add_line(self, line, same=False):
        if same:
            self._lines.append(self.count_tabs(self._lines[-1]) * '\t' + line + '\n')
            return
        if len(self._lines) != 0:
            up = self._lines[-1]
            if up.endswith(':\n'):
                line = (self.count_tabs(up) + 1) * '\t' + line
            elif up.startswith('\n'):
                index = -1
                while self._lines[index] == '\n':
                    index -= 1
                indent = self.count_tabs(self._lines[index]) + index + 2
                line = indent * '\t' + line
        self._lines.append(line + '\n')


    def count_tabs(self, string):
        tabs = 0
        for chr in string:
            if chr != '\t':
                break
            tabs += 1
        return tabs


    def get_content(self):
        return ''.join(self._lines)


    def normalize(self, str):
        return str.replace(' ', '_').lower()


    def list_to_string(self, list):
        return ('[' + self.normalize(','.join(list)) + ']').replace(',', ', ')


    def generate(self):
        properties = self.client.get_device(self.name).get_properties()
        self.add_line('class {}(Windevice):'.format(self.name.replace(' ', '_')))
        self.add_line('def __init__(self, winclient, indi_device):')
        self.add_line('super().__init__(winclient, indi_device)')
        self.add_line('\n')
        for p in properties:
            self.add_line('def set_{}(self, **kwargs):'.format(self.normalize(p)))
            self.add_line('properties_list = {}'.format(self.list_to_string(properties[p])))
            self.add_line('self.set_global_property({}, properties_list, **kwargs)'.format(p), True)
            self.add_line('\n')
        self.write()


    def write(self):
        f = open('{}.py'.format(self.normalize(self.name)), mode='w+')
        f.write(self.get_content())
        f.close()



generator = Generator('SBIG CCD')
generator.generate()
