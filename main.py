from sqlalchemy import text
from flask import Flask, render_template, request, flash

from models.permit import Permit
from app import create_app, db
from utils import valid_coordinates, get_five_closest

app = create_app()

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        # default state is all approved permits
        permits = Permit.query.filter(Permit.status=="APPROVED").all()
        return render_template('index.html', permits=permits)

    if request.method == 'POST':
        applicant = request.form.get('applicant', type=str)
        address = request.form.get('address', type=str)
        lat = request.form.get('lat', type=float)
        lon = request.form.get('lon', type=float)
        approvedOnly = (request.form.get('approved') is not None)

        # require user submitted only one type of search criteria
        if sum(map(bool, [applicant,address,(lat or lon)])) > 1:
            flash('Please search by applicant, address, OR coodinates')
            return render_template('index.html', permits=[])

        # if searching by coordinates, we need both
        if ((lat and not lon) or (lon and not lat)):
            flash('Please enter both latitude and longitude')
            return render_template('index.html', permits=[])

        # create base of the query
        query = Permit.query

        if approvedOnly: query = query.filter(Permit.status=='APPROVED')

        # handle special 5 nearest case separately
        if (lat and lon):
            if (not valid_coordinates(lat, lon)):
                flash('Please enter valid coordinates')
                return render_template('index.html', permits=[])

            permits = query.all()
            closest_trucks = get_five_closest(permits, lat, lon)

            return render_template('index.html', permits=closest_trucks)

        if applicant: query = query.filter(Permit.applicant.like(f'%{applicant}%'))
        elif address: query = query.filter(Permit.address.like(f'%{address}%'))

        permits = query.all()
        
        return render_template('index.html', permits=permits)
