from flask import Flask, render_template
import os 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

@app.route('/')
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'starrynight.png')
    return render_template("index.html", user_image = full_filename)

if __name__ == '__main__':
    app.run(debug = True, port=8000)