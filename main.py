from flask import Flask, request, render_template_string
import url_processor

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <form action="/analyze" method="post">
        <input type="text" name="url" placeholder="Enter URL to analyze">
        <input type="submit" value="Analyze">
    </form>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    chances, is_scam = url_processor.analyze_url(url)
    result = "Potential Phishing Scam" if is_scam else "Not a Phishing Scam"
    return render_template_string('''
        URL: {{ url }} <br>
        Chances: {{ chances }}% <br>
        Result: {{ result }}
        <br><br>
        <a href="/">Go back</a>
    ''', url=url, chances=chances, result=result)

if __name__ == "__main__":
    app.run(debug=True)
