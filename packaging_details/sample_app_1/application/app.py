
from flask import Flask, render_template, request, jsonify
print('Application 1')
print("--------------------------------------------------")
print()
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
PORT = 8100

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/display', methods=['GET'])
def display():
    return render_template('simple.html')


if __name__ == '__main__':
    app.run(port=6000, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
