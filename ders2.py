import psycopg2
from psycopg2 import sql, extensions
import sys


connection = psycopg2.connect(
   user = "postgres",
   password = "onat123",
   host = "localhost",
   port = "5432",
   database = "kitap"
)

cursor = connection.cursor()
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(autocommit)

# veri tabanını oluşturacağımız fonksiyonu yazalım

def createDB(dbname):
   try:
      global connection
      global cursor
      createDB = "CREATE DATABASE " + dbname
      cursor.execute(createDB)
      connection.commit()
      print("== Veri tabani baglantisi basariyla olusturuldu ==")
   except(Exception,psycopg2.Error) as error:
      print("== Baglanti hatasi : {} ==".format(error))
      connection = None
   finally:
      # baglanti yoksa olustursun varsa kapasin islemleri
      if connection != None:
         cursor.close()
         connection.close()
         print("== Postgresql veri tabani suanda kapatilmistir ==")
         
# veri tabanını oluşturduk şimdi sıra tablo da
def createTable():
   try:
      global connection
      global cursor 
      create_table = "CREATE TABLE book (id INTEGER PRIMARY KEY, author VARCHAR(120), isbn VARCHAR(120), title VARCHAR(120), date_published DATE)"
      cursor.execute(create_table)
      print("== Veri tabani baglantisi basariyla olusturuldu ==")      
   except(Exception, psycopg2.Error) as error:
      print("== Baglanti hatasi : {} ==".format(error))
      connection = None
   finally:
      # baglanti yoksa olustursun varsa kapasin islemleri
      if connection != None:
         cursor.close()
         connection.close()
         print("== Postgresql veri tabani suanda kapatilmistir ==")
         
# şimdi sıra verileri eklemekte
# bunun için oluşturduğumuz fonksiyonu kullanıcıdan bilgiler oluşturacak şekilde yapalım
def insertTable(id, author, isbn, title, date_published):
   try:
      global connection
      global cursor
      insert_table = "INSERT INTO book (id, author, isbn, title, date_published) VALUES (%s,%s,%s,%s,%s)"
      insterted_values = (id, author, isbn, title, date_published)
      cursor.execute(insert_table, insterted_values)
      # Kaç satırlık işlem yaptığımızı count değişkeniyle saydırtabiliriz
      count = cursor.rowcount
      print("=='{}'tane kayit tabloya eklenmistir.==".format(count))      
   except(Exception, psycopg2.Error) as error:
      print("== Baglanti hatasi : {} ==".format(error))
      connection = None
   finally:
      # baglanti yoksa olustursun varsa kapasin islemleri
      if connection != None:
         cursor.close()
         connection.close()
         print("== Postgresql veri tabani suanda kapatilmistir ==")

# Satırları görmek için sürekli veritabanı uygulamasından bakmak yerine buradan bakalım
def selectTable():
   try:
      global connection
      global cursor
      selectQuery = "SELECT * FROM book"
      cursor.execute(selectQuery)
      # bir for döngüsüne alabilmek için fetchall yaparız
      books = cursor.fetchall()
      for kitaplar in books:
         print(kitaplar)
      # eğer kaç kayıt olduğunu görmek istiyorsak yine count isimli bir değişken yapabiliriz
      count = cursor.rowcount
      print("== Tablo da toplam {} kayit bulunmaktadir.==".format(count))      
      
   except(Exception, psycopg2.Error) as error:
      print("== Baglanti hatasi : {} ==".format(error))
      connection = None
   finally:
      # baglanti yoksa olustursun varsa kapasin islemleri
      if connection != None:
         cursor.close()
         connection.close()
         print("== Postgresql veri tabani suanda kapatilmistir ==")

# şimdi de update kısımlarını yapalım
def updateTable(bookid, title):
   try:
      global connection
      global cursor
      updateQuery = "UPDATE book SET title= %s WHERE id=%s "
      # %s lere gönderilecek verilerle ilgili kod parçacığı aşşağıda ki satırda bulunmakta
      cursor.execute(updateQuery, (title,bookid))
      count = cursor.rowcount
      print("=='{}' tane kayit basariyla guncellendi ==".format(count))
      
   except(Exception, psycopg2.Error) as error:
      print("== Baglanti hatasi : {} ==".format(error))
      connection = None
   finally:
      # baglanti yoksa olustursun varsa kapasin islemleri
      if connection != None:
         cursor.close()
         connection.close()
         print("== Postgresql veri tabani suanda kapatilmistir ==")

# Şimdi de delete table için yapalım
def deleteTable(bookid):
   try:
      global connection
      global cursor
      deleteQuery = "DELETE FROM book WHERE id = {}".format(bookid) # burda yapılan işlem aslında %s ile aynıdır, 
                                                                    # sadece bir alternatif olduğunu göstermek için konmuştur
      # %s lere gönderilecek verilerle ilgili kod parçacığı aşşağıda ki satırda bulunmakta
      cursor.execute(deleteQuery)
      count = cursor.rowcount
      print("=='{}' tane kayit basariyla silinmistir ==".format(count))
   except(Exception, psycopg2.Error) as error:
      print("== Baglanti hatasi : {}==".format(error))
      connection = None
   finally:
      # baglanti yoksa olustursun varsa kapasin islemleri
      if connection != None:
         cursor.close()
         connection.close()
         print("== Postgresql veri tabani suanda kapatilmistir ==")

def menu():
   print("""
         =============================
         Seciminizi yapiniz.
         1-Tum kayitlari listele
         2-Yeni kayit ekle
         3-Kayit guncelleme
         4-Kayit silme
         5-Cikis
         """)

# main fonksiyonumuza önce bir menü gelicek ve
# bu menüleri sonsuz döngüye koyucaz
def main():
   while True: #while 1
      menu()
      secim = input("== Lutfen seciminizi yapiniz: ")
      if secim == "1":
         selectTable()
      elif secim == "2":
         id = input("ID: ")
         author = input("AUTHOR: ")
         isbn = input("ISBN: ")
         title = input("TITLE: ")
         date_published = input("DATE: ")
         insertTable(id,author,isbn,title,date_published)
      elif secim == "3":
         id = input("ID: ")
         title = input("TITLE: ")
         updateTable(id,title)
      elif secim == "4":
         id = input("ID: ")
         deleteTable(id)
      elif secim == "5":
         sys.exit() 
      else:
         print("== Yanlis bir islem yaptiniz.==")
         
if __name__ == "__main__":
   createDB("kitap")  
   createTable()    
   main()