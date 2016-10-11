from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def root():
  return render_template('catalogue.html'), 200

@app.route('/favourites')
def favourites():
  return render_template('favourites.html'), 200  

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

