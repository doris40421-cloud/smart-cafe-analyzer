import pg8000
from datetime import datetime

# 遠端 Render 資料庫連線設定（全組共用這串）
DB_CONFIG = {
    "user": "cafe_db_8q60_user",
    "password": "LFPPajtpnxQEttpiqeclp7CI70zGXk6H",
    "host": "dpg-d842s5p9rddc7399ntl0-a.singapore-postgres.render.com",
    "database": "cafe_db_8q60",
    "port": 5432
}

def simulate_jetson_upload(current_count):
    print(f"📡 [Jetson 模擬器] 正在將偵測到的人流數據 ({current_count} 人) 上傳至雲端...")
    try:
        conn = pg8000.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 塞入一筆人流紀錄
        cursor.execute(
            "INSERT INTO traffic_records (people_count) VALUES (%s)",
            (current_count,)
        )
        conn.commit()
        
        # 順便撈出資料庫目前最新的前 3 筆紀錄，確認有寫入
        cursor.execute("SELECT id, people_count, timestamp FROM traffic_records ORDER BY id DESC LIMIT 3")
        rows = cursor.fetchall()
        
        print("\n📈 [雲端最新人流紀錄回傳]：")
        for row in rows:
            print(f" └─ 紀錄ID: {row[0]} | 人數: {row[1]} 人 | 時間: {row[2]}")
            
        cursor.close()
        conn.close()
        print("\n✅ [成功] 遠端讀寫測試完全正常！")
    except Exception as e:
        print(f"❌ 遠端連線失敗: {e}")

if __name__ == "__main__":
    # 模擬 Jetson 偵測到店內現在有 12 個人（屬於尖峰上班族型人）
    simulate_jetson_upload(12)