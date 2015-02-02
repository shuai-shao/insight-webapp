from flask import render_template, request
from app import app
import MySQLdb as mdb
from a_Model import Modellt
import dataclean as dc
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
import cPickle

# @app.route('/')
# @app.route('/index')
# def index():
#     user = { 'nickname': 'Sean' }   # fake user
#     return  render_template("index.html", title = 'Home', user = user)

@app.route('/')
def prices_input():
    return render_template('input.html')

@app.route('/output', methods=['GET'])
def cities_output():
    # print request.args.get('test')
    # return render_template('input.html')

    address = request.args.get('address')  # read in location
    if not address:
        address = '26 Sheridan Avenue, Palo Alto, CA'
    neighborhood = address.split(',')[1]
    roomtype = request.args.get('roomtype')
    gender = request.args.get('gender')
    bedrooms = request.args.get('bedrooms')
    beds = request.args.get('beds')
    bathrooms = request.args.get('bathrooms')
    accommodates = request.args.get('accommodates')
    # get amenities 
    wireless_internet = request.args.get('wireless_internet')
    tv = request.args.get('tv')
    kitchen = request.args.get('kitchen')
    air_conditioning = request.args.get('air_conditioning')
    breakfast = request.args.get('breakfast')
    cable_tv = request.args.get('cable_tv')
    events = request.args.get('events')
    co_detector = request.args.get('co_detector')
    doorman = request.args.get('doorman')
    washer = request.args.get('washer')
    dryer = request.args.get('dryer')
    first_aid_kit = request.args.get('first_aid_kit')
    free_parking = request.args.get('free_parking')
    gym = request.args.get('gym')
    heating = request.args.get('heating')
    essentials= request.args.get('essentials')
    hot_tub = request.args.get('hot_tub')
    fireplace = request.args.get('fireplace')
    pool = request.args.get('pool')
    fire_extinguisher = request.args.get('fire_extinguisher')
    shampoo = request.args.get('shampoo')
  
    input_list = [air_conditioning, breakfast, cable_tv,co_detector,doorman,dryer,tv,essentials,events,
    fire_extinguisher,fireplace,first_aid_kit,gym,heating,hot_tub,wireless_internet,kitchen,free_parking,
    pool,shampoo,washer,accommodates,bathrooms,bedrooms,beds,gender,roomtype,neighborhood,address]

    output_list,lat,lng = dc.inputTransfer(input_list)


    print "input list is:\n" + str(len(input_list))
    print input_list
    print "output list is:\n" + str(len(output_list))
    print output_list

    # with db:
    #     cur = db.cursor()
    #     cur.execute('SELECT * FROM training_data_X')
    #     query_results = cur.fetchall()
    # print query_results
    with open('rf_regressor','rb') as f:
        rf = cPickle.load(f)

    # training = pd.read_csv('training.csv')
    # training_data_X = np.array(training.drop('Price',1))
    # training_data_y = np.array(training['Price'])
    # rf = RandomForestRegressor(n_estimators = 100)
    # rf.fit(training_data_X,training_data_y)
    predicted_price = rf.predict(output_list)

    the_result = predicted_price
    return render_template('output.html',lat = lat, lng=lng,the_result=the_result)
