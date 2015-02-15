import csv
import curses
import locale
import numpy as np
import time

class MatrixRain(object):
    def __init__(self, path='hex.csv'):
        locale.setlocale(locale.LC_ALL, '')

        self.scr = curses.initscr()
        self.scr.nodelay(1)
        curses.noecho()
        curses.curs_set(0)
        curses.endwin()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        height, width = self.scr.getmaxyx()

        self.height = height
        self.width = width
        self.matrix = np.zeros((height, width))
        self.cloud = np.zeros((width,))
        self.charset = self._import_csv(path)

        self._rain()

    def _import_csv(self, path):
        try:
            open(path, 'rt')
        except TypeError as e:
            print 'Error', e.message
            raise TypeError
        except IOError as e:
            print 'Error', e.strerror
            raise IOError
        finally:
            with open(path, 'rt') as file_:
                reader = csv.reader(file_)

                charset = {}
                for row in reader:
                    index = int(row[0])
                    value = row[1]
                    charset[index] = value

            return charset

    def _rain(self):
        quit = -1
        while quit != ord('q'):
            # create new drop
            slot = np.random.randint(0, self.width)
            if self.cloud[slot] == 0:
                length = np.random.randint(1, self.height)
                self.cloud[slot] = length

            # drops array
            range_ = len(self.charset)
            drops = np.zeros((self.width,))
            for i in range(self.width):
                if self.cloud[i] != 0:
                    drops[i] = np.random.random_integers(1, range_)
                    self.cloud[i] -= 1

            # rain
            self.matrix = np.vstack((drops, self.matrix))
            self.matrix = np.delete(self.matrix, self.height - 1, axis=0)

            # print matrix to screen
            self.scr.clear()
            for i in range(self.height):
                for j in range(self.width):
                    if i == self.height - 1 and j == self.width - 1:
                        continue
                    else:
                        index = self.matrix[i][j]
                        if index != 0:
                            hex_string = self.charset[index]
                            decimal = int(hex_string, 16)
                            utf8 = unichr(decimal)
                            self.scr.addstr(i, j, utf8.encode('utf-8'), curses.color_pair(1))
                        else:
                            self.scr.addstr(i, j, ' ')

            self.scr.refresh()
            time.sleep(0.1)
            quit = self.scr.getch()

        curses.endwin()

if __name__ == '__main__':
    matrix = MatrixRain()
