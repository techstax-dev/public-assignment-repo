from app import create_app
from flask import request

app = create_app()

@app.route('/')
def log():
    return "All OK!"

@app.route('/github', methods=['POST','GET'])
def gh_api():
    if(request.method == 'POST'):
        if(request.headers["Content-Type"]) == "application/json":
            info = json.dumps(request.json)
            print("data : \n :: "+info)
            return info
    else:
        return "GET method"


if __name__ == '__main__': 
    app.run(host="localhost",port=3000,debug=False)
