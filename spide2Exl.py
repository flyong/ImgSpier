from selenium import webdriver
import re,random,time,random,os
from lxml import html
from lxml import etree
import xlwt
import xlrd
from xlwt import Workbook
from xlutils.copy import copy
from urllib import request
from selenium.webdriver.chrome.options import Options

# def get_url(group):
#     urls=[]
#     file_object = open("C:\\Users\\litao\\OneDrive - tongji.edu.cn\\大四下\\信息中心\\杂\\爬虫\\test1.txt",'rU')
#     try: 
#         pattern = re.compile('.*'+group+'.*')
#         for line in file_object:
#             if pattern.match(line):    
#                 urls.append(line)
#     finally:
#         file_object.close()
#     return urls

def writeTitle(fileName,sheetName):
    title=['分组','项目名称','专家（单位）1','','专家2','','专家3','','专家4','','专家5','','第1作者','','第2作者','','贡献单位']
    f=xlrd.open_workbook(fileName, formatting_info=True)
    f=copy(f)
    s1=f.add_sheet(sheetName,cell_overwrite_ok=True)
    for i in range(len(title)):
        s1.write(0,i,title[i])
    f.save(fileName)

def createExl(fileName):
    f=xlwt.Workbook()
    f.add_sheet('sheet1',cell_overwrite_ok=True)  
    f.save(fileName)  

def spiderPart(urls,fileName,sheetName,index):
    #进入二级分组
    #writeTitle(fileName,sheetName)
    for url in urls:
        stepIn(url,fileName,index)

def Start():
    startUrl=r""
    urls=urlSpider.get_url(startUrl)

    #fileName=r'result.xls'
    #createExl(fileName)

    spiderPart(urlSpider.selectUrl('zr',urls),fileName,"自然科学奖",1)
    spiderPart(urlSpider.selectUrl('fm',urls),fileName,"技术发明奖",2)
    spiderPart(urlSpider.selectUrl('jb',urls),fileName,"科技进步奖",3)
    

def stepIn(url,filename,sheetNum):
    #进入二级，遍历三级网页,写入数据(每读完一个二级目录写一次)

    wb= xlrd.open_workbook(filename, formatting_info=True)    
    sheet=wb.sheet_by_index(sheetNum)        
    rowIndex=sheet.nrows
    wb=copy(wb)
    newSheet=wb.get_sheet(sheetNum)
    
    wb.save(filename)
   
    nextStepIn=[]
    if sheetNum!=3:
        nextStepIn=nextStepIn1
    else:
        nextStepIn=nextStepIn2

    for link in urlSpider.get_links(url):
        result=nextStepIn(link,sheetNum)
        colIndex=0        
        newSheet.write(rowIndex,colIndex,result.group)
        colIndex=1
        newSheet.write(rowIndex,colIndex,result.name)
        
        if isinstance(result.professor,str):
            colIndex=colIndex+1
            newSheet.write(rowIndex,colIndex,result.professor)
        else:
                for professor in result.professor:
                    colIndex=colIndex+1
                    newSheet.write(rowIndex,colIndex,professor)
        colIndex=11
        for author in result.author:
            colIndex=colIndex+1
            newSheet.write(rowIndex,colIndex,author)
        colIndex=20
        if isinstance(result,items.ResearchItem2):            
            colIndex=colIndex+1
            newSheet.write(rowIndex,colIndex,result.depart)
        rowIndex+=1
    
  
    
 
def nextStepIn1(url,num):
    #第一二部分
    nextBrow=webdriver.PhantomJS()
    nextBrow.get(url)
    #time.sleep(random.random())

    page=etree.HTML(nextBrow.page_source)
    a=page.xpath('//tbody/tr[3]/t')
    if page.xpath('//tbody/tr')[2][0].text=='提名专家：':
        group=page.xpath('//tbody/tr[1]/td[2]/text()')
        name=page.xpath('//*[@style="PADDING-LEFT: 0.5em"]/text()')[1]#项目名称        

        professor=[]
        c=page.xpath('//tbody/tr[3]/td/ol/li')
        for x in c:
            str=x.xpath('string(.)')
            professorname=re.search(r'(?<=姓名：).*?(?=工作)',str)[0]            
            professor.append(professorname)
            professord=re.search(r'(?<=工作单位：).*?(?=技术职称)',str)[0]
            professor.append(professord) 
        d=page.xpath('//tbody/tr['+('%d' %(5+num))+']/td/ol/li')
        author=[]
        for x in d:
            str=x.xpath('string(.)')
            authorname=re.search(r'(?<=姓名：).*?(?=排名)',str)[0]
            author.append(authorname)
            authorDepart=re.search(r'(?<=工作单位：).*?(?=对本项目)',str)[0]
            author.append(authorDepart)
        nextBrow.close()
        return items.ResearchItem1(group,name,professor,author)
    else:
        group=page.xpath('//tbody/tr[1]/td[2]/text()')#项目分组
        a=page.xpath('//*[@style="PADDING-LEFT: 0.5em"]/text()')#项目名称        
        name=a[1]
        depart=a[2]
        
        d=page.xpath('//tbody/tr['+('%d' %(6+num))+']/td/ol/li')
        author=[]
        for x in d:
            str=x.xpath('string(.)')
            authorname=re.search(r'(?<=姓名：).*?(?=排名)',str)[0]
            author.append(authorname)
            authorDepart=re.search(r'(?<=工作单位：).*?(?=对本项目)',str)[0]
            author.append(authorDepart)      
        nextBrow.close()   
        return items.ResearchItem1(group,a[1],a[2],author)
    
