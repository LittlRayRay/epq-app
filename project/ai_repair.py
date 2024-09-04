from flask import render_template, flash, request, redirect, send_from_directory, url_for
from flask import Blueprint
import os
from openai import OpenAI
from constants import API_KEY

ai_repair = Blueprint("ai_repair", __name__)


UPLOAD_FOLDER = '/uploads'

@ai_repair.route("/ai-repair")
def ai_repair_main():

    return render_template("ai_repair.html")

@ai_repair.route("/ai-repair/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        print(request.files.keys())
        print("GOT HERE")
        if 'file' not in request.files:
            print("failed! :(")
            flash("No file selected")
            return redirect("/ai-repair")
        file = request.files['file']

        if file.filename=='':
            flash("Unnamed file")
            return redirect("/ai-repair")
        file.save(os.path.join('uploads', file.filename))
        print("got here")
        return redirect(f"/ai-repair/response/{file.filename}")
    else:
        return redirect("/ai-repair")


@ai_repair.route("/ai-repair/response/<filename>")
def ai_repair_response(filename):

    client = OpenAI(api_key=API_KEY)

    code=""
    with open(os.path.join('uploads', filename)) as f:
        code = f.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert code debugger. Only return the corrected code without any explanation."},
            {
                "role": "user",
                "content": f"Correct the following code:\n{code}\nPlease return only the corrected code"
            }
        ]
    )

    with open(os.path.join('uploads', filename), "w") as f:
        f.write(str(response.choices[0].message))
    
    return redirect(f"/ai-repair/download/{filename}")
    

@ai_repair.route("/ai-repair/download/<filename>")
def ai_repair_download(filename):

    return send_from_directory(
        'uploads', filename
    )