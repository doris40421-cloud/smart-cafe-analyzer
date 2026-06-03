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

🧱 系統技術架構
本專案採用三層式架構設計，確保資料流與運算邏輯分離：

資料擷取與邊緣輸入層： 透過 scrape_menu.py 進行動態網頁資料收集；並由邊緣端裝置（模擬器 test_remote.py）即時定時回傳環境人流數據。

雲端資料儲存層 (Backend Storage)： 部署於 Render 雲端平台之 PostgreSQL 關聯式資料庫，負責維護商品菜單與歷史人流軌跡。

應用程式展示層 (Web Application)： 基於 Flask 框架開發的網頁端，即時從雲端資料庫撈取數據，進行動態情境分析與前端渲染。

---
📁 專案標準目錄架構（範本）
smart-cafe-analyzer/
├── app/                  # Flask 核心應用程式模組
│   ├── __init__.py       # App 初始化、連線 Render DB、動態建表邏輯
│   ├── routes.py         # 網頁路由與動態型人推薦邏輯 (Persona Analytics)
│   └── templates/        # 前端網頁 HTML 模板 (index.html, menu.html)
├── run.py                # 本地/生產環境 Web 伺服器啟動點
├── scrape_menu.py        # 網路爬蟲與資料庫初始化寫入腳本
├── test_remote.py        # 遠端數據上傳測試（模擬邊緣運算裝置輸入）
├── requirements.txt      # 專案相依套件環境清單 (Flask, pg8000, requests 等)
└── README.md             # 專案說明文件（GitHub 門面）
