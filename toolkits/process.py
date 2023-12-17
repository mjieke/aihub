import os
import re
import json
import time
import logging
import requests
from PIL import Image
from tqdm import tqdm
from bs4 import BeautifulSoup
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urljoin


logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(name="")
logger.setLevel(logging.INFO)


def read_url_info(url_file):
    with open(url_file) as f:
        urls = json.load(f)
    return urls


def save_url_info(info_dict, url_file):
    with open(url_file, "w") as f:
        json.dump(info_dict, f, indent=4, ensure_ascii=False)


def get_aibot_url(html_file, dst_url_file):
    """读取aibot.html文件，提取html的url链接，并保存"""
    with open(html_file) as f:
        lines = f.readlines()

    urls = {}
    for line in lines:
        if "data-url" in line:
            splited = line.strip().split('="')
            if len(splited) > 1 and len(splited[1]) > 2:
                addr = splited[1][:-1]
                urls[addr] = {}

    save_url_info(urls, dst_url_file)


def url_to_img_name(url):
    url = url.strip().replace("https://", "").replace("http://", "").replace(".", "_")
    splited = url.split("/")
    if "github" in url:
        splited = splited[:2]
        img_name = "_".join(splited)
    else:
        img_name = splited[0]
    return img_name


def get_list_screenshot(url_file, save_dir, dst_file):
    """读取url链接，并截取url首页，保存图片到save_dir"""
    if not os.path.exists(mainpage_path):
        os.makedirs(mainpage_path)

    logger.info("get url screenshot")
    urls = read_url_info(url_file)
    old_urls = read_url_info(dst_file)
    new_urls = {}
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    driver = webdriver.Chrome(options=chrome_options)
    # 设置窗口大小为 1024 x 768
    driver.set_window_size(1280, 900)  # smaller
    for url, info in tqdm(urls.items()):
        if info.get("delete", False):
            continue

        new_url = {}

        # 检测到同名图片已存在，就更新到字典内
        img_name = url_to_img_name(url) + ".jpg"
        screenshot_path = os.path.join(save_dir, img_name)
        if os.path.exists(screenshot_path):
            new_url.update({"mainpage_org_img": screenshot_path})

        # 老版本存在图像，则继承到新版本
        if url in old_urls and "mainpage_org_img" in old_urls[url]:
            new_url.update(old_urls[url])

        # 指定图像，则覆盖老版本
        new_url.update(info)
        new_urls[url] = new_url
        if "mainpage_org_img" in new_url:
            continue

        # 打开网站首页
        try:
            driver.get(url)
        except Exception as e:
            print(f"exception {e}")
            continue

        # 等待页面加载完成，你可以根据实际情况调整等待时间
        # driver.implicitly_wait(25)
        # 再显示的等待时间
        time.sleep(5)
        driver.save_screenshot(screenshot_path)
        new_url["mainpage_org_img"] = screenshot_path
        logger.info(f"get screenshot for {url} save to {screenshot_path}")
        new_urls[url] = new_url

    save_url_info(new_urls, dst_file)
    # 关闭浏览器
    driver.quit()
    logger.info(f"screenshot done\n\n")


