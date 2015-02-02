import numpy as np
from lxml import html
from lxml.etree import tostring
import bs4
import mechanize
import json
import urllib2
import MySQLdb as mdb
def inputTransfer(input_list):
	"""
	transfer input data into the format for random forest prediction
	intput : 29-dim input_list from user clicking
	output : 216-dim meta_list to be sent to random forest regressor
	"""
	output_list = []
	for amenity in input_list[:-8]:   # handle amenities
		if amenity: 
			output_list.append(1)
		else:
			output_list.append(0)

	accommodates = input_list[-8]
	if not accommodates:
		output_list.append(2)
	elif accommodates == '16+':
		output_list.append(16)
	else:
		output_list.append(float(accommodates))

	bathrooms = input_list[-7]
	if not bathrooms:
		output_list.append(1)
	elif bathrooms == '8+':
		output_list.append(8)
	else:
		output_list.append(float(bathrooms))

	bedrooms = input_list[-6]
	if not bedrooms:
		output_list.append(1)
	elif bedrooms == '8+':
		output_list.append(8)
	else:
		output_list.append(float(bedrooms))

	beds = input_list[-5]
	if not beds:
		output_list.append(2)
	elif beds == '16+':
		output_list.append(16)
	else:
		output_list.append(float(beds))

	gender = input_list[-4]
	roomtype = input_list[-3]
	neighborhood = input_list[-2]
	address = input_list[-1]

	# handle address
	add_list = address.split(',')
	api_link_gg = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	for i in range(len(add_list)):
		add_list[i] = '+'.join(add_list[i].split())
		if i>0:
			add_list[i] = ',+' + add_list[i]
		api_link_gg = api_link_gg + add_list[i]
	api_link_gg = api_link_gg + '&key=AIzaSyA573WgEnh01ReQ99PkkY-jFIUV4iZTjR0'
	geo_info = json.load(urllib2.urlopen(api_link_gg))
	lat = geo_info['results'][0]['geometry']['location']['lat'] #return lat 
	lng = geo_info['results'][0]['geometry']['location']['lng'] # return lng

	# now, connect to walkscore api to get the walkscore data
	api_link_ws = 'http://api.walkscore.com/score?format=xml&address='  # come back to this later 
	walkscore = 80
	transitscore = 80
	output_list.append(walkscore)
	output_list.append(transitscore)


	if roomtype == 'Entire Place':  # handle room type
		output_list.extend([1,0,0])
	elif roomtype == 'Private Room':
		output_list.extend([0,1,0])
	elif roomtype == 'Shared Room':
		output_list.extend([0,0,1])
	else:
		output_list.extend([0,0,0])




	if gender == 'Couple':    # handle host gender 
		output_list.extend([1,0,0,0])
	elif gender == 'Female':
		output_list.extend([0,1,0,0])
	elif gender == 'Male':
		output_list.extend([0,0,1,0])
	elif gender == 'Others':
		output_list.extend([0,0,0,1])
	else:
		output_list.extend([0,0,0,0])



	
	if not neighborhood:    # handle neighborhood
		neighborhood = 'SD_Neighborhood_Palo Alto'
	else:
		neighborhood = 'SD_Neighborhood_' + neighborhood

	neighborhood_list = [u'SD_Neighborhood_Alameda',
       u'SD_Neighborhood_Alamo Square', u'SD_Neighborhood_Albany',
       u'SD_Neighborhood_Alum Rock', u'SD_Neighborhood_Angwin',
       u'SD_Neighborhood_Aptos', u'SD_Neighborhood_Aromas',
       u'SD_Neighborhood_Atherton', u'SD_Neighborhood_Bayview',
       u'SD_Neighborhood_Belmont', u'SD_Neighborhood_Belvedere Tiburon',
       u'SD_Neighborhood_Ben Lomond', u'SD_Neighborhood_Berkeley',
       u'SD_Neighborhood_Bernal Heights', u'SD_Neighborhood_Berryessa',
       u'SD_Neighborhood_Bodega', u'SD_Neighborhood_Bodega Bay',
       u'SD_Neighborhood_Boulder Creek',
       u'SD_Neighborhood_Burbank/Del Monte', u'SD_Neighborhood_Burlingame',
       u'SD_Neighborhood_Calistoga', u'SD_Neighborhood_Cambrian/Pioneer',
       u'SD_Neighborhood_Campbell', u'SD_Neighborhood_Capitola',
       u'SD_Neighborhood_Castro Valley', u'SD_Neighborhood_Castroville',
       u'SD_Neighborhood_Cazadero', u'SD_Neighborhood_Central San Jose',
       u'SD_Neighborhood_Chinatown', u'SD_Neighborhood_Civic Center',
       u'SD_Neighborhood_Cole Valley', u'SD_Neighborhood_College Park',
       u'SD_Neighborhood_Concord', u'SD_Neighborhood_Corralitos',
       u'SD_Neighborhood_Cory', u'SD_Neighborhood_Cotati',
       u'SD_Neighborhood_Cow Hollow', u'SD_Neighborhood_Crocker Amazon',
       u'SD_Neighborhood_Cupertino', u'SD_Neighborhood_Davenport',
       u'SD_Neighborhood_Diamond Heights', u'SD_Neighborhood_Dillon Beach',
       u'SD_Neighborhood_Dogpatch', u'SD_Neighborhood_Downtown',
       u'SD_Neighborhood_Duboce Triangle',
       u'SD_Neighborhood_Duncans Mills', u'SD_Neighborhood_East Oakland',
       u'SD_Neighborhood_East Palo Alto',
       u'SD_Neighborhood_East Richmond Heights',
       u'SD_Neighborhood_Edenvale', u'SD_Neighborhood_El Cerrito',
       u'SD_Neighborhood_Emeryville', u'SD_Neighborhood_Evergreen',
       u'SD_Neighborhood_Excelsior', u'SD_Neighborhood_Felton',
       u'SD_Neighborhood_Fetters Hot Springs-Agua Caliente',
       u'SD_Neighborhood_Financial District',
       u"SD_Neighborhood_Fisherman's Wharf",
       u'SD_Neighborhood_Five Wounds/Brookwood Terrace',
       u'SD_Neighborhood_Forestville', u'SD_Neighborhood_Foster City',
       u'SD_Neighborhood_Freestone', u'SD_Neighborhood_Fremont',
       u'SD_Neighborhood_Geyserville', u'SD_Neighborhood_Gilroy',
       u'SD_Neighborhood_Glen Ellen', u'SD_Neighborhood_Glen Park',
       u'SD_Neighborhood_Graton', u'SD_Neighborhood_Guerneville',
       u'SD_Neighborhood_Haight-Ashbury', u'SD_Neighborhood_Half Moon Bay',
       u'SD_Neighborhood_Hayes Valley', u'SD_Neighborhood_Hayward',
       u'SD_Neighborhood_Healdsburg', u'SD_Neighborhood_Hercules',
       u'SD_Neighborhood_Highlands-Baywood Park',
       u'SD_Neighborhood_Hillsborough', u'SD_Neighborhood_Ingleside',
       u'SD_Neighborhood_Inner Sunset', u'SD_Neighborhood_Inverness',
       u'SD_Neighborhood_Jenner', u'SD_Neighborhood_Kensington',
       u'SD_Neighborhood_Kenwood', u'SD_Neighborhood_La Honda',
       u'SD_Neighborhood_La Selva Beach', u'SD_Neighborhood_Lafayette',
       u'SD_Neighborhood_Lakeshore', u'SD_Neighborhood_Laurel Park',
       u'SD_Neighborhood_Los Altos', u'SD_Neighborhood_Los Altos Hills',
       u'SD_Neighborhood_Los Gatos', u'SD_Neighborhood_Marin',
       u'SD_Neighborhood_Marina', u'SD_Neighborhood_Marshall',
       u'SD_Neighborhood_Menlo Park', u'SD_Neighborhood_Middletown',
       u'SD_Neighborhood_Millbrae', u'SD_Neighborhood_Milpitas',
       u'SD_Neighborhood_Mission District',
       u'SD_Neighborhood_Mission Terrace', u'SD_Neighborhood_Monte Rio',
       u'SD_Neighborhood_Monte Sereno', u'SD_Neighborhood_Monterey',
       u'SD_Neighborhood_Morgan Hill', u'SD_Neighborhood_Moss Landing',
       u'SD_Neighborhood_Mountain View', u'SD_Neighborhood_Napa',
       u'SD_Neighborhood_Newark', u'SD_Neighborhood_Newhall/Sherwood',
       u'SD_Neighborhood_Nob Hill', u'SD_Neighborhood_Noe Valley',
       u'SD_Neighborhood_North Beach', u'SD_Neighborhood_North San Jose',
       u'SD_Neighborhood_North and East', u'SD_Neighborhood_Novato',
       u'SD_Neighborhood_Oakland', u'SD_Neighborhood_Occidental',
       u'SD_Neighborhood_Oceanview', u'SD_Neighborhood_Orinda',
       u'SD_Neighborhood_Outer Sunset', u'SD_Neighborhood_Pacific Grove',
       u'SD_Neighborhood_Pacific Heights', u'SD_Neighborhood_Palo Alto',
       u'SD_Neighborhood_Penngrove', u'SD_Neighborhood_Pescadero',
       u'SD_Neighborhood_Petaluma', u'SD_Neighborhood_Pinole',
       u'SD_Neighborhood_Pleasanton', u'SD_Neighborhood_Portola Valley',
       u'SD_Neighborhood_Potrero Hill',
       u'SD_Neighborhood_Presidio Heights', u'SD_Neighborhood_Prunedale',
       u'SD_Neighborhood_Redwood City', u'SD_Neighborhood_Richmond Annex',
       u'SD_Neighborhood_Richmond District',
       u'SD_Neighborhood_Richmond Heights', u'SD_Neighborhood_Rio Del Mar',
       u'SD_Neighborhood_Rio del Mar', u'SD_Neighborhood_Rohnert Park',
       u'SD_Neighborhood_Royal Oaks', u'SD_Neighborhood_Russian Hill',
       u'SD_Neighborhood_Saint Helena', u'SD_Neighborhood_Salinas',
       u'SD_Neighborhood_San Carlos', u'SD_Neighborhood_San Francisco',
       u'SD_Neighborhood_San Jose', u'SD_Neighborhood_San Leandro',
       u'SD_Neighborhood_San Martin', u'SD_Neighborhood_San Mateo',
       u'SD_Neighborhood_Santa Clara', u'SD_Neighborhood_Santa Cruz',
       u'SD_Neighborhood_Santa Rosa', u'SD_Neighborhood_Saratoga',
       u'SD_Neighborhood_Sausalito', u'SD_Neighborhood_Scotts Valley',
       u'SD_Neighborhood_Sebastopol',
       u'SD_Neighborhood_Shasta/Hanchett Park', u'SD_Neighborhood_SoMa',
       u'SD_Neighborhood_Sonoma', u'SD_Neighborhood_Soquel',
       u'SD_Neighborhood_Soquel -Santa Cruz',
       u'SD_Neighborhood_South Beach', u'SD_Neighborhood_South San Jose',
       u'SD_Neighborhood_St Helena', u'SD_Neighborhood_Stanford',
       u'SD_Neighborhood_Sunnyside', u'SD_Neighborhood_Sunnyvale',
       u'SD_Neighborhood_Telegraph Hill', u'SD_Neighborhood_Tenderloin',
       u'SD_Neighborhood_The Castro', u'SD_Neighborhood_Tomales',
       u'SD_Neighborhood_Twin Peaks', u'SD_Neighborhood_Union City',
       u'SD_Neighborhood_Valley Ford', u'SD_Neighborhood_Walnut Creek',
       u'SD_Neighborhood_Watsonville', u'SD_Neighborhood_West Valley',
       u'SD_Neighborhood_Western Addition/NOPA',
       u'SD_Neighborhood_Willow Glen', u'SD_Neighborhood_Windsor',
       u'SD_Neighborhood_Woodside',
       u'SD_Neighborhood_Yountville - Napa Valley']

	x = [0]*len(neighborhood_list)
 	for i in range(len(neighborhood_list)):
		if neighborhood == neighborhood_list[i]:
			x[i] = 1
	output_list.extend(x)
	return output_list,lat,lng

