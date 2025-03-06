def GetQuestionsData(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    questions = []
    for i in range(0, len(lines), 5):
        question = lines[i].strip()
        answersWithImages = [tuple(line.strip().split(' ')) for line in lines[i+1:i+5]]
        questions.append((question, answersWithImages))
    
    return questions

file_path = 'Data/pytania.txt'
questions = GetQuestionsData(file_path)

for question, answersWithImages in questions:
    for answer in answersWithImages:
        print((answer))

class Answers:
    def __init__(self):
        self.answersTable = []

    def AppendAnswer(self, answer):
        self.answersTable.append(answer)
