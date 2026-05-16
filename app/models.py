from app import db
from datetime import datetime

# 表格一：存爬蟲抓到的菜單資料
class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)     # 商品名稱
    price = db.Column(db.Integer, nullable=False)        # 價格
    tag = db.Column(db.String(50))                       # 型人標籤 (例如：適合久坐、外帶首選)

# 表格二：存 Jetson 傳回來的人流紀錄
class TrafficRecord(db.Model):
    __tablename__ = 'traffic_records'
    id = db.Column(db.Integer, primary_key=True)
    people_count = db.Column(db.Integer, nullable=False) # 當時人數
    timestamp = db.Column(db.DateTime, default=datetime.now) # 紀錄時間