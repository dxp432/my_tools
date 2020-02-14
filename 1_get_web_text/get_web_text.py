import tkinter as tk
import requests
from lxml import etree
import tkinter.messagebox
import re
import os
import requests
from bs4 import BeautifulSoup
import webbrowser

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36"
}  # 模拟手机


root = tk.Tk()

root.title('获取网页文本小工具--微信公众账号：小鹏同学')

# 第3步，设定窗口的大小(长 * 宽)
root.geometry('1000x300')  # 这里的乘是小x

label_1 = tk.Label(root, text="填入网页地址：")
label_1.grid(column=0, row=0)

# 第4步，在图形界面上设定输入框控件entry并放置控件
e2 = tk.Entry(root, width=60, show=None, font=('Arial', 14))  # 显示成明文形式
e2.grid(column=1, row=0)


def getHTMLText(url):
    kv = {'User-agent': 'Baiduspider'}
    try:
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


def findPList(html):
    plist = []
    soup = BeautifulSoup(html, "html.parser")
    plist.append(soup.title.string)
    for div in soup.find_all('div', attrs={"class": "bd doc-reader"}):
        plist.extend(div.get_text().split('\n'))

    plist = [c.replace(' ', '') for c in plist]
    plist = [c.replace('\x0c', '') for c in plist]
    return plist



def deletefile():
    path = '正文.txt'  # 文件路径
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)
        # os.unlink(path)
    else:
        # print('deletefile no such file')  # 则返回文件不存在
        pass

def printPList(plist, path='正文.txt'):
    file = open(path, 'w', encoding='utf-8')
    for str in plist:
        file.write(str)
        file.write('\n')
    file.close()


def get_num(url):
    response = requests.get(url, headers=headers).text
    # print("response:")
    # print(response)
    # re 模块，它提供 Perl 风格的正则表达式模式。re.search 扫描整个字符串并返回第一个成功的匹配。如：(11, 14)
    result = re.search(
        r'&md5sum=(.*)&sign=(.*)&rtcs_flag=(.*)&rtcs_ver=(.*?)".*rsign":"(.*?)",', response, re.M | re.I)  # 寻找参数
    reader = {
        "md5sum": result.group(1),
        "sign": result.group(2),
        "rtcs_flag": result.group(3),
        "rtcs_ver": result.group(4),
        "width": 176,
        "type": "org",
        "rsign": result.group(5)
    }

    result_page = re.findall(
        r'merge":"(.*?)".*?"page":(.*?)}', response)  # 获取每页的标签
    print(result_page)
    if len(result_page) == 1:
        print('只有一个result_page,所以用其他python爬虫方法')
        deletefile()
        html = getHTMLText(url)
        plist = findPList(html)
        # 把结果写到文件里
        print("把结果写到文件里result.txt")
        printPList(plist)
    else:
        doc_url = "https://wkretype.bdimg.com/retype/merge/" + url[29:-5]  # 网页的前缀
        n = 0
        # print(len(result_page))
        for i in range(len(result_page)):  # 最大同时一次爬取10页
            # print(i)
            print('进入for')
            if i % 10 is 0:
                # i 为0,10,20,30,40....
                print('进入if没有起到作用----------')
                doc_range = '_'.join([k for k, v in result_page[n:i]])
                reader['pn'] = n + 1
                reader['rn'] = 10
                reader['callback'] = 'sf_edu_wenku_retype_doc_jsonp_%s_10' % (
                    reader.get('pn'))
                reader['range'] = doc_range
                n = i
                print(doc_url)
                print(reader)
                get_page(doc_url, reader)
        else:  # 剩余不足10页的
            print('进入剩余不足10页的-------------------')
            doc_range = '_'.join([k for k, v in result_page[n:i + 1]])
            reader['pn'] = n + 1
            reader['rn'] = i - n + 1
            reader['callback'] = 'sf_edu_wenku_retype_doc_jsonp_%s_%s' % (
                reader.get('pn'), reader.get('rn'))
            reader['range'] = doc_range
            print(doc_url)
            print(reader)
            get_page(doc_url, reader)


def get_page(url, data):
    response = requests.get(url, headers=headers, params=data).text
    response = response.encode(
        'utf-8').decode('unicode_escape')  # unciode转为utf-8 然后转为中文
    response = re.sub(r',"no_blank":true', '', response)  # 清洗数据
    result = re.findall(r'c":"(.*?)"}', response)  # 寻找文本匹配
    result = '\n'.join(result)
    print(result)
    # 把结果写到文件里
    print("正文.txt")
    f = open('正文.txt', 'a')
    f.write(result)
    f.close()


def get_text():
    InsertUrl = e2.get()
    if InsertUrl.find('bilibili') >= 0:
        url = InsertUrl
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        page_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath("//div[@class='article-holder']//text()")
        if li_list:
            printPList(li_list)
    elif InsertUrl.find('360doc') >= 0:
        url = InsertUrl
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        page_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath("//td[@id='artContent']//text()")
        if li_list:
            printPList(li_list)
    elif InsertUrl.find("baidu") >= 0:
        get_num(InsertUrl)
    else:
        tkinter.messagebox.showinfo('不支持，请重新填', '暂不支持这个网站的提取，可以去获取最新工具或和我联系。')


# 第6步，创建并放置两个按钮分别触发两种情况
b1 = tk.Button(root, text='点击获取正文', width=15, command=get_text)
b1.grid(column=2, row=0)

label_2 = tk.Label(root, text=" ")
label_2.grid(column=0, row=1, columnspan=8)

label_2 = tk.Label(root, text="点击完“点击获取正文”后请在本地查看生成的txt文本结果。")
label_2.grid(column=0, row=2, columnspan=8)

label_2 = tk.Label(root, text="本工具目前仅支持提取的类型：百度文库的word类型文件，360doc个人故事馆，bilibili专栏")
label_2.grid(column=0, row=3, columnspan=8)

label_2 = tk.Label(root, text="本工具目前不支持提取的类型：不支持百度文库的ppt、excel类型和其他网页。")
label_2.grid(column=0, row=4, columnspan=8)

label_2 = tk.Label(root, text="版本：v1.0")
label_2.grid(column=0, row=8, columnspan=8)

label_2 = tk.Label(root, text="本工具开源、免费。")
label_2.grid(column=0, row=9, columnspan=8)

label_3 = tk.Label(root, text="想获取最新工具，请欢迎关注微信公众账号：小鹏同学   或 https://github.com/dxp432")
label_3.grid(column=0, row=10, columnspan=8)


# 此处必须注意，绑定的事件函数中必须要包含event参数
def open_url(event):
    webbrowser.open("https://github.com/dxp432", new=0)


# 绑定label单击时间
label_3.bind("<Button-1>", open_url)

# 进入消息循环
root.mainloop()
