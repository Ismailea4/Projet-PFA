from flask import Flask, render_template, request, send_file,jsonify,redirect,url_for
import pandas as pd
from Scrapping import Twitter_scrapping  # Importer votre fonction de scraping
from Prepar_data import clean_data
from Analyse_Data import Visuel_data
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    keyword = request.form['keyword']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    nombre_iter = request.form['nombre_iter']
        
    # Lancer le script de scraping avec les paramètres de l'utilisateur
    df = Twitter_scrapping(nombre_iter,start_date, end_date,keyword)
    
    # Sauvegarder les données dans un fichier CSV
    df.to_csv('data/tweets.csv', index=False)
    df.to_excel('data/tweets.xlsx', index=False)

    
    # Générer le graphique
    #Visuel_data(df1)
    #return render_template('result.html')
    
    return redirect(url_for('result'))

@app.route('/result')
def result():
    df = pd.read_csv('data/tweets.csv')
    tweets = df.to_dict(orient='records')
    return render_template('result.html', tweets=tweets)

@app.route('/analyze')
def analyze():
    df = pd.read_csv('data/tweets.csv')
    df1 = clean_data(df)
    
    # Générer le graphique
    Visuel_data(df1)
    
    return render_template('analyse.html')


@app.route('/downloadcsv')
def downloadcsv():
    return send_file('data/tweets.csv', as_attachment=True)

@app.route('/downloadxl')
def downloadxl():
    return send_file('data/tweets.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
