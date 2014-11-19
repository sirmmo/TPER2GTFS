#! /bin/env python

#docs:
#https://developers.google.com/transit/gtfs/examples/gtfs-feed


#agency
#agency_id, agency_name,agency_url,agency_timezone,agency_phone,agency_lang
files = {}

files["agency.txt"] = {
	"fields":['agency_id', 'agency_name','agency_url','agency_timezone','agency_phone','agency_lang'],
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
	"origin":"stops.csv",
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
files["routes.txt"] = {
	"origin":"lines.csv",
	"fields": ['route_id','route_short_name','route_long_name','route_desc','route_type'],
	"cols":{
			'route_id':{"id":0, "op":str},
			'route_short_name':{"id":0, "op":str},
			'route_long_name':{"id":0,"op":str},
			'route_desc':{"id":0, "op":str},
			'route_type':1,
		}
	}

#trips
#route_id,service_id,trip_id,trip_headsign,block_id
files["trips.txt"] = {
	"origin":"stoplist.csv",
	"fields": ['route_id','service_id','trip_id','trip_headsign','block_id'],
	"cols":{
			'route_id':{"id":0, "op":str},
			'service_id':{"id":9, "op":int},
			'trip_id':{"id":1,"op":str},
			'trip_headsign':{"id":0, "op":str},
			'block_id':{"id":1, "op":str},
		}
	}

#stop_times
#trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type
files["stop_times.txt"] = {
	"origin":"stoplist.csv",
	"fields": ['trip_id','arrival_time','departure_time','stop_id','stop_sequence','pickup_type','drop_off_type'],
	"cols":{
			'trip_id':{"id":1, "op":int},
			'arrival_time':"ws",
			'departure_time':"ws",
			'stop_id':{"id":1, "op":str},
			'stop_sequence':0,
			'pickup_type':0,
			'drop_off_type':0,
		}
	}

#shapes
#shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled


#calendar
#service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date

#calendar_dates
#service_id,date,exception_type

#fare_attributes
#fare_id,price,currency_type,payment_method,transfers,transfer_duration

#fare_rules
#fare_id,route_id,origin_id,destination_id,contains_id

the_stops = []

def get_files():	
	import urllib
	import csv

	#stops_url = "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=tper.it&filename=fermate&version=20141101&format=csv"
	#line_arcs_url = "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=tper.it&filename=archi&version=20141101&format=csv"
	#lines_url = "https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=tper.it&filename=linee&version=20141101&format=csv"
	#stoplist_url ="https://solweb.tper.it/web/tools/open-data/open-data-download.aspx?source=solweb.tper.it&filename=lineefermate&version=20141101&format=csv"
#
#	#print "getting", "stops.csv"
#	#urllib.urlretrieve(stops_url, "stops.csv")
#
#	#print "getting", "lines.csv"
#	#urllib.urlretrieve(lines_url, "lines.csv")
#
#	#print "getting", "arcs.csv"
#	#urllib.urlretrieve(line_arcs_url, "arcs.csv")
#
#	#print "getting", "stoplist.csv"
	#urllib.urlretrieve(stoplist_url, "stoplist.csv")

	print "writing", "agency.txt"
	#agency
	with open("agency.txt", "wb") as stops_out:
		_out = csv.DictWriter(stops_out, files["agency.txt"].get("fields"))
		_out.writerow(dict(zip(files["agency.txt"].get("fields"),files["agency.txt"].get("fields"))))
		firstrow = True
		_out.writerow(files["agency.txt"].get("data"))
	print "written", "agency.txt"


	#stops
	print "writing", "stops.txt"
	with open("stops.csv","rb") as stops_in:
		with open("stops.txt", "wb") as stops_out:
			_in = csv.reader(stops_in, delimiter=';')
			_out = csv.DictWriter(stops_out, files["stops.txt"].get("fields"))
			_out.writerow(dict(zip(files["stops.txt"].get("fields"),files["stops.txt"].get("fields"))))
			firstrow = True
			for _inrow in _in:
				if firstrow:
					firstrow=False
				else:
					the_stops.append(_inrow[0])
					to_add = {}
					for k,v in files["stops.txt"].get("cols").items():
						to_add[k] = v.get("op")(_inrow[v.get("id")].replace(",", ".")) if type(v)== dict else v
					_out.writerow(to_add)
	print "written", "stops.txt"

	#routes
	print "writing", "routes.txt"
	with open("lines.csv","rb") as stops_in:
		with open("routes.txt", "wb") as stops_out:
			_in = csv.reader(stops_in, delimiter=';')
			_out = csv.DictWriter(stops_out, files["routes.txt"].get("fields"))
			_out.writerow(dict(zip(files["routes.txt"].get("fields"),files["routes.txt"].get("fields"))))
			firstrow = True
			for _inrow in _in:
				if firstrow:
					firstrow=False
				else:
					the_stops.append(_inrow[0])
					to_add = {}
					for k,v in files["routes.txt"].get("cols").items():
						to_add[k] = v.get("op")(_inrow[v.get("id")].replace(",", ".")) if type(v)== dict else v
					_out.writerow(to_add)
	print "written", "routes.txt"

	#trips
	print "writing", "trips.txt"
	with open("stoplist.csv","rb") as stops_in:
		with open("trips.txt", "wb") as stops_out:
			_in = csv.reader(stops_in, delimiter=';')
			_out = csv.DictWriter(stops_out, files["trips.txt"].get("fields"))
			_out.writerow(dict(zip(files["trips.txt"].get("fields"),files["trips.txt"].get("fields"))))
			firstrow = True
			for _inrow in _in:
				if firstrow:
					firstrow=False
				else:
					the_stops.append(_inrow[0])
					to_add = {}
					for k,v in files["trips.txt"].get("cols").items():
						to_add[k] = v.get("op")(_inrow[v.get("id")].replace(",", ".")) if type(v)== dict else v
					_out.writerow(to_add)
	print "written", "stop_times.txt"

	#trips
	print "writing", "stop_times.txt"
	with open("stoplist.csv","rb") as stops_in:
		with open("stop_times.txt", "wb") as stops_out:
			_in = csv.reader(stops_in, delimiter=';')
			_out = csv.DictWriter(stops_out, files["stop_times.txt"].get("fields"))
			_out.writerow(dict(zip(files["stop_times.txt"].get("fields"),files["stop_times.txt"].get("fields"))))
			firstrow = True
			for _inrow in _in:
				if firstrow:
					firstrow=False
				else:
					the_stops.append(_inrow[0])
					to_add = {}

					stop = _inrow[1]
					line = _inrow[0]

					for k,v in files["stop_times.txt"].get("cols").items():
						to_add[k] = v.get("op")(_inrow[v.get("id")].replace(",", ".")) if type(v)== dict else v

					get_times(_out, to_add, [stop], [line])
	print "written", "trips.txt"





def get_times(out, to_add = {}, stops = [], lines = []):
	from suds.client import Client

	hellobus = 'https://solweb.tper.it/tperit/webservices/hellobus.asmx?wsdl'
	hourslots = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
	minslots = ["00","15","30","45"]


	times = []

	hbclient = Client(hellobus)
	hbclient.set_options(port="HelloBusSoap")
	for hour in hourslots:
		for minute in minslots:
			for stop in stops:
				for line in lines:
					print "getting", hour, minute, stop, line
					for coming in hbclient.service.QueryHellobus4ivr(stop,line, hour+minute).split("\n")[2].split(" "):
						if "P" in coming:
							time = coming.split("P")[0].strip()
							times.append(time)
						times = list(set(times))
	for time in times:
		to_add["arrival_time"] = time[:2]+":"+time[2:]
		to_add["departure_time"] = time[:2]+":"+time[2:]
		out.writerow(to_add)
		

def zip_files():
	import zipfile
	to_zip = files.keys()

	with zipfile.ZipFile("GTFS.zip", "w") as gtfs:
		for f in to_zip:
			gtfs.write(f)


if __name__ == "__main__":
	get_files()
	
	zip_files()

