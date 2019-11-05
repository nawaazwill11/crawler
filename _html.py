import os, re
from urllib.request import Request, urlopen

class GrabHTML(object):

    def __init__(self):
        self.file_handlers = []
        self.log = ''
        self.getFileHandler()

    
    def getFileHandler(self):
        while True:
            self.path = input('Enter the path of folder containing html files:\n-> ').strip()
            # path = './htmlfiles/' + file_name
            if (os.path.exists(self.path)):
                html_files_list = []
                for file in os.listdir(self.path):
                    if os.path.splitext(file)[1] == '.html':
                        html_files_list.append(file)
                break
            print('Invalid path. Retry')
        self.createFileHandler(html_files_list)
    
    def createFileHandler(self, files_list):
        for file in files_list:       
            path = self.path + '/' + file
            self.file_handlers.append(open(path, 'r'))

    def downloadHTMLFiles(self, url, start_page, end_page, directory):
        for i in range(start_page, end_page + 1):
            # if i > 1:
            #     url += '-' + str(i)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
                req = Request(url, headers=headers)
                html = str(urlopen(req).read(), 'utf-8')
                title = re.search('<title>.+</title>', html).group()[7:-8]
                file_name = f'./htmlfiles/{directory}/{title}-{i}.html' 
                file = open(file_name, 'w')
                print(len(html))
                file.write(html)
                file.close()
            except Exception as e:
                print(f'Unable to open page. An exception occured.\n{e}')

# app = GrabHTML()
# app.downloadHTMLFiles('http://www.patkip.com', 10, 20, 'web_developers')