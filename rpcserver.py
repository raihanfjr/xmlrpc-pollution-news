#import library SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer

#import SimpleXMLRPCRequestHandler dari bagian server
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

#Pembatasan path /RPC
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_path = ('/RPC',)

#Buat Server menggunakan ip serta port dari jaringan server
with SimpleXMLRPCServer(('192.168.43.186', 5005), requestHandler=SimpleXMLRPCRequestHandler, allow_none=False) as server:

	#Buat data struktur dictionary yang digunakan
	list_aqi = {
		"ids": [],
		"aqi": [],
		"suhu": []
	}

	#kode setelah ini adalah critical section
	#siapkan lock
	lock = threading.Lock()

	#buat fungsi
	def input_aqi(ids, aqi, suhu):

		#critical section dimulai harus dilock
		lock.acquire()
		#jika kandidat ada dalam dictionary maka tambahkan nilai votenya
		if len(list_aqi["ids"]) == 0:
			list_aqi["ids"].append(ids)
			list_aqi["aqi"].append(aqi)
			list_aqi["suhu"].append(suhu)
		else:
			for i in range(0, len(list_aqi["ids"])):
				if (list_aqi["ids"][i] == ids):
					list_aqi["aqi"][i] = aqi
					list_aqi["suhu"][i] = suhu
					break
				if (i == len(list_aqi["ids"])-1):
					list_aqi["ids"].append(ids)
					list_aqi["aqi"].append(aqi)
					list_aqi["suhu"].append(suhu)

		#critical section berakhir
		lock.release()
		return True

	#register fungsi vote_candidate sebagai vote
	server.register_function(input_aqi, "inputaqi")

	#buat fungsi cek status aqi
	def status_aqi(aqi):
		if(aqi >= 0 and aqi <= 50):
			status = "Good"
		elif(aqi > 50 and aqi <= 100):
			status = "Moderate"
		elif(aqi > 100 and aqi <= 150):
			status = "Little-Unhealthy"
		elif(aqi > 150 and aqi <= 200):
			status = "Unhealthy"
		elif(aqi > 200 and aqi <= 300):
			status = "Very-Unhealthy"
		elif(aqi > 300):
			status = "Hazardous"
		else:
			status = "error"

		return status

	#register fungsi vote_candidate sebagai vote
	server.register_function(status_aqi, "statusaqi")

	#buat fungsi bernama query result
	def query_result():
		#critical section dimulai
		lock.acquire()

		#hitung aqi
		status = []
		for i in range(0, len(list_aqi["ids"])):
			status.append(status_aqi(list_aqi["aqi"][i]))

		#critical section berakhir
		lock.release()
		return[
			list_aqi["ids"],
			list_aqi["aqi"],
			list_aqi["suhu"],
			status		
			]

	#register query_result sebagai query
	server.register_function(query_result,"query")

	print("Server Jakarta Pollution berjalan...")

	#Jalankan server
	server.serve_forever()