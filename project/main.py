from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import render_template

from flask import Flask 
from flask import Blueprint
import os
import time


main = Blueprint('main', __name__)

@main.route("/dashboard")
def dashboard():

    return render_template('dashboard.html')


@main.route("/")
def homepage():
    return render_template('homepage.html')

@main.route("/repair")
def repair():
    driver = webdriver.Chrome()

    driver.get("https://www.ifixit.com/Guide/iPhone+12+Screen+Replacement/140572")
    
    height = driver.execute_script("return document.body.scrollHeight")
    
    # scrolls down the webpage to load images
    curr_height = 0
    while curr_height < (height):
        curr_height += 40
        driver.execute_script(f"window.scrollTo(0, {curr_height});")

    elements = driver.find_elements(By.CLASS_NAME, "step") 

    return_string = ""
    
    steps_texts=[]
    image_srcs=[]

    for step in elements:
        steps_texts.append(step.text.replace('\n', ' '))

    if os.path.exists("temp.txt"):
        os.remove("temp.txt")
    if os.path.exists("images.txt"):
        os.remove("images.txt")
    
    steps_texts=list(dict.fromkeys(steps_texts))
    
    images = driver.find_elements(By.TAG_NAME, 'img')
    image_srcs = [[] for i in range(len(steps_texts))]
    print(len(steps_texts))
    for image in images:
        tempid = image.get_attribute("id").lower()
        if tempid[:4] == "step":
            step_no = int(tempid.split("-")[0][4:])
            image_srcs[step_no-1].append(image)
            print(step_no)
        else:
            print(image.get_attribute("id"))
    
    with open("temp.txt", "w", encoding="utf-8") as text_file:
        for i in steps_texts:
            text_file.write(f"{i}\n")
    
    with open("images.txt", "w", encoding="utf-8") as images_file: 
        for image in image_srcs:
            text_buff = ""
            for src in image:
                img_src = ""
                text_buff+= f"{src.get_attribute('src')} "
            images_file.write(f"{text_buff}\n")

    return render_template('index.html')


@main.route("/steps/<number>")
def steps(number):
    text_print = ""
    number = int(number)
    file = open("temp.txt")
    for n, text in enumerate(file):
        if n == number:
            text_print = text
            break
    srcs=[]
    images = open("images.txt")
    for n, image in enumerate(images):
        if n == number:
            srcs=image.split(" ")
            break
    print(srcs)    
    srcs=srcs[:-1]
    srcs=list(dict.fromkeys(srcs))
    return render_template('step.html', text=text_print, number=number, srcs=srcs)