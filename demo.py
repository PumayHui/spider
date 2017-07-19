import http.cookiejar
import urllib.request
import urllib.parse

def post(url, data):
    req = urllib.request.Request(url)
    data = urllib.parse.urlencode(data).encode(encoding='utf-8')

    filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(filename)

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    # response = opener.open(req, data)
    cookie.save(ignore_discard=True, ignore_expires=True)
    # return response.read()


def main():
    postUrl = "https://www.zhihu.com/#signin"
    data = {'username': '13572067484@163.com', 'password': '645228322'}
    print(post(postUrl, data))


if __name__ == '__main__':
    main()