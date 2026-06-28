from flask import Blueprint, render_template
from datetime import datetime

main_bp = Blueprint('main', __name__)

# 建立一個相容的類別，防範前端 HTML 使用 item.name 這種物件屬性的寫法
class MockItem:
    def __init__(self, name, price, tag):
        self.name = name
        self.price = price
        self.tag = tag
    # 同時支援字典寫法 item['name']
    def __getitem__(self, item):
        return getattr(self, item)

# 模擬從雲端爬蟲撈下來的完整 PostgreSQL 資料庫清單
ALL_MOCK_MENU = [
    MockItem("每日精選咖啡", 95, "上班族"),
    MockItem("那堤 (Latte)", 135, "上班族"),
    MockItem("美式咖啡 (Americano)", 110, "上班族"),
    MockItem("焦糖瑪奇朵", 155, "文青"),
    MockItem("經典熱巧克力", 140, "文青"),
    MockItem("玫瑰蜜香茶那堤", 145, "文青"),
    MockItem("舒活草本茶", 120, "山型人"),
    MockItem("活力葡萄乾司康", 65, "山型人")
]

@main_bp.route('/')
def index():
    current_count = 12 
    record_time = datetime.now()
    traffic_slope = 2.0  
    current_hour = record_time.hour
    
    if 6 <= current_hour < 9:
        persona = "山型人"
        persona_desc = "早起山型客群（清晨活力補給，推薦能量輕食）"
    elif (8 <= current_hour < 10 or 12 <= current_hour < 14 or 17 <= current_hour < 19) or current_count > 5 or traffic_slope > 0.5:
        persona = "上班族"
        persona_desc = "通勤與午間尖峰客群（高流量、快速提神外帶需求）"
    else:
        persona = "文青"
        persona_desc = "離峰文青客群（低流量、空間安靜適合慢飲久坐）"
    
    recommended_items = [item for item in ALL_MOCK_MENU if item.tag == persona]

    return render_template(
        'index.html',
        people=current_count,       # 對齊 index.html 中的 {{ people }}
        persona=persona,            # 對齊 index.html 中的 {{ persona }}
        desc=persona_desc,          # 對齊 index.html 中的 {{ desc }}
        items=recommended_items     # 對齊 index.html 中的 {{ items }}
    )

@main_bp.route('/menu')
def menu():
    # 【核心修正】精確對齊 menu.html 中的 {% for item in menu_items %}
    return render_template('menu.html', menu_items=ALL_MOCK_MENU)
