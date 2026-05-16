from flask import Flask
import pg8000

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # 設定你的 Render 資料庫連線資訊
    app.config['DB_CONFIG'] = {
        "user": "cafe_db_8q60_user",
        "password": "LFPPajtpnxQEttpiqeclp7CI70zGXk6H",
        "host": "dpg-d842s5p9rddc7399ntl0-a.singapore-postgres.render.com",
        "database": "cafe_db_8q60",
        "port": 5432
    }

    # 註冊網頁路由
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # 測試連線並建立資料表
    try:
        config = app.config['DB_CONFIG']
        conn = pg8000.connect(**config)
        cursor = conn.cursor()
        
        # 建立菜單資料表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price INTEGER NOT NULL,
                tag VARCHAR(50)
            )
        ''')
        
        # 建立人流紀錄資料表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traffic_records (
                id SERIAL PRIMARY KEY,
                people_count INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("⚡ [成功] 已成功連線至 Render PostgreSQL，資料表準備就緒！")
    except Exception as e:
        print(f"❌ [失敗] 資料庫連線失敗，錯誤訊息: {e}")

    return app