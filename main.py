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
    image_srcs=[]

    for step in elements:
        steps_texts.append(step.text.replace('\n', ' '))
        images = step.find_elements(By.TAG_NAME, 'img')
        temp_srcs=[]
        for image in images:
            temp_srcs.append(image.get_attribute('src'))
        image_srcs.append(temp_srcs)
    print(image_srcs)

    if os.path.exists("temp.txt"):
        os.remove("temp.txt")
    if os.path.exists("images.txt"):
        os.remove("images.txt")
    steps_texts=list(dict.fromkeys(steps_texts))

    with open("images.txt", "w", encoding="utf-8") as images:
        for step in image_srcs:
            write_buff = ""
            for src in step:
                write_buff += f"{src} "
            images.write(f"{write_buff}\n")


    with open("temp.txt", "w", encoding="utf-8") as text_file:
        for i in steps_texts:
            text_file.write(f"{i}\n")
    

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
