from flask import Flask, request, Response

app = Flask(__name__)
    
@app.route('/consumeKey/', methods=['GET'])
@app.route('/drm/consumeKey/', methods=['GET'])
def drmpc():
    response = f"status=0&type={request.args.get('types')}"
    return Response(response, content_type='text/plain')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
