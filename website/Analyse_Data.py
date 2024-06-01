import pandas as pd
import matplotlib.pylab as plt
import numpy as np
from Scrapping import Twitter_scrapping  # Importer votre fonction de scraping
from Prepar_data import clean_data

def Visuel_data(df):
    df2 = df[['Day','Sentiment']]

    # Compter le nombre de chaque sentiment pour chaque année
    sentiment_counts = df2.groupby(['Day', 'Sentiment']).size().unstack(fill_value=0)

    # Assurez-vous que toutes les valeurs de sentiment sont présentes dans le DataFrame
    sentiment_counts = sentiment_counts.reindex(columns=[-1, 0, 1], fill_value=0)

    # Définir les positions des barres
    day = sentiment_counts.index
    n_day = len(day)
    n_bars = len(sentiment_counts.columns)
    bar_width = 0.3
    x = np.arange(n_day)

    # Tracer l'histogramme avec des barres groupées
    fig, ax = plt.subplots(figsize=(12, 8))  # Agrandir la taille du plot à 12x8 pouces
    for i, sentiment in enumerate(sentiment_counts.columns):
        if sentiment < 0 :
            ax.bar(x + i * bar_width, sentiment_counts[sentiment], width=bar_width, color='red' ,label='Sentiment Négatif')
        elif sentiment == 0 :
            ax.bar(x + i * bar_width, sentiment_counts[sentiment], width=bar_width, color='gray' ,label='Sentiment Neutre')
        else :
            ax.bar(x + i * bar_width, sentiment_counts[sentiment], width=bar_width, color='green' ,label='Sentiment Positif')

    # Ajouter des étiquettes et un titre
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of Sentiments')
    ax.set_title('Number of Each Sentiment by Year')
    ax.set_xticks(x + bar_width * (n_bars - 1) / 2)
    ax.set_xticklabels(day)
    ax.legend(title='Sentiment')

    # Afficher le graphique
    plt.savefig('static/images/sentiment_plot.png')



def Multiple_Visuel_data(path_csv):
    df = pd.read_csv(path_csv)

    df2 = df[['Day','Sentiment']]
    
    # Compter le nombre de chaque sentiment pour chaque année
    sentiment_counts = df2.groupby(['Day', 'Sentiment']).size().unstack(fill_value=0)

    # Assurez-vous que toutes les valeurs de sentiment sont présentes dans le DataFrame
    sentiment_counts = sentiment_counts.reindex(columns=[-1, 0, 1], fill_value=0)

    # Définir les positions des barres
    days = sentiment_counts.index
    n_days = len(days)
    n_bars = len(sentiment_counts.columns)
    bar_width = 0.3
    x = np.arange(n_days)

    # Définir des couleurs pour chaque sentiment
    colors = { -1: 'red', 0: 'gray', 1: 'green' }

    # Créer une figure avec plusieurs sous-graphiques
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Créer une grille 2x2 de sous-graphiques

    # Premier plot
    axs[0, 0].bar(x - bar_width, sentiment_counts[-1], width=bar_width*2, color=colors[-1], label='Sentiment -1')
    axs[0, 0].set_title('Sentiment Négatifs')
    axs[0, 0].set_xticks(x)
    axs[0, 0].set_xticklabels(days)
    axs[0,0].set_xlabel('Day')
    axs[0,0].set_ylabel('Number of Sentiments')

    # Deuxième plot
    axs[0, 1].bar(x, sentiment_counts[0], width=bar_width*2, color=colors[0], label='Sentiment 0')
    axs[0, 1].set_title('Sentiment Neutre')
    axs[0, 1].set_xticks(x)
    axs[0, 1].set_xticklabels(days)
    axs[0,1].set_xlabel('Day')
    axs[0,1].set_ylabel('Number of Sentiments')

    # Troisième plot
    axs[1, 0].bar(x + bar_width, sentiment_counts[1], width=bar_width*2, color=colors[1], label='Sentiment 1')
    axs[1, 0].set_title('Sentiment Positif')
    axs[1, 0].set_xticks(x)
    axs[1, 0].set_xticklabels(days)
    axs[1,0].set_xlabel('Day')
    axs[1,0].set_ylabel('Number of Sentiments')

    # Quatrième plot: Histogramme empilé
    for i, sentiment in enumerate(sentiment_counts.columns):
        axs[1, 1].bar(x + i * bar_width, sentiment_counts[sentiment], width=bar_width, color=colors[sentiment], label=f'Sentiment {sentiment}')
    axs[1, 1].set_title('Histogramme Empilé')
    axs[1, 1].set_xticks(x + bar_width)
    axs[1, 1].set_xticklabels(days)
    axs[1, 1].legend(title='Sentiment')
    axs[1,1].set_xlabel('Day')
    axs[1,1].set_ylabel('Number of Sentiments')

    # Ajuster l'espacement entre les sous-graphiques
    plt.tight_layout()

    # Afficher le graphique
    plt.savefig('static/images/sentiment_plot3.png')