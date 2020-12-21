import app

if __name__ == '__main__':
    data = app.call_search_twitter()
    app.process_response(data)
