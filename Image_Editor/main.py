from flask import Flask , render_template , request, flash
from werkzeug.utils import secure_filename
import os
import cv2
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}

app=Flask(__name__)
app.secret_key = "Shivam_Bansal" 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def processImage(filename,operation):
    print(f"The operation is {operation} and file is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f"static/{filename}",imgProcessed)
        case "cwebp":
            cv2.imwrite(f"static/{filename.split('.')[0]}.webp",imgProcessed)
        case "cpng":
            cv2.write(f"static/{filename.split('.')[0]}.webp",imgProcessed)
        case "cjpg":
            cv2.write(f"static/{filename.split('.')[0]}.webp",imgProcessed)
@app.route("/")
def home():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/edit", methods=["GET","POST"])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "No file is selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(filename,operation)
            flash(f"Your image has been processed and is available <a href='static/{filename} >here</a>")
            return render_template("index.html")
    return render_template("index.html")

app.run(debug=True)
