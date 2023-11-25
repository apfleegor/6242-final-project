from flask import Flask, render_template

# create instance of Flask
app = Flask(__name__)

# create root route
@app.route("/")
def home():
    # note: can send data to index.html through this function
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)