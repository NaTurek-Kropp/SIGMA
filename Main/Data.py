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
    for i in range(0, len(lines), 5):
        questionExh = lines[i].strip().split(' ')
        question = []
        has_link = False
        for e in questionExh:
            if e.startswith('http://') or e.startswith('https://'):
                questions.append([" ".join(question), e])
                question.clear()
                has_link = True
            else:
                question.append(e)
        if not has_link:
            questions.append([" ".join(question), "https://th.bing.com/th/id/R.5c0d878025129c09413bd39fbe3861e1?rik=59PQbUvuzaeGEw&riu=http%3a%2f%2f3.bp.blogspot.com%2f-dUzAJBVUsgI%2fVzkbCJPVm2I%2fAAAAAAAABYk%2fOL1zPvLSHZYzbIUVvFJJgLla7YRmwhYmwCHM%2fw1200-h630-p-k-no-nu%2fwhite-color.jpg&ehk=XIdYEFjQBXOooQ4XC9XosZ%2fzlqslBdDM1HgDBgPcSdk%3d&risl=&pid=ImgRaw&r=0"])
        #ANSWERS
        answers = []
        for line in lines[i+1:i+5]:
            answerExh = line.strip().split(' ')
            answer = []
            for e in answerExh:
                if e.startswith('http://') or e.startswith('https://') :
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
 
def GetLastLine(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines[-1].strip() if lines else None


file_path = 'ProjectData/pytania.txt'

questions = GetQuestionsDataFixed(file_path)

class Answers:
    def __init__(self, numOfQuestions):
        self.answersTable = [None] * numOfQuestions

    def AppendAnswer(self,question,answer):
        self.answersTable[question] = answer
    
    def Answers(self):
        return self.answersTable