from selenium import webdriver
from selenium.webdriver.common.by import By

from flask import render_template

from flask import Flask 

import os

app = Flask(__name__)



@app.route("/")
def main():
    driver = webdriver.Chrome()

    driver.get("https://www.ifixit.com/Guide/iPhone+15+Pro+Battery+Replacement/166394")

    elements = driver.find_elements(By.CLASS_NAME, "step") 

    return_string = ""

    steps_texts=[]

    for step in elements:
        steps_texts.append(step.text.replace('\n', ' '))

    if os.path.exists("temp.txt"):
        os.remove("temp.txt")

    steps_texts=list(dict.fromkeys(steps_texts))

    with open("temp.txt", "w") as text_file:
        text_file.write(return_string)
    
    return render_template('index.html')


@app.route("/steps/<number>")
def steps(number):
    text_print = ""
    number = int(number)
    file = open("temp.txt")
    for n, text in enumerate(file):
        if n == number:
            text_print = text
            break
    return render_template('step.html', text=text_print, number=number)
