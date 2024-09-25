from flask import Flask, render_template
# clone github directory with "git clone https://github.com/KolozsiZsombor/SzoftverModszerMiniProject"
# cmd : "pip install flask"
# go into directory with cd /SzoftverModszerMiniProject
# run python script with python app.py
# visit http://127.0.0.1:5000
# stop server with ctrl + c
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)