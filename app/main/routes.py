from datetime import datetime
import os
import csv
from turtle import title
from flask_sqlalchemy import Pagination
import pandas as pd
from os.path import join, dirname, realpath
from werkzeug.urls import url_parse
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc, asc
from app import db
from app.main import bp
from app.main.forms import NewMovieForm
from app.models import User, Movies

# This function will be used to update tables with movies from csv
def parseCSV(filePath):
    # CVS Column Names
    # col_names = ['show_id','type','title', 'director', 'cast' , 'country', 'date_added', 'release_year', 
    #                 'rating', 'duration', 'listed_in', 'description']
    
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, sep='\t', header=0)
    # Loop through the Rows
    for i,row in csvData.iterrows():
            
        show_id = row[0]
        type = row[1]
        title = row[2]
        director = row[3]
        cast = row[4]
        country = row[5]
        date_added = pd.to_datetime(row[6])
        release_year = pd.to_datetime(row[7], format='%Y')
        rating = row[8]
        duration = row[9]
        listed_in = row[10]
        description = row[11]
        m = Movies(show_id=show_id,type=type,title=title, director=director, cast=cast, country=country,
        date_added=date_added,  rating=rating, duration=duration,
        listed_in=listed_in, description=description, release_year=release_year, id=i+1)
        try:
            db.session.add(m)
            db.session.commit()
            print(f"new movies added {title}")
        except:
            db.session.rollback()
            flash("Failed to upload movies")

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if request.form['submit_button'] == 'add_csv':
            # get the uploaded file
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
                flash("new csv uploaded")
                parseCSV(file_path)
                return redirect(url_for('main.index'))
    if request.method == 'GET':
        movies = Movies.query.all()
        return render_template('index.html', title='Home', movies=movies)        

@bp.route('/new_movie', methods=['GET', 'POST'])
def new_movie():
    if current_user.is_authenticated:     
        form = NewMovieForm()
        last_movie = Movies.query.order_by(desc(Movies.id)).first()
        show_id = last_movie.show_id
        show_id = show_id[1:]
        show_id = int(show_id)+1
        show_id = 's' + str(show_id)
        release_year = pd.to_datetime(form.release_year.data)
        
        if form.validate_on_submit(): 
            movie = Movies(show_id=show_id, title=form.title.data, type=form.type.data, date_added=form.date_added,
                            director=form.director.data, cast=form.cast.data, country=form.country.data,
                            release_year=form.release_year.data, rating=form.rating.data, duration=form.duration.data,
                            listed_in=form.listed_in.data, description=form.description.data)
            db.session.add(movie)
            db.session.commit()
            flash("New Movie Submited")
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('login'))
    return render_template('new_movie.html', title='New Movie', form=form)
