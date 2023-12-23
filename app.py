from flask import Flask, render_template
import pymysql
from beautifultable import BeautifulTable

app = Flask(__name__)

# Fuzzy logic harga
def harga_murah(harga):
    if harga <= 50:
        return 1
    if harga >= 150:
        return 0
    if 50 < harga < 150:
        return round(((150 - harga) / 100), 3)

def harga_normal(harga):
    if harga <= 50 or harga >= 500:
        return 0
    if 50 < harga < 150:
        return round(((harga - 50) / 100), 3)
    if 150 < harga < 500:
        return round(((500 - harga) / 350), 3)

def harga_mahal(harga):
    if harga <= 150:
        return 0
    if harga >= 500:
        return 1
    if 150 < harga < 500:
        return round(((harga - 150) / 350), 3)

def predict_Harga(harga):
    try:
        murah = harga_murah(float(harga))
        normal = harga_normal(float(harga))
        mahal = harga_mahal(float(harga))
        return murah, normal, mahal
    except Exception as e:
        print(f"Error predicting harga for {harga}: {e}")
        return None, None, None

#Fuzzy logic dimensi

def panjang_Pendek(panjang):
    if panjang <= 65:
        return 1
    if panjang >= 100:
        return 0
    if panjang > 65 and panjang < 100:
        return (100 - panjang) / 35


def panjang_Normal(panjang):
    if panjang <= 65 or panjang >= 200:
        return 0
    if panjang > 65 and panjang < 100:
        return (panjang - 65) / 35
    if panjang > 100 and panjang < 200:
        return (200 - panjang) / 100


def panjang_Panjang(panjang):
    if panjang <= 100:
        return 0
    if panjang >= 200:
        return 1
    if panjang > 100 and panjang < 200:
        return (panjang - 100) / 100


def lebar_Sempit(lebar):
    if lebar <= 20:
        return 1
    if lebar >= 45:
        return 0
    if lebar > 20 and lebar < 45:
        return (45 - lebar) / 7


def lebar_Normal(lebar):
    if lebar <= 20 or lebar >= 45:
        return 0
    if lebar > 20 and lebar < 45:
        return (lebar - 20) / 15
    if lebar > 45 and lebar < 80:
        return (80 - lebar) / 35


def lebar_Lebar(lebar):
    if lebar <= 45:
        return 0
    if lebar >= 80:
        return 1
    if lebar > 45 and lebar < 80:
        return (lebar - 45) / 35


def tebal_Tipis(tebal):
    if tebal <= 10:
        return 1
    if tebal >= 25:
        return 0
    if tebal > 10 and tebal < 25:
        return (25 - tebal) / 15


def tebal_Normal(tebal):
    if tebal <= 10 or tebal >= 100:
        return 0
    if tebal > 10 and tebal < 25:
        return (tebal - 10) / 15
    if tebal > 25 and tebal < 100:
        return (100 - tebal) / 75


def tebal_Tebal(tebal):
    if tebal <= 25:
        return 0
    if tebal >= 100:
        return 1
    if tebal > 25 and tebal < 100:
        return (tebal - 25) / 75


def ukuran_kecil(ukuran):
    if ukuran <= 13:
        return 1
    if ukuran >= 112.5:
        return 0
    if ukuran > 13 and ukuran < 112.5:
        return round(((112.5 - ukuran) / 99.5), 3)


def ukuran_normal(ukuran):
    if ukuran <= 13 or ukuran >= 1600:
        return 0
    if ukuran > 13 and ukuran < 99.5:
        return (ukuran - 13) / 99.5
    if ukuran > 99.5 and ukuran < 1600:
        return round(((1600 - ukuran) / 1487.5), 3)


def ukuran_besar(ukuran):
    if ukuran <= 112.5:
        return 0
    if ukuran >= 1600:
        return 1
    if ukuran > 112.5 and ukuran < 1600:
        return round(((ukuran - 112.5) / 1487.5), 3)


def predict_Dimensi(panjang, lebar, tebal):
    ukuran = (panjang * lebar * tebal) / 1000
    kecil = ukuran_kecil(ukuran)
    normal = ukuran_normal(ukuran)
    besar = ukuran_besar(ukuran)
    return kecil, normal, besar


