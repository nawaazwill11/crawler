import re, functools, math
from _html import GrabHTML

class HTMLCrawler(GrabHTML):

    def __init__(self):
        GrabHTML.__init__(self)
        self.counter = 1
        avg_min_salary = []
        avg_max_salary = []
        for file in self.file_handlers:
            print(f'Working on file: {file.name}')
            min_sal, max_sal = self.getAverageSalary(file.read())
            if min_sal != 0 or max_sal != 0:
                avg_min_salary.append(min_sal)
                avg_max_salary.append(max_sal)
        self.log += f'Scanned {len(self.file_handlers)} pages with {self.counter - 1} salary entries\n'

        avg_min_salary, avg_max_salary = self.calculateAverage(avg_min_salary, avg_max_salary)
        self.log += f'Average minimum salary is: {avg_min_salary}\n' + f'Average maximum salary is: {avg_max_salary}'
        print(self.log)
        print('Check log for details')
        writeLog = open(self.path + '/' + '_log.txt', 'w')
        writeLog.write(self.log)
        writeLog.close()
        # ./htmlfiles/web_developers
    
    def getAverageSalary(self, file):
        min_salaries = []
        max_salaries = []
        while True:
            valid = self.getMinMaxSalary(file)
            if valid:
                min_salaries.append(valid[0])
                max_salaries.append(valid[1])
                file = file[valid[2]:]
                # print(len(self.html_file))
            else: break
        
        return self.calculateAverage(min_salaries, max_salaries)
    
    def calculateAverage(self, min_salaries, max_salaries):
        if len(min_salaries) == 0 or len(max_salaries) == 0:
            return [0, 0]
        
        avg_min_salary =  math.ceil(functools.reduce(lambda item, total: item+total, min_salaries) / len(min_salaries))
        avg_max_salary =  math.ceil(functools.reduce(lambda item, total: item+total, max_salaries) / len(max_salaries))

        return [avg_min_salary, avg_max_salary]
        
        
    def getMinMaxSalary(self, file):
        match = re.search("[0-9,\- ]+PA", file)
        if match:
            self.log +=  match.group() + '\n'
            salary_range = match.group()
            min_salary = 0
            max_salary = 0
            match_mns = re.search('[0-9, ]+-', salary_range)
            if match_mns:
                match_mns = match_mns.group()
                min_salary = int("".join(re.search('[0-9,]+', match_mns).group().split(',')))
            match_mxs = re.search('-[0-9, ]+', salary_range)
            if match_mxs:
                match_mxs = match_mxs.group()
                max_salary = int("".join(re.search('[0-9,]+', match_mxs).group().split(',')))
            self.counter += 1
            return [min_salary, max_salary, match.span()[1]]
        return None

   

app = HTMLCrawler()