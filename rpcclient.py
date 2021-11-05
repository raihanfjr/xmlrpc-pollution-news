#import xmlrpc client
import xmlrpc.client
import sys
import os
#buat stub (proxy) untuk client
proxy = xmlrpc.client.ServerProxy("http://192.168.100.4:5005")

#deskripsi aqi
def deskripsi_aqi(status):
		print()
		if (status == "Good"):
			print("Kualitas udara bagus, dan tidak terdapat resiko pada kesehatan anda")
			print()
			print("Rekomendasi: ")
			print("Silahkan nikmati aktivitas anda di luar ruangan")
			print("Kami sarankan untuk buka kaca dan ventilasi rumah anda untuk sirkulasi udara segar yang kaya akan oksigen")
			print()
		elif (status == "Moderate"):
			print("Kualitas udara cukup baik, dan terdapat resiko kecil pada kesehatan anda")
			print()
			print("Rekomendasi: ")
			print("Bagi anda yang sedikit sensitif terhadap udara kotor, diharapkan mengurangi aktivitas anda di luar ruangan")
			print("Kami tidak menyarankan untuk membuka kaca dan ventilasi rumah anda untuk menghindari udara yang sedikit kotor")
			print()
		elif (status == "Little-Unhealthy"):
			print("Udara saat ini dapat menyebabkan resiko iritasi dan masalah pernafasan")
			print()
			print("Rekomendasi: ")
			print("Diharapkan mengurangi aktivitas anda di luar ruangan")
			print("Bagi anda yang sensitif terhadap udara kotor diharapkan untuk menghindari segala aktivitas anda di luar ruangan")
			print("Nyalakan alat pembersih udara jika udara di dalam ruangan dirasa kotor")
			print()
		elif (status == "Unhealthy"):
			print("Udara saat ini dapat menyebabkan resiko besar pada jantung dan paru paru")
			print()
			print("Rekomendasi: ")
			print("Diharapkan untuk menghindari segala aktivitas di luar ruangan")
			print("Nyalakan alat pembersih udara jika udara di dalam ruangan dirasa kotor")
			print()
		elif (status == "Very-Unhealthy"):
			print("Udara saat ini dapat menyebabkan resiko besar pada jantung dan paru paru pada setiap orang, dan dapat menurunkan daya tahan tubuh bagi anda yang sensitif terhadap udara kotor")
			print()
			print("Rekomendasi: ")
			print("Diharapkan mengurangi aktivitas anda di luar ruangan")
			print("Bagi anda yang sensitif terhadap udara kotor diharapkan untuk menghindari segala aktivitas anda di luar ruangan")
			print("Nyalakan alat pembersih udara jika udara di dalam ruangan dirasa kotor")
			print()
		elif (status == "Hazardous"):
			print("Udara saat ini dapat menyebabkan resiko besar pada iritasi kuat dan efek kesehatan yang memicu penyakit besar lainnya")
			print()
			print("Rekomendasi: ")
			print("Diharapkan mengurangi aktivitas anda di luar ruangan")
			print("Bagi anda yang sensitif terhadap udara kotor diharapkan untuk menghindari segala aktivitas anda di luar ruangan")
			print("Nyalakan alat pembersih udara di dalam ruangan")
			print()
		else:
			print("error")
			print()

#Lakukan pemanggilan fungsi vote
def inputsuhu():
	hasil=proxy.query()
	hitungsuhu()
	print()
	print("*******INPUT AIR QUALITY INDEX******")
	ids = int(input("Masukkan id suhu: "))
	aqi = int(input("Masukkan AQI (Air Quality Index): "))
	suhu = int(input("Masukkan suhu: "))
	proxy.inputaqi(ids, aqi, suhu)
	print("************************************")
	print()
	input("Succeed, Press Enter to continue...")


#Lakukan pemanggilan fungsi lain
def hitungsuhu():
	hasil=proxy.query()
	sums = 0
	suma = 0
	print("*******AIR QUALITY INDEX LIST*******")
	if(len(hasil[0])==0):
		print("Belum ada input")
		print("************************************")
		print()
		input("Press Enter to continue...")
	else:
		for i in range(0, len(hasil[0])):
			sums = sums + hasil[2][i]
			suma = suma + hasil[1][i]
			print("AQI -", hasil[0][i], "| AQI:", hasil[1][i],", Suhu:",hasil[2][i],"C , Status:", hasil[3][i]);

		rsuhu = sums/len(hasil[0])
		raqi = suma/len(hasil[0])
		status = proxy.statusaqi(raqi)

		print("Rata rata suhu: ", rsuhu, "C")
		print("Rata rata AQI: ", raqi, "-", status)
		print("************************************")
		deskripsi_aqi(status)
		print("***********************************")
		input("Press Enter to continue...")
		print()


def menu():
    print("*******JAKARTA POLLUTION NEWS*******")
    print()

    choice = input("""
    	A: Publish Air Quality Index
    	B: View Air Quality Index
    	Q: Quit

    	Masukkan pilihan: """)

    print("************************************")
    print()
    os.system('cls')

    if choice == "A" or choice =="a":
        inputsuhu()
        os.system('cls')
        menu()
    elif choice == "B" or choice =="b":
        hitungsuhu()
        os.system('cls')
        menu()
    elif choice=="Q" or choice=="q":
        sys.exit()
    else:
    	os.system('cls')
    	print("Anda harus memasukan A,B, atau Q")
    	print("Silahkan coba lagi")
    	menu()

if __name__ == '__main__':
	os.system('cls')
	menu()