def pb_kecil(RAM):
    if RAM <= 2:
        return 1
    if RAM >= 4:
        return 0
    if RAM > 2 and RAM < 4:
        return round(((4 - RAM) / 3), 3)


def pb_sedang(RAM):
    if RAM <= 2 or RAM >= 16:
        return 0
    if RAM > 2 and RAM <= 4:
        return round(((RAM - 2) / 3), 3)
    if RAM > 4 and RAM < 16:
        return round(((16 - RAM) / 8), 3)


def pb_besar(RAM):
    if RAM <= 4:
        return 0
    if RAM >= 16:
        return 1
    if RAM > 4 and RAM < 16:
        return round(((RAM - 4) / 8), 3)


def predict_RAM(RAM):
    kecil = pb_kecil(RAM)
    sedang = pb_sedang(RAM)
    besar = pb_besar(RAM)

    return kecil, sedang, besar


#fuzzy logic baterai
def pb_kecil(Baterai):
    if Baterai <= 1400:
        return 1
    if Baterai >= 2000:
        return 0
    if Baterai > 5 and Baterai < 2000:
        return round(((2000 - Baterai) / 1800), 3)


def pb_sedang(Baterai):
    if Baterai <= 1400 or Baterai >= 5000:
        return 0
    if Baterai > 1400 and Baterai <= 2000:
        return round(((Baterai - 1400) / 1800), 3)
    if Baterai > 2000 and Baterai < 5000:
        return round(((5000 - Baterai) / 3500), 3)


def pb_besar(Baterai):
    if Baterai <= 2000:
        return 0
    if Baterai >= 5000:
        return 1
    if Baterai > 2000 and Baterai < 5000:
        return round(((Baterai - 2000) / 3500), 3)


def predict_Baterai(Baterai):
    kecil = pb_kecil(Baterai)
    sedang = pb_sedang(Baterai)
    besar = pb_besar(Baterai)

    return kecil, sedang, besar

#fuzzy logic kamera belakang

def pb_rendah(KameraBlkng):
    if KameraBlkng <= 5:
        return 1
    if KameraBlkng >= 20:
        return 0
    if KameraBlkng > 5 and KameraBlkng < 20:
        return round(((20 - KameraBlkng) / 15), 3)


def pb_menengah(KameraBlkng):
    if KameraBlkng <= 5 or KameraBlkng >= 40:
        return 0
    if KameraBlkng > 5 and KameraBlkng <= 20:
        return round(((KameraBlkng - 5) / 15), 3)
    if KameraBlkng > 20 and KameraBlkng < 40:
        return round(((40 - KameraBlkng) / 35), 3)


def pb_tinggi(KameraBlkng):
    if KameraBlkng <= 20:
        return 0
    if KameraBlkng >= 40:
        return 1
    if KameraBlkng > 20 and KameraBlkng < 40:
        return round(((KameraBlkng - 20) / 35), 3)


def predict_KameraBlkng(KameraBlkng):
    rendah = pb_rendah(KameraBlkng)
    menengah = pb_menengah(KameraBlkng)
    tinggi = pb_tinggi(KameraBlkng)

    return rendah, menengah, tinggi



# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='fuzzy',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('index.html')

#route untuk dimensi
@app.route('/dimensi')
def dimensi():
    # Fetch data from the database for Dimensi
    try:
        with connection.cursor() as sql:
            sql.execute("SELECT Type, P, L, T FROM DataHP")
            fetched_rows = sql.fetchall()

            # Perform fuzzy logic predictions
            table_dimensi = BeautifulTable()
            header_dimensi = ["No", "Type", "P", "L", "T", "P*L*T", "Kecil", "Normal", "Besar"]
            table_dimensi.column_headers = header_dimensi

            nomor = 1
            for row in fetched_rows:
                kecil, normal, besar = predict_Dimensi(panjang=row["P"], lebar=row["L"], tebal=row["T"])
                table_dimensi.append_row([nomor, row["Type"], row["P"], row["L"], row["T"], row["P"] * row["L"] * row["T"],
                                          kecil, normal, besar])
                nomor += 1

        # Close the database connection
        return render_template('dimensi.html', table=table_dimensi)
    except Exception as e:
        print(f"Error: {e}")



