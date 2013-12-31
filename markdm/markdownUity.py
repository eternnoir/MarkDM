import markdown

class markdownUity:
    markdown_options = ['extra', 'codehilite']
    
    def __init__(self):
        self.markdown_options = ['extra', 'codehilite']
        
    def setUpOptions(self,options):
        self.markdown_options = options

    def mdToHtml(self,markdownString):
        html = markdown.markdown(markdownString,self.markdown_options)
        return html

    def mdToHtmlByPath(self,Path):
        file = open(Path).read().decode('utf-8')
        return self.mdToHtml(file)
