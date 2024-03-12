from flask import Flask, request, render_template_string
import url_processor

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: auto; }
        .website-list { margin-top: 20px; }
        .website-list h2 { color: #333; }
        .non-phishing, .phishing { background-color: #ecffdc; padding: 10px; border-radius: 5px; }
        .phishing { background-color: #ffebeb; }
        .website { margin: 5px 0; }
        a { color: #067df7; text-decoration: none; }
        a:hover { text-decoration: underline; }
        form { margin-top: 20px; }
        input[type=text] { width: 70%; padding: 10px; margin-right: 10px; border: 1px solid #ccc; border-radius: 5px; }
        input[type=submit] { padding: 10px 20px; background-color: #067df7; color: white; border: none; border-radius: 5px; cursor: pointer; }
        input[type=submit]:hover { background-color: #0056b3; }
    </style>
    <div class="container">
        <form action="/analyze" method="post">
            <input type="text" name="url" placeholder="Enter URL to analyze">
            <input type="submit" value="Analyze">
        </form>
        <div class="website-list non-phishing">
            <h2>Non-Phishing Websites Examples</h2>
            <div class="website"><a href="https://www.coursera.org/" target="_blank">https://github.com/rodmarkun/</a></div>
            <div class="website"><a href="https://www.youtube.com/" target="_blank">https://www.youtube.com/</a></div>
            <div class="website"><a href="https://calendar.google.com/calendar/u/0/r/week" target="_blank">https://calendar.google.com/calendar/u/0/r/week</a></div>
            <div class="website"><a href="https://data.mendeley.com/datasets/c2gw7fy2j4/3" target="_blank">https://data.mendeley.com/datasets/c2gw7fy2j4/3</a></div>
        </div>
        <div class="website-list phishing">
            <h2>Phishing Websites Examples (Do not visit these)</h2>
            <div class="website">https://nozed-uname.firebaseapp.com/</div>
            <div class="website">http://beta.kenaidanceta.com/postamok/d39a2/source</div>
            <div class="website">http://vkaktivations23.bos.ru</div>
            <div class="website">http://https.www.paypal.com.ttlart2012ttcysu.aylandirow.tmf.org.ru/signin/client-log</div>
            <div class="website">https://marketing.contentmessage.com/email/unsubscribe/5d4aef51ae3dc355752153</div>
        </div>
    </div>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    chances, is_scam = url_processor.analyze_url(url)
    result = "Potential Phishing Scam" if is_scam else "Not a Phishing Scam"
    return render_template_string('''
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            a { color: #067df7; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
        URL: {{ url }} <br>
        Chances: {{ chances }}% <br>
        Result: {{ result }}
        <br><br>
        <a href="/">Go back</a>
    ''', url=url, chances=chances, result=result)

if __name__ == "__main__":
    app.run(debug=True)
