# Smart Cafe Analyzer 智慧咖啡廳人流偵測與動態推薦系統

一個結合邊緣運算、雲端資料庫與 Web 應用程式的智慧物聯網（IoT）專案。本系統透過 NVIDIA Jetson 邊緣端設備即時偵測咖啡廳內的人流數量，並將數據同步至雲端資料庫；Web 後端則依據即時人流與環境狀態，動態進行「顧客型人分析（Customer Persona Analytics）」，即時調整並推薦最符合當下情境的熱門咖啡餐點。

---

## 🚀 核心功能 (Key Features)

* **邊緣端即時人流偵測與上傳 (Edge-to-Cloud Ingestion):** 利用 NVIDIA Jetson 邊緣運算裝置即時估算店內人數，並透過輕量化資料庫驅動將數據即時寫入雲端。
* **動態型人與情境分析 (Dynamic Persona Analytics):** 後端系統根據雲端最新的人流紀錄進行自動化門檻判定：
  * **人數 ≤ 5人：** 判定為「輕度文青型人」，評估店內安靜舒適，推薦適合久坐慢飲的高享受品項（如：焦糖瑪奇朵、經典熱巧克力）。
  * **人數 > 5人：** 判定為「尖峰上班族型人」，評估店內人潮擁擠，推薦製作快速、方便外帶的提神品項（如：每日精選、美式咖啡、那堤）。
* **自動化餐點數據爬取 (Automated Menu Scraping):** 內建網路爬蟲腳本，可自動化獲取最新連鎖咖啡廳（如星巴克）的熱門餐點、價格，並在寫入資料庫時預先完成「型人標籤 (Tag)」的關聯化分類。
* **即時動態網頁服務 (Real-time Web Dashboard):** 基於 Flask 框架開發的響應式網頁，前端畫面能隨著雲端資料庫的更新，即時變更當前人數、型人狀態描述及動態篩選後的推薦菜單。

---

## 🛠️ 技術棧 (Tech Stack)

* **網頁後端框架 (Web Framework):** Python / Flask 3.1.3
* **資料庫 (Database):** PostgreSQL (託管於 Render 雲端平台)
* **資料庫驅動 (Database Driver):** pg8000
* **硬體/邊緣端技術 (Edge Computing):** NVIDIA Jetson 邊緣運算平台環境整合
* **自動化腳本 (Data Scraper):** Requests / 數據預處理與標籤關聯化
* **生產環境部署 (Deployment):** Gunicorn WSGI 伺服器

---

## 📁 專案架構 (Project Structure)

```text
smart-cafe-analyzer/
├── app/
│   ├── __init__.py      # 初始化 Flask App、配置 Render PostgreSQL 雲端連線並自動建立資料表
│   ├── routes.py        # 核心業務邏輯：撈取最新人流、執行型人判定、動態篩選推薦餐點
│   └── templates/       # 網頁前端模板（index.html, menu.html）
├── run.py               # 本地端開發伺服器啟動進入點
├── scrape_menu.py       # 咖啡廳菜單爬蟲與型人標籤自動化寫入腳本
├── test_remote.py       # NVIDIA Jetson 邊緣端即時人流數據上傳模擬器
└── requirements.txt     # 專案相依套件清單
