#coding:utf-8
import os
class MyNode:
    def __init__(self):
        self.father=0
        self.sons=[]
        self.content=0
    def getFather(self):
        return self.father
    def setFather(self,father):
        self.father=father
    def addSon(self,son):
        son.setFather(self)
        self.sons.append(son)
    def setContent(self,content):
        self.content=content
    def lines(self):
        result=[]
        result.append(self.content)
        for s in self.sons:
            for l in s.lines():
                result.append("\t"+l)
        return result
    def show(self):
        result=self.lines()
        for l in result:
            print(l)
    def getLastChild(self):
        return self.sons[-1]
    def tag(self,content,tag,c=""):
        return "<"+tag+" class=\""+c+"\">"+content+"</"+tag+">"
    def pekiaTagHref(self,content,url=""):
        if url=="":
            url="http://zh.wikipedia.org/wiki/"+content
        return "<a href=\""+url+"\">"+content+"</a>"
    def htmShow(self):
        sonStr=""
        if len(self.sons)>0:
            for s in self.sons:
                sonStr+=s.htmShow()
            sonStr=self.tag(sonStr,"ul")
        result=self.tag(self.tag(self.pekiaTagHref(self.content),"span")+sonStr,"li")
        return result
    def treeWrap(self):
        return self.tag(self.tag(self.htmShow(),"ul","tree"),"div","wrapper")
class Analyzer:
    def __init__(self):
        self.filePath=0
        self.trees=[]
        self.core=0
        self.currentDepth=0
        self.currentLine=0
    def setFile(self,filePath):
        self.filePath=filePath
    def parser(self):
        f=open(self.filePath,"r")
        counter=0
        for l in f.readlines():
            counter+=1
            #print("line:"+str(counter)+"currentTabNum:"+str(self.currentDepth)+" content:"+l)
            self.setCurrentLine(l)
            v=self.getVaryDepth(counter)
            if v==0:
                pass
            else:
                if v>0:
                    self.down()
                else:
                    self.up(v)
            self.append(l,v)
            self.currentDepth+=v
        f.close()
    def down(self):
        #print("down() currentDepth:"+str(self.currentDepth))
        if self.currentDepth==0:
            self.core=self.trees[-1]
        else:
            self.core=self.core.getLastChild()
    def up(self,v):
        if self.currentDepth>0:
            n=abs(v)
            for i in range(n):
                self.core=self.core.getFather()
    def append(self,line,v):
        realIn=line.strip()
        if len(realIn)==0:
            return
        if (self.currentDepth+v)==0:
            newTree=MyNode()
            newTree.setContent(realIn)
            self.trees.append(newTree)
            self.core=self.trees[-1]
        else:
            newNode=MyNode()
            newNode.setContent(realIn)
            self.core.addSon(newNode)
    def setCurrentLine(self,line):
        self.currentLine=line
    def getTabNum(self,line):
        result=0
        lenth=len(line)
        flag=0
        downFlag=0
        for i in range(lenth):
            if line[i]=='\t':
                result+=1
            else:
                if line[i]==' ':
                    flag+=1
                else:
                    downFlag=1
                if flag==4:
                    flag=0
                    result+=1
                if downFlag==1:
                    break
        return result
    def getVaryDepth(self,line):
        cLen=self.getTabNum(self.currentLine)
        result=cLen-self.currentDepth
        if result>1:
            self.error("too much tab or space in one line",line)
        return result
    def getCurrentContent(self):
        return self.currentLine.strip()
    def error(self,msg,line):
        print("error at line: "+str(line)+" , message:"+msg)
        exit()
    def getTrees(self):
        return self.trees
