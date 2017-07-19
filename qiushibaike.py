import urllib
import urllib.request
import re
import threading
import time

class QSBK:

    # 初始化方法，定义变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量
        self.stories = []
        # 存放程序能否继续运行的变量
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的request
            request = urllib.request.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib.request.urlopen(request)
            # 将页面转化为utf-8代码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib.request.URLError as e:
            if hasattr(e,'reason'):
                print(u"连接糗事百科失败啦~错误原因", e.reason)
                return None

    # 传入某一页码，返回本页段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败啦~")
            return None
        pattern = re.compile('<div class="author clearfix">.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)'
                         '</div>.*?<div class="stats">.*?class="number">(.*?)</i>.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储每页的段子们
        pageStories = []
        # 遍历正则表达式匹配的信息
        for item in items:
            # haveImg = re.search("img",item[3])
            # if not haveImg:
            text = re.sub(r'<span>|</span>', " ", item[1])
            # item[0]是用户名称，item[1]是内容，item[2]是点赞数，item[3]是评论数
            text = re.sub(r'<br/>', "\n", text)
            pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
        return pageStories

    # 加载并提取页面内容，加入到列表中
    def loadPage(self):
        if self.enable == True:
            # 若当前未看的页数少于2页，则加载新一页
            if len(self.stories) < 2:
                # 获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存入全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印出一个段子
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            inputSen = input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 若输入Q则程序结束
            if inputSen == "Q":
                self.enable = False
                return
            print(u"你查看的是第%d页\t发布人是:%s\t好笑指数:%s\t评论:%s\n%s" % (page, story[0], story[2], story[3], story[1]))

    def start(self):
        print(u"正在读取好玩的糗事百科，请按回车查看新段子，请按Q退出")
        # 使变量为True,程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加1
                nowPage += 1
                # 将全局list中的第一个元素剔除，因为已经取出
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()

