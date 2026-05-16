from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True 代表改程式碼網頁會自動重啟，方便開發
    app.run(debug=True, port=000)