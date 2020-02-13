from functools import reduce


class AnswerGroup:
    def __init__(self, value):
        self.__value = value

    def GetSumm(self):
        return reduce(lambda a, b: a + b, self.__value)

    def GetProbability(self, answer):
        return self.__value[answer] / self.GetSumm()

    # Мой самодельный алгоритм нахождения энтропии
    # Он отличается от валидного, но зато мне лично всё понятно
    # Валидный с логарифмами: https://ru.wikipedia.org/wiki/Информационная_энтропия
    # В моём варианте я перемножаю все вероятности и нормирую до интервала [0 .. 1]
    def GetNormalizedEnthropy(self):
        _sum = self.GetSumm()
        _prob_list = [v / _sum for v in self.__value]
        # Добавляем нормировочный коэффициент в список
        # Коэффициент подобрал интуитивно-эмпирически, но я уверен что его можно вывести из самой формулы перемножения
        power = len(self.__value)
        _prob_list.append(power ** power)
        # Всё перемножаем
        return reduce(lambda a, b: a * b, _prob_list)

    # Упрощённый вариант энтропии
    # На самом деле засчёт отсутствия нормализации он даже более пригоден для более точного сопоставления того,
    # какой вопрос имеет более или менее случайные ответы.
    # Но при условии что наборы ответов идентичны у всех вопросов.
    # В противном случае вопрос с бОльшим числом вариантов ответов будет иметь меньшую энтропию.
    # Тогда лучше использовать нормализованную версию
    def GetEnthropy(self):
        return reduce(lambda a, b: a * b, self.__value)

    def ApplyAnswer(self, answer):
        self.__value[answer] += 1
