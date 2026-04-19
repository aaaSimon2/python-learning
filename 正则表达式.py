
import requests
import re
from urllib.parse import urljoin
BASE_URL = "http://books.toscrape.com"
START_PAGE = 1
END_PAGE = 2
for page in range(START_PAGE, END_PAGE + 1):
    page_url = f"{BASE_URL}/catalogue/page-{page}.html"
    print(f"\n===== 正在爬第 {page} 页：{page_url} =====")
    page_data = requests.get(page_url)
    page_data.encoding = "utf-8"
    html = page_data.text
    books = re.findall(r'<a href="(.*?)"><img.*?alt="(.*?)"', html)
    print(f"第 {page} 页找到 {len(books)} 本书")
    for i, (link, name) in enumerate(books, 1):
        detail_url = urljoin(page_url, link)
        print(f"\n----- 第 {i} 本：《{name}》-----")
        print(f"详情页地址：{detail_url}")
        detail_data = requests.get(detail_url)
        detail_data.encoding = "utf-8"
        detail_html = detail_data.text
        desc_list = re.findall(
            r'Product Description.*<p>(.*?)</p>',
            detail_html,
            re.DOTALL
        )
        if desc_list:
            print(f"描述：{desc_list[0].strip()}")
        else:
            print("描述：未找到")