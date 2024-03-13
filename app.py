from flask import Flask, request, render_template
import url_processor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    chances, is_scam = url_processor.analyze_url(url)
    result = "Potential Phishing Scam" if is_scam else "Not a Phishing Scam"
    return render_template('analyze.html', url=url, chances=chances, result=result)

if __name__ == "__main__":
    app.run(debug=True, port=10000)
