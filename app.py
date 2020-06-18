from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

#메인 html
@app.route('/')
def mainpage():
    return render_template('index.htm')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
             #해당 위치에 경로 수정 필요
      if f.filename.endswith('.txt'):
         f.save("upload/" + secure_filename(f.filename))
         
      return render_template('index.htm')
		
if __name__ == '__main__':
   app.run(debug = True)