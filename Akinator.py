# !/usr/bin/python
# -*- coding: utf-8 -*-


from Game import *
from Database import *


class Application:
    def __init__(self, database: Database):
        self.__db: Database = database

    def ParseQuestions(self, question):
        qlist = question.split('?')
        qlist = [q.strip(' ?')+'?' for q in qlist if q]
        return qlist

    def ParseVariants(self, variants):
        if not variants:
            variants = 'yes; no; don`t know; irrelevant'
        return [v.strip() for v in variants.split(';') if v]

    def ParseSubjects(self, subject):
        return [s.strip() for s in subject.split(';') if s]

    def StartLoop(self):
        print('Hello!')
        while True:
            command = input(':> ')
            if command in ['help', 'h']:
                print('''command list:
        help, h                     - show this help text.
        add question, add q, addq   - Adding new question.
        add subject, add s, adds    - Adding new subject.
        list                        - listing of all subjects.
        play                        - start game round.
        reset                       - clears database
        exit                        - stop program.''')
            elif command in ['add question', 'add q', 'addq']:
                question = input('Q> ')
                variants = input('V> ')
                questions = self.ParseQuestions(question)
                variants = self.ParseVariants(variants)
                for question in questions:
                    self.__db.AddQuestion(question, variants)
                self.__db.Save()
            elif command in ['add subject', 'add s', 'adds']:
                subject = input('A> ')
                subjects = self.ParseSubjects(subject)
                for subject in subjects:
                    self.__db.AddSubject(subject)
                self.__db.Save()
            elif command == 'list':
                print('Subjects:')
                for subject in db.Subjects:
                    print('- {}: {}'.format(subject.Id, subject.Name))
                print('Questions:')
                for question in db.Questions:
                    print('- {}: {}'.format(question.Id, question.Text))
            elif command == 'play':
                game = Game(self.__db)
                game.StartLoop()
                self.__db.Save()
                print('Game completed!')
            elif command == 'reset':
                self.__db.Reset()
            elif command == 'exit':
                break
            else:
                print('Unknown command \'{}\''.format(command))


'''
Ответы записаны в форме
(id вопроса, id ответа)

Для каждого загаданного объекта есть набор групп ответов на вопросы.

Что бы сосчитать вероятность для конкретного объекта - пробегаемся по всем вопросам
и если для заданного вопроса дан ответ - считаем вероятность объекта в зависимости от ответа
затем подсчитываем общую вероятность для объекта

'''


def CalculateQuestionsProbabilityes(questions):
    global db
    for item in questions:
        quest = item['question']
        for subject in db['subjects']:
            if quest['id'] in subject['answers']:
                group = subject['answers'][quest['id']]


def CalculateAnswerGroupPower(group):
    size = len(group)


def CalculateProbabilityEach(answers):
    global db
    for subject in db['subjects']:
        CalculateProbabilitySingle(subject, answers)


def CalculateProbabilitySingle(subject, answers):
    prob_list = []
    prob_sum = 0
    coef = len(answers)
    for answer in answers:
        qid = str(answer['qid'])
        aid = str(answer['aid'])
        group = GetGroup(subject, qid)
        prob = GetProbabilityByGroup(group, aid) / coef
        prob_list.append(prob)
        prob_sum += prob
    print(' - {: <10}  {:6.2f}'.format(subject['name'], prob_sum))


def GetGroup(subject, qid):
    ans = subject['answers']
    if qid not in ans:
        ans[qid] = {'1': 1, '2': 1, '3': 1, '4': 1}
    return ans[qid]


def GetGroupFullPower(group):
    return group['1'] + group['2'] + group['3'] + group['4']


def GetProbabilityByGroup(group, answer):
    return group[answer] / GetGroupFullPower(group)


def UpdateProbabilityes(subject, answers):
    for answer in answers:
        qid = str(answer['qid'])
        aid = str(answer['aid'])
        group = GetGroup(subject, qid)
        UpdateGroup(group, aid)


def UpdateGroup(group, answer):
    group[answer] += 1


# ------------------------------------------------------------ #

config_path = 'akinator.database.json'

if __name__ == '__main__':
    db = Database(config_path)
    db.Load()

    app = Application(db)
    app.StartLoop()
    print('Thanx for playing!')
