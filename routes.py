from flask import Blueprint, render_template
from datetime import datetime
# 假設你的資料庫 Model 名稱為 TrafficRecord 與 MenuItem
# from app.models import TrafficRecord, MenuItem 

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # 1. 從流量紀錄中讀取最新人數與時間戳記
    latest_record = TrafficRecord.query.order_by(TrafficRecord.timestamp.desc()).first()
    
    if not latest_record:
        current_count = 0
        record_time = datetime.now()
    else:
        current_count = latest_record.count
        record_time = latest_record.timestamp

    # 【數理亮點】撈取前一筆資料，計算即時人流變化率（呼應微積分導數概念）
    previous_record = TrafficRecord.query.order_by(TrafficRecord.timestamp.desc()).offset(1).first()
    traffic_slope = 0.0  # 預設變化率為 0
    
    if previous_record and latest_record:
        time_diff = (latest_record.timestamp - previous_record.timestamp).total_seconds()
        if time_diff > 0:
            # 計算每分鐘的人數變化量 (ΔCount / Δt)
            traffic_slope = (latest_record.count - previous_record.count) / (time_diff / 60.0)

    # 2. 多維度資料分析（綜合「當前時段」與「人流密度/變化率」）
    current_hour = record_time.hour
    
    # 智慧客群情境判定
    if 6 <= current_hour < 9:
        # 情境 C：清晨時段，判定為偏好特定時段活動的「山型人」
        persona = "山型人"
        persona_desc = "早起山型客群（清晨活力補給，推薦能量輕食）"
        
    elif (8 <= current_hour < 10 or 12 <= current_hour < 14 or 17 <= current_hour < 19) or current_count > 5 or traffic_slope > 0.5:
        # 情境 B：處於通勤/午間尖峰時段，或店內人數擁擠，或人流正快速湧入 (斜率為正) -> 「上班族」
        persona = "上班族"
        persona_desc = "通勤與午間尖峰客群（高流量、快速提神外帶需求）"
        
    else:
        # 情境 A：其餘離峰時段，且店內人數較少、空間安靜 -> 「文青」
        persona = "文青"
        persona_desc = "離峰文青客群（低流量、空間安靜適合慢飲久坐）"

    # 3. 依情境標籤從雲端資料庫動態篩選項目
    recommended_items = MenuItem.query.filter_by(tag=persona).all()

    # 將分析結果與即時數據傳遞給前端 HTML 渲染
    return render_template(
        'index.html',
        current_count=current_count,
        persona=persona,
        persona_desc=persona_desc,
        traffic_slope=round(traffic_slope, 2),
        recommended_items=recommended_items,
        record_time=record_time.strftime('%Y-%m-%d %H:%M:%S')
    )