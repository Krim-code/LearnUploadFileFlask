from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import base64
print()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imagesBlob.db'

db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)

class UploadForm(FlaskForm):
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        data = image.read()  # Read the binary data of the image
        new_image = Image(data=data)
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('gallery'))
    return render_template('upload_image.html', form=form)

@app.route('/gallery')
def gallery():
    images = Image.query.all()
    encoded_images = []
    for image in images:
        encoded_image = base64.b64encode(image.data).decode('utf-8')
        encoded_images.append(encoded_image)
    return render_template('galleryBlob.html', images=encoded_images)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)