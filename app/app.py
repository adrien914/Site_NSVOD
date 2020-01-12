from flask import render_template, Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.getcwd() + '/database.db'

db = SQLAlchemy(app)

class Videos_Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Video link %r>' % self.link

@app.route('/', methods=['GET'])
def index():
    db.create_all()
    videos = Videos_Portfolio.query.all()
    return render_template('index.html', videos=videos)

@app.route('/videos', methods=['GET'])
def videos():
    db.create_all()
    videos = Videos_Portfolio.query.all()
    return render_template('videos.html', videos=videos)
    
@app.route('/videos', methods=['POST'])
def videos_add():
    try:
        db.create_all()
        full_link = request.form["link"]
        link = full_link.split("v=")[1]
        videos = Videos_Portfolio(link=link)
        db.session.add(videos)
        db.session.commit()
        return redirect("/videos")
    except Exception as e:
        return "This entry already exists"

@app.route('/videos/remove', methods=['POST'])
def videos_remove():
    try:
        db.create_all()
        link = request.form['link']
        video = Videos_Portfolio.query.filter_by(link=link).first()
        db.session.delete(video)
        db.session.commit()
        return redirect("/videos")
    except Exception as e:
        return str(e)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
