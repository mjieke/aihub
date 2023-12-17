import json
from collections import defaultdict
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from category import categories

env = Environment(loader=FileSystemLoader("./template"))
template_base = env.get_template("base.html")
template_index = env.get_template("index.html")
template_about = env.get_template("about.html")
template_search = env.get_template("search.html")
template_categories = env.get_template("categories.html")


aibot_url_info_file = "aibot/aibot_5_processed.json"
WEB_SITE = "http://127.0.0.1:5500"
WEB_SITE = "https://mjieke.github.io/aihub"
WEB_CSS = "asserts/css/header.css"


@dataclass
class ItemCard:
    url: str
    keywords: str
    description: str
    image: str
    title: str


def read_url_info(url_file):
    with open(url_file) as f:
        urls = json.load(f)
    return urls


def create_cards(url_file):
    urls = read_url_info(url_file)
    cards = []  # 无类别
    cates = defaultdict(list)  # 有类别
    for key, info in urls.items():
        if info.get("delete", False):
            continue

        card = ItemCard(
            url=key,
            title=info.get("title"),
            keywords=info.get("keywords"),
            description=info.get("description"),
            image=info.get("mainpage_nail_img"),
        )
        cate = info.get("category")
        cards.append(card)
        cates[cate].append(card)
    cates = dict(sorted(cates.items(), key=lambda x: categories[x[0]].idx))
    cates = [(categories[x].name[0], y) for x, y in cates.items()]

    return cards, cates


cards, cates = create_cards(aibot_url_info_file)


base_content = template_base.render(
    title="Ai·Hub",
    show_menu="latest",
    cards=cards,
    web_site=WEB_SITE,
    base_css=WEB_CSS,
)
index_content = template_index.render(
    title="Ai·Hub",
    show_menu="latest",
    cards=cards,
    web_site=WEB_SITE,
    base_css=WEB_CSS,
)
about_content = template_about.render(
    title="Ai·Hub",
    show_menu="about",
    web_site=WEB_SITE,
    base_css=WEB_CSS,
)
search_content = template_search.render(
    title="Ai·Hub",
    show_menu="search",
    web_site=WEB_SITE,
    base_css=WEB_CSS,
)
cate_content = template_categories.render(
    title="Ai·Hub",
    show_menu="categories",
    cates=cates,
    web_site=WEB_SITE,
    base_css=WEB_CSS,
)

# with open("../base.html", "w") as f:
#     f.write(base_content)
with open("../index.html", "w") as f:
    f.write(index_content)
with open("../about/index.html", "w") as f:
    f.write(about_content)
with open("../search/index.html", "w") as f:
    f.write(search_content)
with open("../categories/index.html", "w") as f:
    f.write(cate_content)
