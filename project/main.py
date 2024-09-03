from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import render_template
from flask import redirect
from flask import url_for
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

@main.route("/make-new-repair/<id>")
def new_repair(id):
 
    con=sqlite3.connect("urls.db")
    cur=con.cursor()
    print("LOOK ID :P", id)
    res=cur.execute(f"SELECT title FROM urls WHERE primary_key = {id}").fetchall()[0][0]

    return render_template('new_repair.html', id=id, res=res)

@main.route("/add-new-repair/<id>", methods=['POST'])
def add_new_repair(id):

    con=sqlite3.connect("urls.db")
    cur=con.cursor()

    url=cur.execute(f"SELECT url FROM urls WHERE primary_key = {id}").fetchall()[0][0]

    con.close()
    name = request.form.get('name', "New Guide").strip()
    print(url)
    con = sqlite3.connect("repairs.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS repairs(primary_key INTEGER PRIMARY KEY AUTOINCREMENT, name, url, cache)")
    cur.execute(f"INSERT INTO repairs(name, url, cache) VALUES(?, ?, ?);", (name, url, 0))
    

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
    res=cur.execute(f"SELECT url FROM repairs WHERE primary_key = {num};")
    output=res.fetchall()
   
    # use cache if it exists else create it
    
    cache_res = cur.execute(f"SELECT cache FROM repairs WHERE primary_key = {num};")
    cache=int(cache_res.fetchall()[0][0])
    

    if (os.path.exists(f"cache/_{num}t.txt")) == False:
        cache = False
    elif (os.path.exists(f"cache/_{num}i.txt")) == False:
        cache = False

    if cache == 1:
        return redirect(f"/{num}/steps/0")

    driver = webdriver.Chrome()
    output=output[0][0] 
    try:
        driver.get(str(output))
    except:
        return "invalid url" 
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

    with open(f"cache/_{num}t.txt", "w", encoding="utf-8") as text_file:
        for i in steps_texts:
            text_file.write(f"{i}\n")

    with open(f"cache/_{num}i.txt", "w", encoding="utf-8") as images_file: 
        for image in image_srcs:
            text_buff = ""
            for src in image:
                img_src = ""
                text_buff+= f"{src.get_attribute('src')} "
            images_file.write(f"{text_buff}\n")
    
    cur.execute(f"UPDATE repairs SET cache = 1 WHERE primary_key = {num};") 
    
    con.commit()
    con.close()
    return redirect(f"/{num}/steps/0") 

@main.route("/<guide>/steps/<number>")
def steps(guide, number):
    
    text_print = ""
    print(number)
    number = int(number)
    file = open(f"cache/_{guide}t.txt")
    for n, text in enumerate(file):
        if n == number:
            text_print = text
            break
    srcs=[]
    images = open(f"cache/_{guide}i.txt")
    for n, image in enumerate(images):
        if n == number:
            srcs=image.split(" ")
            break
    print(srcs)    
    srcs=srcs[:-1]
    srcs=list(dict.fromkeys(srcs))
    return render_template('step.html', text=text_print, number=number, srcs=srcs, guide=guide)

@main.route("/search")
def search():
    q = request.args.get("s")
    if q:
        pass
    else:
        return render_template("search_results.html", results=[]) 
    con = sqlite3.connect("urls.db")
    cur = con.cursor()
    print("LOOK HERE:", q)
    res=cur.execute(f"SELECT primary_key, title FROM urls WHERE title LIKE '%{q}%' LIMIT 50").fetchall()
    print(res)
    return render_template("search_results.html", results=res)
