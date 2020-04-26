import json

END_CHARACTER = "\0"
TARGET_ENCODING = "utf-8"

class Send:

    def __init__(self, username="", city="", start=False, move=False, q=True, answer=None):
        self.username = username
        self.city = city
        self.start = start
        self.move = move
        self.q = q
        self.answer = answer

    def getCity(self):
        return "Город " + self.city + "."

    def getStart(self):
        if self.start:
            return "Игра началась. Вы играете против " + self.username + "."
        else:
            return "Игра не началась. Дождитесь подключения"

    def getMove(self):
        if self.move:
            return "Ваш ход."
        else:
            return "Ждите ход соперника."

    def getAnswer(self):
        if self.answer == None:
            return
        if self.answer:
            return "Вы выиграли."
        else:
            return "Вы програли."


    def __str__(self):
        return "Send(username='{}', city='{}', start='{}', move='{}', q='{}', answer='{}')".format(self.username, self.city, self.start, self.move, self.q, self.answer)

    def marshal(self):
        return (json.dumps(self.__dict__) + END_CHARACTER).encode(TARGET_ENCODING)
