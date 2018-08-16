class Generator:
    _lines = []

    def add_line(self, line):
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


generator = Generator()
generator.add_line('class SBIG:')
generator.add_line('def hello(self, what):')
generator.add_line('print("hello world")')
generator.add_line('\n')
generator.add_line('def hello(self, what):')
generator.add_line('print("hello world")')
f = open('sbig.py', mode='w+')
f.write(generator.get_content())
f.close()
