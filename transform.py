#! /bin/env python

#docs:
#https://developers.google.com/transit/gtfs/examples/gtfs-feed


#agency
#agency_id, agency_name,agency_url,agency_timezone,agency_phone,agency_lang
files = {}

files["agency.txt"] = {
	"data":{
		"agency_id":"TPER",
		"agency_name":"TPER",
		"agency_url":"http://www.tper.it/",
		"agency_timezone":"Europe/Rome",
		"agency_phone":"",
		"agency_lang":"it"
		}
	}

#stops
#stop_id,stop_name,stop_desc,stop_lat,stop_lon,stop_url,location_type,parent_station
files["stops.txt"] = {
	"fields": ['stop_id', "stop_name","stop_desc", "stop_lat", "stop_lon", "stop_url", "location_type", "parent_station"],
	"cols":{
			'stop_id':{"id":0, "op":str},
			'stop_name':{"id":1, "op":str},
			'stop_desc':{"id":2,"op":str},
			'stop_lat':{"id":6, "op":float},
			'stop_lon':{"id":7, "op":float},
			'stop_url':None,
			'location_type':None,
			'parent_station':None,
		}
	}

#routes
#route_id,route_short_name,route_long_name,route_desc,route_type


#trips
#route_id,service_id,trip_id,trip_headsign,block_id


#stop_times
#trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type


#calendar
#service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date


#calendar_dates
#service_id,date,exception_type

#fare_attributes
#fare_id,price,currency_type,payment_method,transfers,transfer_duration


#fare_rules
#fare_id,route_id,origin_id,destination_id,contains_id

#shapes
#shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled


#frequencies
#trip_id,start_time,end_time,headway_secs

#transfers
#from_stop_id,to_stop_id,transfer_type,min_transfer_time


def get_files():	
	import urllib
	import csv

	stops_url = "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=tper.it&filename=fermate&version=20141101&format=csv"
	line_arcs_url = "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=tper.it&filename=archi&version=20141101&format=csv"
	lines_url = "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=tper.it&filename=linee&version=20141101&format=csv"

	urllib.urlretrieve(stops_url, "stops.csv")
	urllib.urlretrieve(lines_url, "lines.csv")
	urllib.urlretrieve(line_arcs_url, "arcs.csv")

	#stops
	__struct = files["stops.txt"]

	with open("stops.csv","rb") as stops_in:
		with open("stops.txt", "wb") as stops_out:
			_in = csv.reader(stops_in, delimiter=';')
			_out = csv.DictWriter(stops_out, __struct.get("fields"))
			_out.writerow(dict(zip(__struct.get("fields"),__struct.get("fields"))))
			firstrow = True
			for _inrow in _in:
				if firstrow:
					firstrow=False
				else:
					to_add = {}
					for k,v in __struct.get("cols").items():
						print _in, v
						to_add[k] = v.get("op")(_inrow[v.get("id")].replace(",", ".")) if v is not None else None
					_out.writerow(to_add)




def get_times(stops = [], lines = []):
	from suds.client import Client

	hellobus = 'https://solweb.tper.it/tperit/webservices/hellobus.asmx?wsdl'
	hourslots = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
	minslots = ["00","15","30","45"]

	hbclient = Client(hellobus)
	hbclient.set_options(port="HelloBusSoap")
	for hour in hourslots:
		for minute in minslots:
			for stop in stops:
				for line in lines:
					print hbclient.service.QueryHellobus4ivr(stop,line, hour+minute)
		

def zip_files():
	import zipfile
	to_zip = files.keys()

	with zipfile.ZipFile("GTFS.zip", "w") as gtfs:
		for f in to_zip:
			gtfs.write(f)


if __name__ == "__main__":
	get_files()
	
	get_times()

	zip_files()

