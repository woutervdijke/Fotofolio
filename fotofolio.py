from flask import Flask, render_template, abort, send_file, request
app = Flask(__name__)

from markdown2 import Markdown
from glob import glob
from os import path, walk
import os

markdowner = Markdown()

def gettext(file):
    with open('content/'+file, 'r') as data:
        html = markdowner.convert(data.read())
    return html

def getimgdesc(folder, filename):
    from PIL import Image
    image = Image.open("content/"+folder+"/"+filename)
    info = image._getexif()
    if 270 in info.keys():
        description = info[270]
        return description
    else:
        return ""

textpaths = glob("content/*.md")

pagetitles = []
for file in textpaths:
    filename = path.basename(file).replace('.md','')
    if filename != "index":
        pagetitles.append(filename)

directories = glob("content/*/")
folders = []


for directory in directories:
    for root, dirs, files in walk(directory):
        foldername = root.replace("content/","").replace("/","")
        folders.append(foldername)



@app.route("/")
def index():
    template = 'textpage.html'
    title="Fotofolio"
    maintext = gettext('index.md')
    menupages = pagetitles + folders
    return render_template(template, title=title, maintext=maintext, pages=menupages)

@app.route("/<page>")
def showpage(page):
    title = "Fotofolio"
    menupages = pagetitles + folders
    if page in pagetitles:
        template = 'textpage.html'
        maintext = gettext(page +'.md')
        return render_template(template, title=title, maintext=maintext, pages=menupages)

    elif page in folders:
        template = 'portfolio.html'
        images = []
        for root, dirs, files in walk('content/'+page):
            for file in files:
                if file not in ['.DS_Store']:
                    img = {}
                    img['filename'] = file
                    img['title'] = file.replace(".jpg","")
                    img['desc'] = getimgdesc(page, file)
                    images.append(img)


        return render_template(template, title=title, pages=menupages, folder = page, images=images)
    else:
        abort(404)


@app.route('/get_image')
def get_image():
    foldername = request.args.get('folder')
    filename = request.args.get('file')
    return send_file("content/"+foldername+"/"+filename, mimetype='image/gif')

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)
