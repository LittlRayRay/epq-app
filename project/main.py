from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import render_template
from flask import redirect
from flask import url_for
from flask import Flask 
from flask import Blueprint
from flask import request
import os
import time
import sqlite3


main = Blueprint('main', __name__)

@main.route("/dashboard")
def dashboard():

    return render_template('dashboard.html')

@main.route("/remove/<id>")
def remove(id):
    
    con = sqlite3.connect("repairs.db")
    cur = con.cursor()

    cur.execute(f"DELETE FROM repairs WHERE primary_key = {id}") 
    con.commit()
    con.close()
    return redirect(url_for('main.homepage'))


@main.route("/")
def homepage():
    con = sqlite3.connect("repairs.db")
    cur = con.cursor()
    try:
        res=cur.execute("SELECT primary_key, name FROM repairs;")
        output = res.fetchall()
    except:
        print("table does not exist")
        return "internal server error"
    ouptut = [list([x[0], x[1]]) for x in output]
    print(f"names of all projects: {output}")
    con.close()
    return render_template('homepage.html',projects=output)

@main.route("/make-new-repair")
def new_repair():
    return render_template('new_repair.html')

@main.route("/add-new-repair", methods=['POST'])
def add_new_repair():
    name = request.form.get('name', "New Guide").strip()
    url = request.form.get('url').strip().lower()
    con = sqlite3.connect("repairs.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS repairs(primary_key INTEGER PRIMARY KEY AUTOINCREMENT, name, url)")
    cur.execute(f"INSERT INTO repairs (name, url) VALUES(?, ?);", (name, url))

    con.commit()
    con.close()

    return redirect(url_for('main.homepage'))

@main.route("/repair/<id>")
def repair(id):
    
    return render_template('repair.html', id=id)


@main.route("/intermed/<num>")
def intermed(num):

    con = sqlite3.connect("repairs.db")
    cur = con.cursor()
    res=cur.execute(f"SELECT url FROM repairs WHERE primary_key = {id};")
    output=res.fetchall()
    driver = webdriver.Chrome()
    print(res)
    driver.get(str(res))
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

    return redirect("/steps/0") 

@main.route("/steps/<number>")
def steps(number):
    text_print = ""
    print(number)
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
