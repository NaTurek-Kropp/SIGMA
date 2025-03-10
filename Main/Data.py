def NumOfQuestions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return len(lines) // 5

def GetQuestionsDataFixed(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    ALL = []
    #QUESTIONS
    questions = []
    for i in range(0, len(lines), NumOfQuestions(file_path)):
        questionExh = lines[i].strip().split(' ')
        question = []
        for e in questionExh:
            if e.startswith('http://') or e.startswith('https://'):
                questions.append([" ".join(question), e])
            else:
                question.append(e)
        #ANSWERS
        answers = []
        for line in lines[i+1:i+5]:
            answerExh = line.strip().split(' ')
            answer = []
            for e in answerExh:
                if e.startswith('http://') or e.startswith('https://'):
                    answers.append([" ".join(answer), e])
                    answer.clear()
                elif e == answerExh[len(answerExh)-1]:
                    answer.append(e)
                    answers.append([" ".join(answer), ""])
                    answer.clear()
                else:
                    answer.append(e)
        
        ALL.append(answers)
    return questions, ALL



file_path = 'Data/pytania.txt'
questions = GetQuestionsDataFixed(file_path)


class Answers:
    def __init__(self, numOfQuestions):
        self.answersTable = [None] * numOfQuestions

    def AppendAnswer(self,question,answer):
        self.answersTable[question] = answer
    
    def Answers(self):
        return self.answersTable
