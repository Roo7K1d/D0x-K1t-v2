#!/usr/bin/python

# Get configuration variables from config.py
from config import *

# Imports for Flask and related libraries
from flask import Flask
from flask import render_template, redirect, url_for, flash, request, session
from flask import jsonify, Response
from flask_googlemaps import GoogleMaps, Map
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, IPAddress, InputRequired
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_nav import Nav
from flask_nav.elements import Navbar, View

# Import for dependency-handling
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

# Networking imports
from whois import whois
import pygeoip
from crtsh import crtshAPI

# System standard-library imports
import os
import sys
import getpass
import socket
import requests
import signal
from time import gmtime, strftime, time
from uuid import getnode as get_mac
from datetime import datetime

# Imports for file-formats
import csv
import yaml
import ast
import json

# Start App and load configurations
app = Flask(__name__)
app.config.from_object('config')

# Application configuration, based on config variables
app.secret_key = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_API_KEY
app.config['ONLINE_LAST_MINUTES'] = ONLINE_LAST_MINUTES
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doxkit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Load up Flask-Bootstrap
Bootstrap(app)

# Load up Google Maps
GoogleMaps(app)

# Load up Flask_Nav
nav = Nav()

# Load up SQLAlchemy
db = SQLAlchemy(app)


# Flask Form for Dox function
class DoxForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    textarea = TextAreaField('Other Information (will be parsed as YAML)', 
    render_kw={"placeholder": """e.g\n Website: https://google.com"""})

# Flask Form for GeoIP function
class GeoIPForm(FlaskForm):
    ip = StringField('IP Address', validators=[IPAddress()])

# Flask Form for DNS function
class DNSForm(FlaskForm):
    url = StringField('Domain Name', [InputRequired()], render_kw={"placeholder": "example.com"})

# SQLAlchemy Model for Dox function
class Doxkit(db.Model):
    __tablename__ = "dox"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    textarea = Column(Text)

    def __init__(self, name, textarea):
        self.name = name
        self.textarea = textarea
    
    def __repr__(self):
        return '<Name {0}>'.format(self.name)

# Helper function for signal Handler to kill safely 
# as well as actual application
def signal_handler(signal, frame):
    print "\033[1;32m\nKilling D0xk1t. Thanks for playing!\033[0m"
    sys.exit(0)
        
# Helper function for deserializing model to yaml
# Thank you: https://stackoverflow.com/questions/42586609/generate-yaml-file-from-sqlalchemy-class-model
def yaml_from_model(model):
    columns = {c.name: c.type.python_type.__name__
               for c in model.__table__.columns}
    return yaml.dump({model.__name__.lower(): columns},
                     default_flow_style=False)

# Start signal handler
signal.signal(signal.SIGINT, signal_handler)

# Global variables to display eye candy
user  = socket.gethostname()
localhost = socket.gethostbyname(user)
lan_ip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read()

header = '\033[1;34m' + """
     ______   _______  __   __  ___   _  ____   _______ 
    |      | |  _    ||  |_|  ||   | | ||    | |       |
    |  _    || | |   ||       ||   |_| | |   | |_     _|
    | | |   || | |   ||       ||      _| |   |   |   |  
    | |_|   || |_|   | |     | |     |_  |   |   |   |  
    |       ||       ||   _   ||    _  | |   |   |   |  
    |______| |_______||__| |__||___| |_| |___|   |___|  
    
    https://github.com/roo7k1d/D0x-K1t-v2
""" + '\033[1;37m'

# Helper function for converting str to dict
@app.template_filter('to_dict')
def to_dict(value):
    return ast.literal_eval(value).items()

# Helper function for serializing JSON to dict
def to_dict_from_json(value):
    return ast.literal_eval(value)

# Helper function for interacting with crt.sh
def subdomain_search(value):
    return json.dumps(crtshAPI().search(str(value)))

# Create database, if not already existing
@app.before_first_request
def setup():
    db.create_all()

# Redirect to /index or /login depending on login session
@app.route('/')
def hello():
    return redirect(url_for('index'))

# Dashboard
@app.route('/index')
def index():
    return render_template('index.html',
                            user=user,
                            title="Admin Dashboard",
                            small="Welcome to D0x-K1t v2!",
                            localhost=localhost, # Localhost address
                            lan_ip=lan_ip,  # LAN Address
                            ) 
# Dox module
@app.route('/dox', methods=['GET', 'POST'])
def dox():
    description = """  D0x-k1t v2 is the new way for gathering information on a specific target. 
          You can use one of the many tools on the left side of the screen.
          If you know another website you want to see on the D0x-K1t website,
          you can easily contact me via GitHub."""

    # Initialize WTForm for display
    form = DoxForm()
    # Query Doxkit database entries
    rows = Doxkit.query.all()
    # If user submitted something, parse yaml and add to database
    if request.method == "POST":
        # Create empty dict to store parsed yaml
        parsed_yaml = {}

        # Load raw text as yaml data into dict
        # ... will now have a key-value structure for template            
        parsed_yaml = yaml.load(request.form["textarea"], Loader=yaml.FullLoader)
        
        # Add 'n commit 'n flash success!
        d = Doxkit(request.form['name'], str(parsed_yaml))
        db.session.add(d)
        db.session.commit()
        flash("D0x created successfully!", "success")
                                
    # Render normally, assumption with GET request    
    return render_template('dox.html',
                            title="D0x Module",
                            small="Writing comprehensive reports for the purpose of information gathering",
                            user=user,
                            description=description,
                            form=form, rows=rows)


