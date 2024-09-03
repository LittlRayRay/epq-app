from selenium import webdriver
from selenium.webdriver.common.by import By

import sqlite3

url_l = []

with open("save.txt", "r") as f:
    url_l = f.readlines()
    url_l = [x.strip('\n').split()[0] for x in url_l]

con = sqlite3.connect("urls.db")
cur = con.cursor()

driver = webdriver.Chrome()

for url in url_l:
    try:
        driver.get(url)
        title = driver.find_element(By.TAG_NAME, "h1").text
        cur.execute("INSERT INTO urls (url, title) VALUES (?, ?)", (url, title))
        print(title)
    except:
        pass

con.commit()
con.close()    
