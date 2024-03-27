from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'

db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))

class UploadForm(FlaskForm):
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        # Создайте папку, если она не существует
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # Сохраните изображение в папку
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_image = Image(filename=filename)
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('gallery'))
    return render_template('upload_image.html', form=form)

@app.route('/gallery')
def gallery():
    images = Image.query.all()
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
