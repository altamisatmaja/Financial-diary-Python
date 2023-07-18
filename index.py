import csv
import os
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt
from prettytable import PrettyTable
    
print(f"\n{'SELAMAT DATANG DI FINANZE':^50}")
print(f"{'APLIKASI PENCATATAN KEUANGAN PRIBADI':^50}")
print(f"\n{50*'='}\n")

database_finanze = 'database_finanze.csv'

def database():
    with open('database_finanze.csv', 'r') as file:
        baca_database = csv.reader(file)
        jadi_tabel = tabulate(baca_database, headers="firstrow", tablefmt="grid")
        print(jadi_tabel)
        
def input_pemasukan():
    pemasukan = {}
    pemasukan['Pemasukkan'] = int(input("Masukkan jumlah pemasukan: ").replace(".", ""))
    pemasukan['tanggal'] = input("Masukkan tanggal pemasukan (DD/MM/YYYY): ")
    pemasukan['kategori'] = input("Masukkan kategori pemasukan: ")

    saldo_terakhir = hitung_saldo()
    saldo_baru = saldo_terakhir + pemasukan['Pemasukkan']

    with open('database_finanze.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pemasukan['tanggal'], pemasukan['kategori'], pemasukan['Pemasukkan'], 0, saldo_baru])

    print("\nPemasukan berhasil ditambahkan!")
    print(f"\n{50*'='}\n")
    
    
def input_pengeluaran():
    pengeluaran = {}
    pengeluaran['Pengeluaran'] = int(input("\nMasukkan jumlah pengeluaran: ").replace(".", ""))
    pengeluaran['tanggal'] = input("Masukkan tanggal pengeluaran (DD/MM/YYYY): ")
    pengeluaran['kategori'] = input("Masukkan kategori pengeluaran: ")

    saldo_terakhir = hitung_saldo()
    saldo_baru = saldo_terakhir - pengeluaran['Pengeluaran']
    
    with open('database_finanze.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pengeluaran['tanggal'], pengeluaran['kategori'], 0, pengeluaran['Pengeluaran'], saldo_baru])

    print("\nPengeluaran berhasil ditambahkan!")
    print(f"\n{50*'='}\n")
    
def input_saldo():
    saldo = {}
    saldo['Saldo'] = int(input("\nMasukkan jumlah saldo: ").replace(".", ""))
    saldo['tanggal'] = input("Masukkan tanggal saldo (DD/MM/YYYY): ")
    saldo['kategori'] = input("Masukkan kategori saldo: ")
    
    saldo_terakhir = hitung_saldo()
    saldo_baru = saldo_terakhir + saldo['Saldo']
    
    with open('database_finanze.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saldo['tanggal'], saldo['kategori'], 0, saldo['Saldo'], saldo_baru])

    print("\nSaldo berhasil ditambahkan!")
    print("========================")
    
def hitung_saldo():
    saldo = 0
    with open('database_finanze.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) == 5:
                pemasukkan = int(row[2])
                pengeluaran = int(row[3])
                saldo += pemasukkan - pengeluaran
    return saldo

def update_data(data, update_file):
    with open(update_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) 

        update_data(data, csv_reader)

def update_data(data, csv_reader):
    baris = next(csv_reader)
    update_baris(data, baris)
    update_data(data, csv_reader)

def update_baris(data, update_baris):
    tanggal = update_baris[0]
    kategori = update_baris[1]
    pemasukkan = int(update_baris[2])
    pengeluaran = int(update_baris[3])

    update_baris(data, tanggal, kategori, pemasukkan, pengeluaran)

def update_baris(data, tanggal, kategori, pemasukkan, pengeluaran, index=0):
    if index >= len(data):
        return

    baris = data[index]
    if baris['Tanggal'] == tanggal and baris['Kategori'] == kategori:
        baris['Pemasukkan'] = pemasukkan
        baris['Pengeluaran'] = pengeluaran

    update_baris(data, tanggal, kategori, pemasukkan, pengeluaran, index + 1)

    menghitung_saldo(data)

def menghitung_saldo(data):
    saldo_sebelumnya = 0
    for baris in data:
        pemasukkan = int(baris['Pemasukkan'])
        pengeluaran = int(baris['Pengeluaran'])
        saldo_terbaru = saldo_sebelumnya + pemasukkan - pengeluaran
        baris['Saldo'] = saldo_terbaru
        saldo_sebelumnya = saldo_terbaru

def read_data(database_finanze):
    with open(database_finanze.csv, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data

def write_data(data, database_finanze):
    array_template = ['Tanggal', 'Kategori', 'Pemasukkan', 'Pengeluaran', 'Saldo']
    with open(database_finanze, 'w', newline='') as file:
        writer = csv.DictWriter(file, array_template=array_template)
        writer.writeheader()
        writer.writerows(data)

def read_data(database_finanze):
    with open(database_finanze, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data

def write_data(data, database_finanze):
    array_template = ['Tanggal', 'Kategori', 'Pemasukkan', 'Pengeluaran', 'Saldo']
    with open(database_finanze, 'w', newline='') as file:
        writer = csv.DictWriter(file, array_template=array_template)
        writer.writeheader()
        writer.writerows(data)

def menghapus_berdasarkan_kategori(file_path, date, kategori, kolom_target):
    updated_rows = []

    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        updated_rows.append(headers)

        for row in reader:
            if len(row) > kolom_target and row[0] != "Tanggal" and row[0] != date and row[kolom_target].lower() != kategori.lower():
                updated_rows.append(row)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    print("Data telah dihapus dari file CSV.")

def cari_indeks(arr, target, batas_bawah, batas_atas):
    # menerima argumen arr (array),
    # target (nilai yang dicari),
    # batas_bawah (indeks bawah),
    # dan batas_atas (indeks atas)
    # mengimplementasikan algoritma binary search untuk mencari indeks dari target dalam array arr
    while batas_bawah <= batas_atas:
        # pencarian akan terus berlanjut selama batas_bawah tidak melebihi batas_atas
        tengah = (batas_bawah + batas_atas) // 2
        # menghitung indeks tengah sebagai pembulatan ke bawah hasil penjumlahan batas_bawah dan batas_atas dibagi dua
        if arr[tengah] == target:
            # memeriksa apakah nilai pada arr[tengah] sama dengan target
            # jika iya, berarti kita telah menemukan indeks yang mengandung target,
            # sehingga langsung mengembalikan tengah
            return tengah
        elif arr[tengah] < target:
            # maka perlu dilakukan pencarian di setengah bagian kanan dari array
            # oleh karena itu, batas_bawah diperbarui menjadi tengah + 1 untuk menggeser
            # rentang pencarian ke bagian kanan array
            batas_bawah = tengah + 1
        else:
            batas_atas = tengah - 1
            # batas_atas diperbarui menjadi tengah - 1 untuk
            # menggeser rentang pencarian ke bagian kiri array
    # jika tidak ada indeks yang ditemukan yang mengandung target dalam rentang pencarian,
    # maka loop akan terus berlanjut hingga batas_bawah melampaui batas_atas
    # pada saat itu, akan dikembalikan nilai -1 untuk menunjukkan bahwa target tidak ditemukan dalam array
    return -1

def cari_transaksi(transaksi, tanggal):
    tanggal_transaksi = [data[0] for data in transaksi]
    indeks = cari_indeks(tanggal_transaksi, tanggal, 0, len(tanggal_transaksi) - 1)
    if indeks != -1:
        return transaksi[indeks]
    else:
        return None

def cari_transaksi_berdasarkan_tanggal(transaksi):
    tanggal = input("Masukkan tanggal transaksi yang ingin dicari (DD/MM/YYYY): ")
    transaksi_ditemukan = cari_transaksi(transaksi, tanggal)
    if transaksi_ditemukan:
        print("Transaksi ditemukan:")
        print("Tanggal: ", transaksi_ditemukan[0])
        print("Pemasukan: ", transaksi_ditemukan[1])
        print("Pengeluaran: ", transaksi_ditemukan[2])
    else:
        print("Transaksi tidak ditemukan.")
    
def tampilkan_finanze():
    finanze = []
    with open('database_finanze.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Mengabaikan header
        for row in reader:
            report = {
                'date': row[0],
                'kategori': row[1],
                'income': int(row[2]),
                'expense': int(row[3]),
                'balance': float(row[4])
            }
            finanze.append(report)
    return finanze

def fitur_bubble_sort(finanze):
    n = len(finanze)
    # inisialisasi nilai
    for i in range(n - 1):
        # melakukan iterasi sebanyak n-1
        for j in range(n - 1 - i):
            # membandingkan dan menukar posisi dua elemen yang berdekatan
            # jika ditemukan bahwa elemen sebelumnya lebih besar dari elemen berikutnya
            if finanze[j]['date'] > finanze[j + 1]['date']:
                # jika tanggal pada finanze[j] lebih besar dari tanggal pada finanze[j + 1],
                # selanjutnya pertukaran posisi elemen
                finanze[j], finanze[j + 1] = finanze[j + 1], finanze[j]


def main():
    
    while True:
        print(f"\n{'MAIN MENU':^50}\n")
        print("1. Fitur Input")
        print("2. Fitur Read")
        print("3. Fitur Update")
        print("4. Fitur Delete")
        print("5. Fitur Search")
        print("6. Fitur Rekapitulasi")
        print("7. Fitur Sorting")
            
        pilihan_user = input("\nMasukkan opsi untuk menggunakan fitur: ")

        if pilihan_user == '1':
            while True:
                print("1. Input Pemasukan")
                print("2. Input Pengeluaran")
                print("3. Cek Saldo")
                print("0. Keluar")
                choice = input("\nMasukkan pilihan: ")

                if choice == '1':
                    input_pemasukan()
                elif choice == '2':
                    input_pengeluaran()
                elif choice == '3':
                    saldo = hitung_saldo()
                    print("\nSaldo saat ini: {}".format(saldo))
                    print("========================")
                elif choice != '1' and choice != '2' and choice != '3':
                    break
            
                tanya_ke_user = input("Apakah mau menambahkan inputan? (y/n):  ")
                if tanya_ke_user == "n" or tanya_ke_user == "N":
                    break
                
        elif pilihan_user == '2':
                finanze = tampilkan_finanze()
                fitur_bubble_sort(finanze)
                table = PrettyTable()
                table.field_names = ["Tanggal", "Kategori", "Pemasukkan", "Pengeluaran", "Saldo"]
                for report in finanze:
                    table.add_row([report['date'], report['kategori'], report['income'], report['expense'], report['balance']])
                print(table)
                    
        elif pilihan_user == '3':
            data = read_data('database_finanze.csv')

            tanggal = input("Masukkan tanggal data yang ingin diubah: ")
            kategori = input("Masukkan kategori data yang ingin diubah: ")

            cari_data = [baris for baris in data if baris['Tanggal'] == tanggal and baris['Kategori'] == kategori]
            print("1. Edit pemasukkan")
            print("2. Edit pengeluaran")
            menu = input("Pilih menu: ")

            if menu == "1":
                pemasukkan = int(input("Masukkan pemasukkan baru: "))
                pengeluaran = cari_data[0]['Pengeluaran']

            elif menu == "2":
                pemasukkan = cari_data[0]['Pemasukkan']
                pengeluaran = int(input("Masukkan pengeluaran baru: "))

            else:
                print("Menu tidak valid.")
                exit()

            for baris in cari_data:
                baris['Pemasukkan'] = pemasukkan
                baris['Pengeluaran'] = pengeluaran

    
            if cari_data[-1] != data[-1]:
                menghitung_saldo(data)
                
            write_data(data, 'database_finanze.csv')
            print("Data berhasil diupdate.")
            
        elif pilihan_user == '4':
            print("Data awal:")
            with open(database_finanze, 'r') as file:
                reader = csv.reader(file)
                table = tabulate(reader, headers="firstrow", tablefmt="grid")
                print(table)

            while True:
                print("\n=== Aplikasi Finanze ===")
                print("1. Delete from Data Pemasukan")
                print("2. Delete from Data Pengeluaran")
                print("3. Delete from Data Saldo")
                print("0. Keluar")
                choice = input("\nMasukkan pilihan: ")

                if choice == '0':
                    break

                if choice in ['1', '2', '3']:
                    date_to_delete = input("Masukkan tanggal data yang akan dihapus (DD/MM/YYYY): ")
                    kategori_to_delete = input("Masukkan kategori data yang akan dihapus: ")

                    if choice == '1':
                        menghapus_berdasarkan_kategori(database_finanze, date_to_delete, kategori_to_delete, 2)  # Kolom Pemasukkan
                    elif choice == '2':
                        menghapus_berdasarkan_kategori(database_finanze, date_to_delete, kategori_to_delete, 3)  # Kolom Pengeluaran
                    elif choice == '3':
                        menghapus_berdasarkan_kategori(database_finanze, date_to_delete, kategori_to_delete, 4)  # Kolom Saldo
                    else:
                        print("Pilihan tidak valid.")


                    print("\nData setelah penghapusan:")
                    with open(database_finanze, 'r') as file:
                        reader = csv.reader(file)
                        table = tabulate(reader, headers="firstrow", tablefmt="grid")
                        print(table)
                else:
                    print("Pilihan tidak valid.")
            
        elif pilihan_user == '5':
            if __name__ == '__main__':
                with open('database_finanze.csv', 'r') as file:
                    reader = csv.reader(file)
                    transaksi = list(reader)

                transaksi.sort(key=lambda x: x[0])
                # digunakan untuk mengurutkan elemen-elemen dalam daftar transaksi berdasarkan kunci yang ditentukan

                # mengambil argumen x yang mewakili setiap elemen dalam daftar transaksi dan mengembalikan nilai x[0]
                # di sini, x[0] merujuk pada elemen pertama dalam setiap elemen dalam daftar transaksi

                cari_transaksi_berdasarkan_tanggal(transaksi)
            
        elif pilihan_user == '6':

            kategori = []
            pengeluaran = []

            with open('database_finanze.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    kategori.append(row[1])
                    pengeluaran.append(float(row[3]))

            colors = ['red', 'blue', 'green', 'yellow', 'orange']


            fig = plt.figure(figsize=(4, 4)) 
            plt.pie(pengeluaran, labels=kategori, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.gca().set_title('Rekapitulasi Keuangan')
            plt.axis('equal')
            plt.show()
            
        elif pilihan_user == '7':
            finanze = tampilkan_finanze()
            fitur_bubble_sort(finanze)
            table = PrettyTable()
            table.field_names = ["Tanggal", "Kategori", "Pemasukkan", "Pengeluaran", "Saldo"]

            for report in finanze:
                table.add_row([report['date'], report['kategori'], report['income'], report['expense'], report['balance']])

            # Menampilkan tabel
            print(table)
            
        else:
            tanya_ke_user = input("Serius ingin keluar dari program ini? (y/n):  ")
            if tanya_ke_user == "y" or tanya_ke_user == "Y":
                break

    print(f"\n{50*'='}\n")

    print("Terima kasih telah menggunakan Finanze!")

if __name__ == '__main__':
    main()