def nextStepIn2(url,num):
    #第三部分
    num=num-1
    nextBrow=webdriver.PhantomJS()
    nextBrow.get(url)
    #time.sleep(random.random())

    page=etree.HTML(nextBrow.page_source)
    a=page.xpath('//tbody/tr[3]/t')
    if page.xpath('//tbody/tr')[2][0].text=='提名专家：':
        group=page.xpath('//tbody/tr[1]/td[2]/text()')
        name=page.xpath('//*[@style="PADDING-LEFT: 0.5em"]/text()')[1]#项目名称        

        professor=[]
        c=page.xpath('//tbody/tr[3]/td/ol/li')
        for x in c:
            str=x.xpath('string(.)')
            professorname=re.search(r'(?<=姓名：).*?(?=工作)',str)[0]            
            professor.append(professorname)
            professord=re.search(r'(?<=工作单位：).*?(?=技术职称)',str)[0]
            professor.append(professord) 
        d=page.xpath('//tbody/tr['+('%d' %(5+num))+']/td/ol/li')
        author=[]
        for x in d:
            str=x.xpath('string(.)')
            authorname=re.search(r'(?<=姓名：).*?(?=排名)',str)[0]
            author.append(authorname)
            authorDepart=re.search(r'(?<=工作单位：).*?(?=对本项目)',str)[0]
            author.append(authorDepart)
        e=page.xpath('//tbody/tr['+('%d' %(6+num))+']/td/ol/li')
        for x in e:
            str=x.xpath('string(.)')
            authorname=re.search(r'(?<=单位名称：).*?(?=单位)',str)[0]
            author.append(authorname)
        nextBrow.close()
        return items.ResearchItem2(group,name,professor,author)
    else:
        group=page.xpath('//tbody/tr[1]/td[2]/text()')#项目分组
        a=page.xpath('//*[@style="PADDING-LEFT: 0.5em"]/text()')#项目名称        
        name=a[1]
        depart=a[2]
        
        d=page.xpath('//tbody/tr['+('%d' %(6+num))+']/td/ol/li')
        author=[]
        for x in d:
            str=x.xpath('string(.)')
            authorname=re.search(r'(?<=姓名：).*?(?=排名)',str)[0]
            author.append(authorname)
            authorDepart=re.search(r'(?<=工作单位：).*?(?=对本项目)',str)[0]
            author.append(authorDepart) 
        
        e=page.xpath('//tbody/tr['+('%d' %(7+num))+']/td/ol/li')
        for x in e:
            str=x.xpath('string(.)')
            authorname=re.search(r'(?<=单位名称：).*?(?=单位)',str)[0]
            author.append(authorname)
        nextBrow.close()   
        return items.ResearchItem2(group,a[1],a[2],author)

def crawlImg(url):
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)    

    page=etree.HTML(driver.page_source) 
    group=page.xpath('//tbody/tr[1]/td[2]/text()')[0]#分组
    name=page.xpath('//*[@style="PADDING-LEFT: 0.5em"]/text()')[1]#项目名称
    
    path="C:\\result\\"+str(group)+'\\'+str(name)
    if os.path.exists(path) is False:
        os.makedirs(path)#创建目录

    imgs=driver.find_elements_by_xpath('//img')
    index=1
    for img in imgs[2:]:
        img_url=img.get_attribute('src')
        pic_name =str(name) + str(index)+'.jpg'
        index=index+1
        file_name = os.path.join(path, pic_name)
        downloadImg(img_url,file_name)
        #urlretrieve(url=img_url,filename=pic_name)
    driver.close()  

def downloadImg(url,filename):
    global headers
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive'}
    
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        req = request.Request(url = url, headers = headers)
        binary_data = request.urlopen(req).read()
        temp_file = open(filename, 'wb') #创建文档
        temp_file.write(binary_data)#将二进制文件写入文档中
        temp_file.close()
        return True
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        if os.path.exists(filename):
            os.remove(filename)

def getTitle(html):
    soup = BeautifulSoup(html, 'lxml')
    doc=lxml.html.fromstring(html)
    return doc.xpath('//*[@id="page_title"]')

def main():
	start()

main()
