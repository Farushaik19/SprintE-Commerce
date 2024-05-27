from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('homepage.html',test='hello there')

if __name__ == '__main__':
   app.run(port=8000)