#route untuk harga
@app.route('/harga')
def harga():
    try:
        with connection.cursor() as sql:
            # harga
            sql.execute("SELECT Type, Harga FROM DataHP")
            table_harga = BeautifulTable()

            header_harga = ["No", "Type", "Harga", "Murah", "Normal", "Mahal"]
            table_harga.column_headers = header_harga

            harga = 1

            for row in sql.fetchall():
                murah, normal, mahal = predict_Harga(row["Harga"])
                table_harga.append_row([harga, row["Type"], row["Harga"], murah, normal, mahal])
                harga += 1
        return render_template('harga.html', table=table_harga)
    except Exception as e:
        print(f"Error: {e}")



@app.route('/ram')
def ram():

    try:
        with connection.cursor() as sql:
            sql.execute("SELECT Type, RAM FROM DataHP")
            fetched_rows = sql.fetchall()

            # Perform fuzzy logic predictions for RAM
            table_RAM = BeautifulTable()
            table_RAM.column_headers = ["No", "Type", "RAM", "Kecil", "Sedang", "Besar"]

            nomor = 1
            for row in fetched_rows:
                kecil, sedang, besar = predict_RAM(row["RAM"])
                table_RAM.append_row([nomor, row["Type"], row["RAM"], kecil, sedang, besar])
                nomor += 1


        return render_template('ram.html', table=table_RAM)

    except Exception as e:
        # Log or print the error for debugging
        print(f"Error: {e}")

@app.route('/baterai')
def baterai():
    try:
        with connection.cursor() as sql:
            sql.execute("SELECT Type,Baterai FROM DataHP")
            fetched_rows = sql.fetchall()

            # Perform fuzzy logic predictions for Baterai
            table_Baterai = BeautifulTable()
            table_Baterai.column_headers = ["No","Type","Baterai","Rendah","Menengah","Tinggi"]

            nomor = 1
            for row in fetched_rows:
                kecil, sedang, besar = predict_Baterai(row["Baterai"])
                table_Baterai.append_row([nomor, row["Type"], row["Baterai"], kecil, sedang, besar])
                nomor = nomor + 1


        return render_template('baterai.html', table=table_Baterai)

    except Exception as e:
        # Log or print the error for debugging
        print(f"Error: {e}")




@app.route('/belakang')
def belakang():
    try:
        with connection.cursor() as sql:
            sql.execute("SELECT Type,KameraBlkng FROM DataHP")
            fetched_rows = sql.fetchall()

            # Perform fuzzy logic predictions for Baterai
            table_KameraBlkng = BeautifulTable()
            table_KameraBlkng.column_headers = ["No","Type","KameraBlkng","Rendah","Menengah","Tinggi"]

            nomor = 1
            for row in fetched_rows:
                rendah, menengah, tinggi = predict_KameraBlkng(row["KameraBlkng"])
                table_KameraBlkng.append_row([nomor, row["Type"], row["KameraBlkng"], rendah, menengah, tinggi])
                nomor = nomor + 1



        return render_template('belakang.html', table=table_KameraBlkng)

    except Exception as e:
        # Log or print the error for debugging
        print(f"Error: {e}")

@app.route('/rekomendbelakang')
def rekomendbelakang():
    try:
        with connection.cursor() as sql:
            sql.execute("SELECT Type,KameraBlkng FROM DataHP")
            fetched_rows = sql.fetchall()

            # Perform fuzzy logic predictions for Baterai
            table_kamera_bagus = BeautifulTable()
            table_kamera_bagus.column_headers = ["No", "Type", "KameraBlkng", "Rekomendasi"]

            nomor = 1
            for row in fetched_rows:
                rendah, menengah, tinggi = predict_KameraBlkng(row["KameraBlkng"])

                table_kamera_bagus.append_row([nomor, row["Type"], row["KameraBlkng"], max(rendah, menengah, tinggi)])
                nomor = nomor + 1



        return render_template('rekomenbelakang.html', table=table_kamera_bagus)

    except Exception as e:
        # Log or print the error for debugging
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
