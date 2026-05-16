from flask import Blueprint, render_template, current_app
import pg8000

main_bp = Blueprint('main', __name__)

def get_db_cursor():
    config = current_app.config['DB_CONFIG']
    conn = pg8000.connect(**config)
    return conn, conn.cursor()

@main_bp.route('/')
def index():
    # 預設人流（如果資料庫沒紀錄時的備用值）
    current_people = 0 
    
    # 🌟 核心改寫：直接去 Render 資料庫撈最新一筆人流紀錄！
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT people_count FROM traffic_records ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            current_people = result[0] # 拿到最新上傳的人數！
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ 無法讀取即時人流: {e}")

    # 2. 型人分析邏輯 (根據雲端最新人數自動判定)
    if current_people <= 5:
        target_tag = "輕度文青型人"
        persona_desc = "店內目前安靜舒適，適合推薦高享受、適合久坐慢飲的品項。"
    else:
        target_tag = "尖峰上班族型人"
        persona_desc = "店內目前人潮擁擠（Jetson 即時偵測），適合推薦製作快速、方便外帶的提神品項。"

    # 3. 根據型人結果撈商品
    recommended_items = []
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT name, price FROM menu_items WHERE tag = %s", (target_tag,))
        rows = cursor.fetchall()
        for row in rows:
            recommended_items.append({"name": row[0], "price": row[1]})
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"資料庫撈取失敗: {e}")

    return render_template(
        'index.html', 
        people=current_people, 
        persona=target_tag, 
        desc=persona_desc,
        items=recommended_items
    )

@main_bp.route('/menu')
def menu():
    all_items = []
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT name, price, tag FROM menu_items")
        rows = cursor.fetchall()
        for row in rows:
            all_items.append({"name": row[0], "price": row[1], "tag": row[2]})
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"資料庫撈取失敗: {e}")
    return render_template('menu.html', menu_items=all_items)