class Translator:
    def __init__(self):
        self.trees=[]
        self.headHtm="<html><head><title>HTML &amp; CSS tree</title><style type=\"text/css\"> body{background-color:#303030}span{color:#00ffff} ul.tree {  overflow-x: auto;  white-space: nowrap;  }ul.tree,ul.tree ul {  width: auto;  margin: 0;  padding: 0;  list-style-type: none;}ul.tree li {  display: block;  width: auto;  float: left;  vertical-align: top;  padding: 0;  margin: 0;}ul.tree ul li {  background-image: url(data:image/gif;base64,R0lGODdhAQABAIABAAAAAP///ywAAAAAAQABAAACAkQBADs=);  background-repeat: repeat-x;  background-position: left top;}ul.tree li span {  display: block;  width: 5em;  /*    uncomment to fix levels    height: 1.5em;  */  margin: 0 auto;  text-align: center;  white-space: normal;  letter-spacing: normal;}</style><!--[if IE gt 8]> IE 9+ and not IE --><style type=\"text/css\">ul.tree ul li:last-child {  background-repeat: no-repeat;  background-size:50% 1px;  background-position: left top;}ul.tree ul li:first-child {  background-repeat: no-repeat;  background-size: 50% 1px;  background-position: right top;}ul.tree ul li:first-child:last-child {  background: none;}ul.tree ul li span {  background: url(data:image/gif;base64,R0lGODdhAQABAIABAAAAAP///ywAAAAAAQABAAACAkQBADs=) no-repeat 50% top;  background-size: 1px 0.8em;  padding-top: 1.2em;}ul.tree ul {  background: url(data:image/gif;base64,R0lGODdhAQABAIABAAAAAP///ywAAAAAAQABAAACAkQBADs=) no-repeat 50% top;  background-size: 1px 0.8em;  margin-top: 0.2ex;  padding-top: 0.8em;}</style><style type=\"text/css\">body {  font-family:sans-serif;  color: #666;  text-align: center;}A, A:visited, A:active {  color: #00ffff;  text-decoration: none;}A:hover {  text-decoration: underline;}ul.tree,div.wrapper {  width: 960px;  margin: 0 auto;}ul.tree {  width: 650px;}.clearer {  clear: both;}p {  margin-top: 2em;}</style></head><body>"
        self.btnHtml="</body></html>"
    def setTrees(self,ts):
        self.trees=ts
    def getHtmlTrees(self):
        result=""
        for t in self.trees:
            result+=t.treeWrap()
        result=self.headHtm+result+self.btnHtml
        return result
    def writeHtmlToFile(self,url):
        f=open(url,"w")
        f.write(self.getHtmlTrees())
        f.close()
class AllMapper:
    def __init__(self):
        self.inPath=0
        self.outPath=0
    def setIO(self,i,o):
        self.inPath=i
        self.outPath=o
    def map(self):
        an=Analyzer()
        an.setFile(self.inPath)
        an.parser()
        tran=Translator()
        tran.setTrees(an.getTrees())
        tran.writeHtmlToFile(self.outPath)

def testNode():
    node1=MyNode()
    node1.setContent("n1")
    node2=MyNode()
    node2.setContent("n2")
    node3=MyNode()
    node3.setContent("n3")
    node4=MyNode()
    node4.setContent("n4")

    node1.addSon(node3)
    node1.addSon(node2)

    node3.addSon(node4)
    node1.show()
def testAnalyzer():
    a=Analyzer()
    a.setFile("/Users/luo/Desktop/file")
    a.parser()
    trees=a.getTrees()
    for tree in trees:
        tree.show()
def testTranslator():
    a=Analyzer()
    a.setFile("/Users/luo/Desktop/file")
    a.parser()
    trans=Translator()
    trans.setTrees(a.getTrees())
    print(trans.getHtmlTrees())

def mainFunc():
    product()

def product():
    file_list=[f for f in os.listdir('.') if os.path.isfile(os.path.join('.',f))]
    dirPath=os.getcwd()
    treeList=[f for f in file_list if f.endswith(".tree")]
    targets=[]
    outs=[]
    count=0
    for i in treeList:
        count+=1
        targets.append(dirPath+"/"+i)
        outs.append(dirPath+"/"+str(count)+".html")
    for i in range(count):
        am=AllMapper()
        am.setIO(targets[i],outs[i])
        am.map()

mainFunc()