def get_chrome_title(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    title = driver.title

    return title


def download_favicon(favicon_url, local_path):
    if favicon_url:
        try:
            # 下载图标文件
            response = requests.get(favicon_url)
            response.raise_for_status()

            # 保存到本地
            with open(local_path, "wb") as f:
                f.write(response.content)

            print(f"Favicon saved to {local_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading favicon: {e}")
    else:
        print("Favicon not found")


def get_url_icon(url_file, icon_path, icon_file):
    if not os.path.exists(icon_path):
        os.mkdir(icon_path)

    urls = read_url_info(url_file)
    for url, info in tqdm(urls.items()):
        if "favicon_url" in info:
            icon_url = info["favicon_url"]
            icon_tail = icon_url.split(".")[-1]
            icon_tail = icon_tail.split("?")[0]
            if icon_tail not in ["png", "ico", "jpg", "jpeg", "gif", "svg"]:
                print("icon_tail", icon_tail, icon_url)
                icon_tail = "png"
            icon_name = url_to_img_name(url) + "." + icon_tail
            icon_save = os.path.join(icon_path, icon_name)
            info["icon_path"] = icon_save
            continue  # 不下载图标
            if os.path.exists(icon_save):
                continue
            download_favicon(icon_url, icon_save)
    save_url_info(urls, icon_file)


def get_url_info(url):
    # 使用 requests 获取 URL 的内容
    response = requests.get(url)

    # 使用 BeautifulSoup 解析 HTML 内容，需要使用content，不然会乱码
    soup = BeautifulSoup(response.content, "html.parser")

    body_text = {}
    # 获取标题
    title = soup.title.string

    if "403" in title or "Just a" in title:
        title, content = get_chrome_title(url)
    body_text.update({"title": title, "url": url})

    # 查找包含图标信息的 link 标签
    favicon_tag = soup.find("link", rel="icon") or soup.find(
        "link", rel="shortcut icon"
    )

    if favicon_tag:
        logger.info(f"{favicon_tag}")
        # 构建完整的图标 URL
        favicon_url = urljoin(url, favicon_tag["href"])
        body_text.update({"favicon_url": favicon_url})

    # 获取正文
    body = soup.find_all("meta")

    for p in body:
        name = p.get("name") or p.get("itemprop") or ""
        content = p.get("content", "")
        if len(content) > 6:
            body_text[name] = content
    # 返回内容信息
    return body_text


def get_url_description(url_file, url_info_file):
    logger.info("get url description")
    urls = read_url_info(url_file)
    old_urls = read_url_info(url_info_file)
    new_urls = defaultdict(dict)
    for url, info in tqdm(urls.items()):
        if info.get("delete", False):
            continue

        if url in old_urls:
            new_urls[url].update(old_urls[url])

        new_urls[url].update(info)
        if (
            "description" in new_urls[url]
            and "title" in new_urls[url]
            # and "favicon_url" in new_urls[url]
        ):
            continue

        try:
            desc = get_url_info(url)
        except Exception as e:
            print(url, e)
            desc = {"error": "null"}

        new_urls[url].update(desc)
        logger.info(f"get info for {url}")

    save_url_info(new_urls, url_info_file)
    logger.info(f"description done\n\n")


def add_category(info):
    from category import categories

    if info.get("category"):
        return

    info["category"] = "other"
    for name, cate in categories.items():
        for keyword in cate.keywords:
            x = info.get("title", "")
            if not isinstance(x, str):
                logger.info(f"title is none {info}")

            if (
                keyword in info.get("keywords", "")
                or keyword in info.get("description", "").lower()
                or keyword in info.get("url", "")
                or keyword in info.get("title", "").lower()
            ):
                info["category"] = name


def add_picture(url_info, card_img_path):
    screenshot_path = url_info.get("mainpage_org_img")
    if screenshot_path:
        # nail_path = "_nail.".join(screenshot_path.split("."))
        img_name = os.path.basename(screenshot_path)
        nail_path = os.path.join(card_img_path, img_name.split(".")[0] + ".png")
        url_info["mainpage_nail_img"] = nail_path[3:]
        if os.path.exists(nail_path):
            return

        img = Image.open(screenshot_path)
        w, h = img.size
        img = img.resize((240, int(240.0 / w * h)))  # TODO 改为双线性插值
        img.save(nail_path)


def add_info_to_json(url_info_file, dst_info_file, resource_img_path):
    urls = read_url_info(url_info_file)
    if not os.path.exists(resource_img_path):
        os.makedirs(resource_img_path)

    for url, info in tqdm(urls.items()):
        add_category(info)
        add_picture(info, resource_img_path)
    save_url_info(urls, dst_info_file)


if __name__ == "__main__":
    aibot_html_file = "mainpage/aibot.html"
    mainpage_path = "aibot/image/v3"
    icon_path = "aibot/image/icon"
    resource_img_path = "../asserts/img"
    aibot_url_file = "aibot/aibot_1_url.json"
    aibot_url_img_file = "aibot/aibot_2_img.json"
    aibot_url_desc_file = "aibot/aibot_3_description.json"
    aibot_url_icon_file = "aibot/aibot_4_icon.json"
    aibot_url_info_file = "aibot/aibot_5_processed.json"

    # 获取aibot工具列表
    # get_aibot_url(aibot_html_file, aibot_url_file)
    # 截取url首页
    get_list_screenshot(aibot_url_file, mainpage_path, aibot_url_img_file)
    # 爬取url上keyword和description字段
    get_url_description(aibot_url_img_file, aibot_url_desc_file)
    # 爬取图标
    get_url_icon(aibot_url_desc_file, icon_path, aibot_url_icon_file)
    # 补全json文件，并添加分类信息
    add_info_to_json(
        aibot_url_icon_file,
        aibot_url_info_file,
        resource_img_path,
    )
