from selenium import webdriver
import re,random,time,random,os
from lxml import html
from lxml import etree
from urllib import request
from selenium.webdriver.chrome.options import Options


def Start():
    global headers
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive'}

    startUrl=r""
    urls=get_url(startUrl)
    #for url in selectUrl('zr',urls)[6:]:
        #spiderPart(url)    
    #for url in selectUrl('fm',urls):
        #spiderPart(url)
    for url in selectUrl('jb',urls)[10:]:
        spiderPart(url)
    
def spiderPart(url):
    #进入二级分组
    for link in get_links(url):#获取并访问底层url
        crawlImg(link)


def crawlImg(url):
    global chrome_option
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_option)
    driver.get(url)    

    page=etree.HTML(driver.page_source) 
    group=page.xpath('//tbody/tr[1]/td[2]/text()')[0]#分组
    name=page.xpath('//*[@style="PADDING-LEFT: 0.5em"]/text()')[1]#项目名称
    
    #path="C:\\result\\"+str(group)+'\\'+str(name)
    path='result\\'+str(group).strip()+'\\'+str(name).strip()
    if os.path.exists(path) is False:
        os.makedirs(path)#创建目录
        
    imgs=driver.find_elements_by_xpath('//img')
    index=1
    for img in imgs[2:]:
        img_url=img.get_attribute('src')
        pic_name =str(name).strip() + str(index)+'.jpg'
        index=index+1
        file_name = os.path.join(path, pic_name)
        if os.path.exists(file_name):
            return False
        if downloadImg(img_url,file_name) is False:
            file_name=os.path.join(path,'warnning.txt')
            if os.path.exists(file_name) is False:
                with open(file_name, 'w') as f:
                    f.write('wrong way')
                f.close()            
            time.sleep(15)
        time.sleep(random.random())
    driver.close()  

def downloadImg(url,filename):
    
    global headers
    try:
        req = request.Request(url = url, headers = headers)
        binary_data = request.urlopen(req).read()
        temp_file = open(filename, 'wb') #创建文档
        temp_file.write(binary_data)#将二进制文件写入文档中
        temp_file.close()
        time.sleep(random.random(60))
        return True
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
        return False
    except Exception:
        if os.path.exists(filename):
            os.remove(filename)
        return False

def get_url(startUrl):
    brow = webdriver.Chrome()
    brow.get(startUrl)
    herfs= brow.find_elements_by_xpath('//*[@href]')#获取下一级链接
    urls=[]
    for herf in herfs:
        temp=herf.get_attribute('href')
        urls.append(temp.strip('\n'))
    brow.close()
    return urls

def selectUrl(group,urls):
    result=[]
    pattern = re.compile('.*'+group+'.*')
    for line in urls:
        if pattern.match(line):    
            result.append(line)
    return result

def get_links(url):
    #获取底层url
    brow = webdriver.Chrome()
    brow.get(url)
    herfs= brow.find_elements_by_xpath('//*[@href]')#获取下一级链接
    urls=[]
    for herf in herfs:
        urls.append(herf.get_attribute('href'))
    brow.close()
    return urls


def main():
    Start()
    
main ()