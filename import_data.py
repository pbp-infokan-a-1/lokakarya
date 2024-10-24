import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lokakarya.settings")
django.setup()

from storepage.models import Toko

data_toko = [
    {
        "nama": "Mahaeswari Jepara Craft",
        "hari_buka": "Senin-Jumat",
        "alamat": "Jl. Kemuning Raya, Rw. IV, Krapyak, Kec. Jepara, Kabupaten Jepara, Jawa Tengah 59421",
        "email": "mahaeswara.jepara@gmail.com",
        "telepon": "0856-2975-929"
    },
    {
        "nama": "Griya Parcel Mahar Jepara",
        "hari_buka": "Senin-Sabtu",
        "alamat": "Jl.panenan RT 3 RW 3 Samping balaidesa depan makam duren mas 5 menit dari pasar Pecangaan, Rw. 2, Pecangaan Wetan, Kec. Pecangaan, Kabupaten Jepara, Jawa Tengah 59462",
        "email": "griyaparcel@gmail.com",
        "telepon": "0821-3376-0316"
    },
    {
        "nama": "Batik Zara Pasar Ratu",
        "hari_buka": "Senin-Jumat",
        "alamat": "Pasar Jepara 1, Jl. Untung Suropati Lantai 1 Blok E Zona B No. D5, Jobokuto I, Jobokuto, Jepara, Jepara Regency, Central Java 59416",
        "email": "batikzara@gmail.com",
        "telepon": "0813-9275-4422"
    },
    {
        "nama": "Mustika Kayu Jati Jepara Furniture",
        "hari_buka": "Senin-Minggu",
        "alamat": "Jl. Raya Grogol, RT.6/RW.1, Grogol, Kec. Limo, Kota Depok, Jawa Barat 16512",
        "email": "mustikajati@gmail.com",
        "telepon": "0877-8642-2278"
    },
    {
        "nama": "Jepara Art Furnicraft",
        "hari_buka": "Senin-Jumat",
        "alamat": "Jl. Cik Lanang No.25, RT.15/RW.5, Jobokuto III, Jobokuto, Kec. Jepara, Kabupaten Jepara, Jawa Tengah 59416",
        "email": "furnicraft@gmail.com",
        "telepon": "0823-2330-3666"
    },
    {
        "nama": "Toko Mede Keramik",
        "hari_buka": "Senin-Minggu",
        "alamat": "Bawu I, Bawu, Kec. Batealit, Kabupaten Jepara, Jawa Tengah 59461",
        "email": "medekeramik@gmail.com",
        "telepon": "0895-9923-1342"
    },
    {
        "nama": "Pengrajin Tenun Unsiyyah",
        "hari_buka": "Senin-Sabtu",
        "alamat": "Pecangakan, Central Java, Segaran Jepara, Jepara, Jawa Tengah 59462",
        "email": "tenununsiyyah@gmail.com",
        "telepon": "0852-2644-4425"
    },
    {
        "nama": "Nambya Tenun",
        "hari_buka": "Senin-Sabtu",
        "alamat": "RT.01/RW.01, Rw. 1, Troso, Kec. Pecangaan, Kabupaten Jepara, Jawa Tengah 59462",
        "email": "nambya@gmail.com",
        "telepon": "0895-3618-62203"
    },
    {
        "nama": "Gallery Tenun Store",
        "hari_buka": "Senin-Sabtu",
        "alamat": "Jl. Bougenvil Raya No.18, Mulyoharjo II, Mulyoharjo, Kec. Jepara, Kabupaten Jepara, Jawa Tengah 59415",
        "email": "tenungallery@gmail.com",
        "telepon": "0812-1599-6938"
    },
    {
        "nama": "Jepara Shellcraft",
        "hari_buka": "Senin-Jumat",
        "alamat": "Gamong, Kec. Kaliwungu, Kabupaten Kudus, Jawa Tengah 59332",
        "email": "jeparacraft@gmail.com",
        "telepon": "0812-8023-0669"
    },
    {
        "nama": "Toko Adhesi Monel",
        "hari_buka": "Senin-Minggu",
        "alamat": "Jl. Raya Krasak No.154, Rw. 03, Krasak, Kec. Pecangaan, Kabupaten Jepara, Jawa Tengah 59462",
        "email": "moneladhesi@gmail.com",
        "telepon": "0891-7223-1987"
    },
    {
        "nama": "Seni Sakti Monel",
        "hari_buka": "Senin-Minggu",
        "alamat": "Jl. Gua Kencana No.43, RT.07/RW.02, Rw. I, Kriyan, Kec. Kalinyamatan, Kabupaten Jepara, Jawa Tengah 59467",
        "email": "senisakti@gmail.com",
        "telepon": "0812-2633-339"
    }   
]

def import_data():
    for toko in data_toko:
        Toko.objects.create(
            nama=toko["nama"],
            hari_buka=toko["hari_buka"],
            alamat=toko["alamat"],
            email=toko["email"],
            telepon=toko["telepon"]
        )
    print("Data berhasil diimpor!")

if __name__ == "__main__":
    import_data()