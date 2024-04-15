from sqlalchemy import text
from flask import Flask, render_template, request, flash

from models.permit import Permit
from app import create_app

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

        # handle special 5 nearest case separately
        if (lat and lon):
            whereClause = 'WHERE status="APPPROVED"' if approvedOnly else ''

            sql = text(f'''
                SELECT locationId, applicant, address, status, latitude, longitude, 
                ((ACOS(SIN(:lat * PI() / 180) * SIN(latitude * PI() / 180) + COS(:lat * PI() / 180) * COS(latitude * PI() / 180) * COS((:lon - longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515) AS distance 
                FROM permits
                {whereClause}
                ORDER BY distance ASC 
                LIMIT 5
                ''')
            
            permits = db.session.execute(sql, {'lat':lat, 'lon':lon})
            return render_template('index.html', permits=permits)

        # filter by status and either applicant name or address
        query = Permit.query

        if approvedOnly: query = query.filter(Permit.status=='APPROVED')
        
        if applicant: query = query.filter(Permit.applicant.like(f'%{applicant}%'))
        elif address: query = query.filter(Permit.address.like(f'%{address}%'))

        permits = query.all()
        
        return render_template('index.html', permits=permits)
