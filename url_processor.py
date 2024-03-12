import pandas as pd
import joblib
from urllib.parse import urlparse
import re
import socket
import requests
from datetime import datetime
import whois

URL1 = 'https://www.coursera.org/'
URL2 = 'https://www.youtube.com/'

def extract_url_features(url):
    features = {}
    
    # Parsing URL
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    path = parsed_url.path
    query = parsed_url.query

    # Basic Features
    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)
    features['nb_dots'] = url.count('.')
    features['nb_qm'] = url.count('?')
    features['nb_eq'] = url.count('=')
    features['nb_slash'] = url.count('/')
    features['nb_www'] = hostname.count('www.')
    digits_ratio = sum(c.isdigit() for c in url) / len(url)
    digits_ratio_host = sum(c.isdigit() for c in hostname) / len(hostname) if hostname else 0
    features['ratio_digits_url'] = digits_ratio
    features['ratio_digits_host'] = digits_ratio_host
    features['tld_in_subdomain'] = 1 if any(part.count('.') > 0 for part in hostname.split('.')) else 0
    features['prefix_suffix'] = 1 if '-' in hostname else 0

    # Advanced Features Requiring More Logic or External Tools
    host_words = re.split('\W+', hostname)
    path_words = re.split('\W+', path)
    features['shortest_word_host'] = len(min(host_words, key=len)) if host_words else 0
    features['longest_words_raw'] = len(max(url.split('/'), key=len))
    features['longest_word_path'] = len(max(path_words, key=len)) if path_words else 0

    # Domain Age, Google Index, Page Rank - Requires external APIs or services
    domain_info = whois.query(hostname)
    features['domain_age'] = (datetime.now() - domain_info.creation_date).days if domain_info.creation_date else -1

    return features

def analyze_url(url):
    result = [extract_url_features(url)]
    df = pd.DataFrame(result)
    loaded_clf = joblib.load('best_model.joblib')
    predictions = loaded_clf.predict(df)

    print(f"Phishing chance: {loaded_clf.predict_proba(df)[0][1]} | Prediction: {predictions[0]}")

    return loaded_clf.predict_proba(df)[0][1], predictions[0]