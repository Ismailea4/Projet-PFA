'''Biblio'''

#Webdriver de Selenium qui permet de contrôler un navigateur
from selenium import webdriver

#Permet d'accéder aux différents élements de la page web
from selenium.webdriver.common.by import By

#Pour attendre qu'une condition soit remplie avant de poursuivre l'exécution du script
from selenium.webdriver.support.ui import WebDriverWait

#fournit des conditions d'attente prédéfinies pour être utilisées avec WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select


#Pour utiliser les fonctionnalités liées à la gestion du temps
import time

import re

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

import pandas as pd

from datetime import datetime

from pprint import pprint 


from bs4 import BeautifulSoup

#=============================================================

'''sous - Fonction '''

def twitter_time(soup1):
    times = soup1.find_all('time')
    dates=[]
    for time in times:
        dates.append(time.get('datetime'))
    return dates

#

def twitter_user(soup1):
    users = soup1.find_all('div',attrs={'data-testid':'User-Name'})

    username=[]
    for div in users:
        divss = div.find('a')
        print(divss['href'])
        username.append(divss.get('href')[1:])
    return username


def twitter_tweets(soup1):
    tweets = soup1.find_all('div',attrs={'data-testid':"tweetText"})

    texts=[]
    for tweet in tweets:
        texts.append(tweet.text)
    return texts

def twitter_react(soup1):
    likes = soup1.find_all('div',attrs={'role':'group'})

    reacts=[]
    order = ['replies', 'reposts', 'likes', 'bookmarks', 'views']
    
    for like in likes:
        react_text=like['aria-label']

        # Initialize dictionary to store numbers
        react_stat = {word: 0 for word in order}

        # Find all numbers and words using regex
        matches = re.findall(r"(\d+) (\w+)", react_text)

        # Update numbers dictionary with extracted values
        for match in matches:
            number, word = match
            if word in react_stat:
                react_stat[word] = int(number)
        reacts.append([react_stat[word] for word in order])

        
    react_sorted = [[row[i] for row in reacts] for i in range(len(reacts[0]))]
        
    return react_sorted

def exctract_twitter_data(soup1):
    dictio = {}
    dictio['Username']=twitter_user(soup1)
    dictio['Date']=twitter_time(soup1)
    dictio['Text']=twitter_tweets(soup1)
    react=twitter_react(soup1)
    dictio['Replies']=react[0]
    dictio['Reposts']=react[1]
    dictio['Likes']=react[2]
    dictio['Bookmarks']=react[3]
    dictio['Views']=react[4]
    
    data = pd.DataFrame(dictio)
    
    return data

'''Fonction principale :'''

def Twitter_scrapping(nombre_iter,date_depart, date_fin , keyword):
    
    d_d = datetime.strptime(date_depart, "%Y-%m-%d")

    d_f = datetime.strptime(date_fin, "%Y-%m-%d")
    
    url = 'https://twitter.com/explore'
    options = Options()
    options.add_argument("--window-size=1920,1080")
    tweets_df=pd.DataFrame()
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the login input field to be present
    wait = WebDriverWait(driver, 20)
    log = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
    # Input the email
    log.send_keys('mana_isma@hotmail.com')
    log.send_keys(Keys.RETURN)
    
    # Input the pseudo
    pseudo = wait.until(EC.presence_of_element_located((By.XPATH, "//input")))
    pseudo.send_keys('Izumiu10')
    pseudo.send_keys(Keys.RETURN)

    # Input the password
    password=wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    password.send_keys('Izumiii0')
    password.send_keys(Keys.RETURN)


    #Search
    search = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']")))
    search.send_keys(str(keyword))

    search.send_keys(Keys.RETURN)



    search_parameter = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='searchBoxOverflowButton']")))
    search_parameter.click()

    search_advanced = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/search-advanced']")))
    search_advanced.click()


    search = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='allOfTheseWords']")))
    search.send_keys(keyword)


    language = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_1']")))
    select_language = Select(language)
    select_language.select_by_value('en')

    From_year = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_4']")))
    From_day = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_3']")))
    From_month = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_2']")))
    select_fyear = Select(From_year)
    select_fday = Select(From_day)
    select_fmonth = Select(From_month)
    select_fyear.select_by_value(str(d_d.year))
    select_fday.select_by_value(str(d_d.day))
    select_fmonth.select_by_value(str(d_d.month))


    To_year = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_7']")))
    To_day = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_6']")))
    To_month = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='SELECTOR_5']")))
    select_tyear = Select(To_year)
    select_tday = Select(To_day)
    select_tmonth = Select(To_month)
    select_tyear.select_by_value(str(d_f.year))
    select_tday.select_by_value(str(d_f.day))
    select_tmonth.select_by_value(str(d_f.month))


    search = driver.find_element(By.XPATH, "//span[text()='Search']")
    search.click()

    time.sleep(10)
    SCROLL_PAUSE_TIME = 20

    itera = 0

    last_height = driver.execute_script("return document.body.scrollHeight")

    while itera < int(nombre_iter):

        page_content = driver.page_source

        soup = BeautifulSoup(page_content, 'html.parser')

        try:
        # Code susceptible de lever une exception
            df = exctract_twitter_data(soup)
            tweets_df = pd.concat([tweets_df, df], ignore_index=True)
        except TypeError as e:
            # Traitement de l'erreur TypeError
            print("Une erreur s'est produite :", e)
        except KeyError :
            print("Erreur de keyerror")

        itera+=1

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            itera+=2*int(nombre_iter)/10
        last_height = new_height

    driver.quit()

    return tweets_df