# Delete-dox GET request
@app.route('/delete-dox/<delete_id>', methods=['GET'])
def deletedox(delete_id):
    
    # Find query by ID, and then delete
    Doxkit.query.filter_by(id=delete_id).delete()
    
    # Commit Changes
    db.session.commit()
    
    # Notify user
    flash("Deleted query!", "success")
    return redirect(url_for('dox')) 


# Export-dox command
@app.route('/export-dox-csv/<export_id>', methods=['GET'])
def exportdox_csv(export_id):
    
    # Create a time object to append to file
    time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())    
    _csv = open('{}.csv'.format(time), 'wb')
    
    # Create CSV writer to newly created file.
    outcsv = csv.writer(_csv)
    
    # Get all records, and write to CSV.
    records = db.session.query(Doxkit).all()
    [outcsv.writerow([getattr(curr, column.name) for column in Doxkit.__mapper__.columns]) for curr in records]
    _csv.close()
    
    # Notify user
    flash("Exported Dox! Stored in your D0xk1t path.", "success")
    return redirect(url_for('dox'))                     


# GeoIP Module
@app.route('/geoip', methods=['GET', 'POST'])
def geoip():
    description = """
    When working with metadata, IP addresses often pop up as a point-of-interest.
    Using Maxmind and Google Map's APIs, the GeoIP module aims to collect geolocation
    information on public IP addresses, in order to gather data on physical location during
    the reconaissance stage of the killchain. In order to make this module work, please provide a <a href="https://developers.google.com/maps/documentation/javascript/get-api-key">Google Maps API key</a>.
    """
    form = GeoIPForm()

    if request.method == "POST":
        # Create geoip object using data file.
        geoip = pygeoip.GeoIP("src/GeoLiteCity.dat")
        try:
            # Find location by specified IP address
            ip_data = geoip.record_by_addr(request.form['ip'])
            
            # Re-render template with proper coordinates
            return render_template('geoip.html', title="GeoIP Module", user=user, description=description, form=form, latitude=ip_data["latitude"], longitude=ip_data["longitude"], ip_data=ip_data)
        
        # If not, flash error
        except (TypeError, ValueError, socket.error):
            flash("Invalid IP Address provided!", "danger")
            return redirect(url_for('geoip')) 
    else:
        return render_template('geoip.html', title="GeoIP Module", small="Using locational data to conduct info-gathering",
                                user=user, description=description, form=form,
                                latitude="0", longitude="0")

# GeoIP API endpoint    
@app.route('/api/geoip/<ip_address>')
def ipinfo(ip_address):
    geoip = pygeoip.GeoIP("app/GeoLiteCity.dat")
    ip_data = geoip.record_by_addr(ip_address)
    return jsonify(ip_data)
    

# DNS Enumeration
@app.route('/dns', methods=['GET', 'POST'])
def dns():
    description = """
    Targets, whether it be a company or a person, may utilize domains in order to
    display web content. Domains, especially those that are not properly configured,
    give penetration testers great opportunity to gather sensitive information in the
    form of metadata, whether it be an address from a WHOIS lookup, or nameservers."""
    
    form = DNSForm()
    
    if request.method == "POST":
        
        # Obtain whois data 
        whois_data = whois(request.form["url"])
        
        # Subdomain enumeration using crt.sh
        _subdomain = subdomain_search(request.form["url"])
        subdomain = [y['domain'] for y in to_dict_from_json(_subdomain)]
        # Re-render with appopriate parameters
        return render_template('dns.html', title="DNS Enumeration Module", 
                            user=user, description=description, 
                            form=form, whois=whois_data, subdomain=subdomain)
    else:
        return render_template('dns.html', title="DNS Enumeration Module", 
                            user=user,description=description, 
                            form=form, whois=None, subdomain=None)
'''
# Nmap
@app.route('/nmap')
def nmap():
    description = """
    Nmap is a great tool for every penetration tester, and should be available for
    every pentest. However, Nmap does provide tons of features that may seem very
    complex to implement when using the command-line version. Therefore, the webNmap
    module provides a great interface to the tool, enabling the attacker to efficiently
    scan a network or host during info-gathering."""
    return render_template('nmap.html', title="webNmap Module", description=description,
        small="A great user interface for quick Nmap scanning", user=user)
'''
    
# Register filters
app.jinja_env.filters['to_dict'] = to_dict 

if __name__ == '__main__':
    print header
    app.run()
