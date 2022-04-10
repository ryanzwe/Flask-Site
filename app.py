from tempfile import tempdir
from flask import Flask,redirect,url_for,request,render_template,session
import requests, os,uuid,json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/',methods=['POST'])
def index_post():
    #Form Valeus
    originalText = request.form['text']
    targLang = request.form['language']

    #Load api requirements from .env file 
    apiKey = os.environ['KEY']
    apiEndpoint = os.environ['ENDPOINT']
    apiLocation = os.environ['LOCATION']

    
    #Api setup
    path = '/translate?api-version=3.0'
    targetLanguageParam = '&to=' + targLang
    constructedUrl = apiEndpoint + path + targetLanguageParam
    print(path)
    print(targetLanguageParam)
    print(constructedUrl)

    #Setup Headers
    requestHeaders = {
        'Ocp-Apim-Subscription-Key': apiKey,
        'Ocp-Apim-Subscription-Region': apiLocation,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    #Text to translate
    body = [{ 'text': originalText }]


    #Call the API
    reqs = requests.post(constructedUrl,headers=requestHeaders,json=body)
    response = reqs.json()
    translatedText = response[0]['translations'][0]['text']

    # #debug
    print(f'Text: {originalText}')
    print(f'Target Language: {targLang}')
    return render_template(
        'results.html',
        translatedText = translatedText,
        originalText=originalText,
        targLang=targLang
    )