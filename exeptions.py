
class BoardExeption(Exception):
    pass


class BoardOutException(BoardExeption):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску"


class BoardUsedException(BoardExeption):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardExeption):
    pass
