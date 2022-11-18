import sys

BACKGROUND = 10
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
GYAN = 36
WHITE = 37

BOLD = 1
FADED = 2
ITALIC = 3
UNDERLINE = 4
BLINK = 5
CROSS = 6
FRAME = 51


def FORMAT(text, format: list):
    res = '\033[' + ';'.join(str(i) for i in format) + 'm' + text + '\033[0m'
    # for text_format in format:
    #    res += str(text_format) + ';'
    # res = res[:-1] + '\033[0m'
    return res


def RGB(r, g, b, backgroung=0):
    res = f'{backgroung + 38};2;{r};{g};{b}'
    return res


class ProgressBar:
    def __init__(self, width=40, begin_char='[', space_char=' ', end_char=']', body_char='|', head_char='', progress=0):
        self.toolbar_width = width
        self.beg_char = begin_char
        self.space_char = space_char
        self.end_char = end_char
        self.body_char = body_char
        self.head_char = head_char
        self.index = progress
        self.message_len = 0

    def begin(self):
        sys.stdout.write(f'{self.beg_char}{self.head_char}{self.space_char * (self.toolbar_width - 1)}{self.end_char}')
        sys.stdout.flush()
        self.index = 0

    def step(self, message='', percent=0):
        if self.index < self.toolbar_width:
            if percent:
                self.index = (self.toolbar_width * percent) // 100
            sys.stdout.write(f"\r{self.beg_char}{self.body_char * (self.index + 1)}{self.head_char}"
                             f"{self.space_char * (self.toolbar_width - self.index - 1)}{self.end_char}{message}")
            sys.stdout.flush()
            if not percent:
                self.index += 1
            self.message_len = len(message)
        elif self.index == self.toolbar_width:
            sys.stdout.write('\b\b' + '\b' * self.message_len + f"{self.end_char}{message}\n")
            sys.stdout.flush()
