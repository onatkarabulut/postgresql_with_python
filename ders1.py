#-Postgresql veri tabani bağlantisi 
#   - Python'a kütüphane ekleme
#   - Veri tabani oluşturma
#      - Tablo olusturma
#     - Veri girisi
#   - SQL bağlanti cümleleri
#      - Yeni kayit ekle
#      - Kayit sil 
#      - Kayit ara
#      - Kayit güncelle
#      - Kayit listeleme


#   !pip install psycopg2

import psycopg2 as ps

# Bu bilgilere erismek icin PostgreSQL 12 sağ tık > properties
database_name = "postgres"
user_name = "postgres"
password = "onat123"
host_ip = "localhost" # 127.0.0.1
host_port = "5432"
 
baglanti = ps.connect(database = database_name,
                      user = user_name,
                      password = password,
                      host = host_ip,
                      port = host_port) 

baglanti.autocommit = True  # Veritabanlarında commitleme/execute 
                            # etmesini açık yapıyoruz

cursor = baglanti.cursor() # satırsal olarak yazdığımız 
                           # sql kodlarını kabul ediyor
                           # sql cümlemizi yönlendirmeye yarıyor
                           # select * from vs vs 
                           
# our_query = "CREATE DATABASE car_db"
# cursor.execute(query=our_query)
cursor.execute("CREATE DATABASE IF NOT EXISTS car_db")


# şimdi nasıl bağlantı yapacağımızı gördük, oluşturduğumuz veritabanına bağlanalım
database_name = "car_db"
baglanti = ps.connect(database = database_name,
                      user = user_name,
                      password = password,
                      host = host_ip,
                      port = host_port )

query_create_table = """
CREATE TABLE IF NOT EXISTS cars(
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
model INTEGER,
number TEXT,
color TEXT,
company TEXT  
)
"""
baglanti.autocommit = True
cursor = baglanti.cursor()
cursor .execute(query_create_table)


#                 INSERT
# insert işlemi için liste oluşturulmalıdır
# o listeyi de bir döngüyle gönderebiliyoruz

# kullanım-1

# query_insert = ( #type:ignore
#    f"INSERT INTO cars (name, model, number, color, company)  
#    VALUES
#    ("Aqua", 2009, "ABC123", "Red", "Toyota"),
#    ("700s", 2015, "XXX22", "Black", "Bmw" ),
#    ("Vezel", 2018, "XXX111", "White", "Honda"),
#    ("200C", 2001, "MMMM11", "Black", "Mercedes"),
#    ("Vitz", 2010, "XXXX", "Red", "Toyata")
#    )")


# kullanım-2 
# tamamen liste oluşturarak yaparız

cars = [
   ("Aqua", 2009, "ABC123", "Red", "Toyota"),
   ("700s", 2015, "XXX22", "Black", "Bmw" ),
   ("Vezel", 2018, "XXX111", "White", "Honda"),
   ("200C", 2001, "MMMM11", "Black", "Mercedes"),
   ("Vitz", 2010, "XXXX", "Red", "Toyata"),
]

# listeyi oluşturduk, peki nasıl yönlendiririz?
car_record = ", ".join(["%s"] * len(cars))
# listenin uzunluğuna göre listeye eklemeyi virgülden sonra eklicek

query_insert = (
   f"INSERT INTO cars(name,model,number,color,company) \
   VALUES {car_record}")

cursor.execute(query_insert, cars) # inserti çalıştırdık ve carsı da eklemeyi unutmadık


#           READ - SELECT
query_select = "SELECT * FROM cars"
cursor.execute(query_select)
# bu listeyi yakalayıp bastırmamız gerekiyor
# bu sonuçları yakalayabilmek için de fetchall() kullanırız
cars = cursor.fetchall() # yani bu şekilde satır kayıt değişkenlerini yakalarız
for car in cars:
   print(car)
   
   
   
   
#           UPDATE
# bu işlemi yapabilmek için önce cümleyi alırız ve execute yaparız
query_update = """
UPDATE cars
SET color = 'Blue'
WHERE model >= 2010
"""# modeli 2010dan büyük olanların rengini mavi olarak değiştirdik

cursor.execute(query_update)




#             DELETE
query_delete = "DELETE FROM cars WHERE color = 'Red'"
cursor.execute(query_delete)