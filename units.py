from exeptions import *


class Dot:
    """Класс точек на поле"""
    def __init__(self, x: int, y:  int):
        self.x = x
        self.y = y

    """Метод сравнения точек"""
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    """Магический метод для вывода точек в виде списка, для удобства отладки"""
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    """Класс корабля"""
    def __init__(self, dot, size, direction):
        """direction - направление корабля (вертикальное(0)/горизонтальное(1)), bow - точка, где размещен нос"""
        self.dot = dot  # Передаем сюда точку (класс Dot) с координатами
        self.size = size
        self.direction = direction
        self.lives = size

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.size):
            cur_x = self.dot.x
            cur_y = self.dot.y

            if self.direction == 0:
                cur_x += i

            elif self.direction == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    """shot в данном случае точка класса Dot для проверки попадания по кораблю"""
    def shooten(self, shot):
        return shot in self.dots


class Board:
    """Класс игровой доски"""

    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid

        self.count = 0  # Счетчик уничтоженных кораблей

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    """Перегрузка метода __str__ для вывода доски на экран с помощью строки"""
    def __str__(self):
        res = ""
        res += " | 1 | 2 | 3 | 4 | 5 | 6 |"

        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")

        return res

    def out(self, dot):
        """Метод, который проверяет, вышла ли точка за пределы поля"""
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        """Метод, который обводит корабли по контуру"""
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    """В этот метод передаем класс корабля"""
    def add_ship(self, ship):
        """Метод, который ставит корабли на доску"""
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot):
        """Выстрел по доске"""
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

            self.field[dot.x][dot.y] = "."
            print("Мимо!")
            return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


