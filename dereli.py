# -*- coding: utf-8 -*-

""":arg
Bu kodların yazım aşamasında bana çok katkısı bulunan @Z3R0D0WN'a çok teşekkür ederim.
"""

import os
import json
import random
import socket
import requests
import datetime
import threading
from tkinter import *
from tkinter import Tk
from bs4 import BeautifulSoup
from tkinter import ttk, messagebox

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")



class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title('DERELI v.1') #pencere başlığı
        """enini boyunu, pencere konumu (nerde dursun açıldığında)
        1366x768 dünya çapında en çok kullanılan genişlik ve yükseklik"""
        self.geometry('1366x768+150+150')
        #self.resizable(FALSE, FALSE) #pencere büyültme ve küçültme yasağı
        self.URL_LIST = set() # Bütün URL'ler burda toplanıyor
        self.DIRECTORY_2 = set()
        self.TOTAL_URL = set()
        URL_LIST = list(self.URL_LIST)
        self.NOT_CONTENT_URL_LIST = set()  # farklı domain'e ait siteleri tutar
        self.USERAGENT = [agent.strip() for agent in open('src/useragent.txt')]
        self.Random_Useragent = random.choice(self.USERAGENT) # İstek yaparken kullanılacak rastgele bir useragent
        self.a = 1 #hedef kutusuna kayıt ederken sütun sırası



    def Request(self):

        if self.hedef_veriyi_al.get(): # Butondan gelen taranacak siteyi burada alıyoruz
            self.host = str(self.hedef_veriyi_al.get())

        else:
            messagebox.showinfo("Uyarı", "Lütfen taranacak bir site giriniz !") #eğer veri yoksa uyarı veriyoruz

        self.req = requests.get(self.host)  # Siteye GET isteği yapılmıştır
        self.req_content = self.req.content  # Sitenin kaynak bilgisi
        self.req_headers = self.req.headers  # Sitenin Headers bilgisi
        self.req_status_code = self.req.status_code  # Sitenin durum kodu (200,301 vs.)
        self.req_history = self.req.history  # Sitedeki yönlendirmeleri gösteriyor
        self.req_text = self.req.text  # Düzenli bir şekilde kaynak kodu
        self.req_method = self.req.raw
        #for value,keys in self.req_headers.items():
        #   self.text1.insert(END, str(value)+": "+str(keys) +"\n")



    def Host_Look(self):
        # Düzenli gözükmesi için verilen site url'sini,  split işlemine sokarak temiz bir host elde ediyoruz.
        self.host_strip = self.host.split("://")[1]



    def Ip_Look(self):

        # Verdiğimiz sitenin ip bilgisini veriyor
        self.host_ip = socket.gethostbyname(self.host_strip)

        #if self.host_ip:
        #    self.label_ip_text.insert(END, str(self.host_ip))
        #else:
        #    self.label_ip_text.insert(END, "İp bulunamadı...")



    def Host_Strip_www(self):

        if 'www' in self.host_strip:

            self.host_strip_control = str(self.host_strip).split('www.')[1]

        else:

            self.host_strip_control = str(self.host_strip)


    def cikis(self):

        if messagebox.askokcancel("Çıkış", "Çıkmak istediğinize emin misiniz?"):

            w.destroy()



    def ikinci_bolum_func(self,evt):

        self.secili_eleman = self.birinci_bolum.focus() #sütun bilgilerini aldık
        self.secili_eleman_bilgi = self.birinci_bolum.item(self.secili_eleman, "text")
        #sütun bilgileri içinden No kısmını alıyoruz

        self.ikinci_bolum_baslik1_text.delete('1.0', END)
        self.ikinci_bolum_baslik2_text.delete('1.0', END)

        try: # Response bölümüne HEADERS yazdırdık

            for key, value in self.req_istek.headers.items():

                """if "application/json" in value:
                    self.ikinci_bolum_baslik3_text.insert(END, json.dumps(self.req_istek.text))
                else:
                    pass"""

                self.ikinci_bolum_baslik1_text.insert(END, str(key) + ": " + str(value) + "\n")


                self.ikinci_bolum_baslik2_text.insert(END, str(key) + ": " + str(value) + "\n")

        except:

            pass

        try: # Response bölümüne kaynak kodlaırnı yazdırdık

            self.ikinci_bolum_baslik2_text.insert(END, '\n\n')
            #self.ikinci_bolum_baslik2_text.insert(INSERT, self.req_istek.content)

            # kaynak kod çok büyük olduğu için yorum satırına aldım.
            #

        except:
            self.ikinci_bolum_baslik2_text.insert(END, '\n\n')
            #self.ikinci_bolum_baslik2_text.insert(INSERT, self.req_istek.content)






        #self.ikinci_bolum_func_dosya_okuma_json = json.load(self.ikinci_bolum_func_dosya_okuma)
        #self.ikinci_bolum_baslik1_text.insert(INSERT, self.ikinci_bolum_func_dosya_okuma.read().encode("'utf-8"))


    def callback(self,evt):
        secili_eleman = self.birinci_bolum.focus()
        secili_eleman_bilgi = self.birinci_bolum.item(secili_eleman)
        self.ikinci_bolum_baslik1_text.delete('1.0', END) 
        self.ikinci_bolum_baslik1_text.insert(INSERT, secili_eleman_bilgi)

    def govde(self):

        self.secenekler = ttk.Notebook(self) #sekmeler halinde pencere özelliği sunar
        #Daha iyi anlamak için: Tarayıcı sekmeleri gibi
        #her sekmede ayrı işlemler yapabiliyoruz bu sayede çok işlevli programlar oluşturabiliyoruz

        self.hedef = Frame(self.secenekler)
        self.secenekler.add(self.hedef, text="Hedef") #Hedef sekmemizi tanımladık

        # -------------------------------------- HEDEF BÖLÜMÜ --------------------------------------
        self.hedef_baslik = Label(  #Label metin veya resim ekleyeceğimiz zaman kullanıyoruz
            self.hedef,
            text="Site: ", #Label'ın yazısı
            font=('open sans', 15, "bold") #yazı tipi, boyutu ve  kalın mı olucak italic mi gibi
        )

        self.hedef_veriyi_al = Entry( # Burda bir veri girmesini istiyoruz kullanıcıdan
            self.hedef,
        )

        self.hedef_buton = Button(
            self.hedef,
            text="Tara", #Buton yazısı
            # Buton'a basıldığında çalışacak fonskiyonlar
            command=lambda: [self.Request(), self.Host_Look(), self.Ip_Look(),
                             self.Host_Strip_www(), self.Url_Crawler_SECTION_1(),
                            ]
        )
		
        self.birinci_bolum = ttk.Treeview(self.hedef) #Treeview bize bir şema sunar.
        #Bu şema sayesinde programımızı ağaçlandırma şeklinde kategoriye ayırabiliyoruz.
        #self.birinci_bolum.bind('<<ListboxSelect>>, <button-1>', self.callback) #bing özelliği bir event tanımlamamıza
        self.birinci_bolum.bind('<<TreeviewSelect>>', self.callback) #bing özelliği bir event tanımlamamıza
        #yardımcı oluyor <button-1> ise sol click özelliğidir
        self.birinci_bolum.bind('<<TreeviewSelect>>', self.ikinci_bolum_func)

        self.birinci_bolum["columns"] = ("sifir","bir", "iki", "uc", "dort", "bes") #sekmelerimizi burda oluşturduk
        self.birinci_bolum.column("#0", width=5, minwidth=10, anchor="center")
        self.birinci_bolum.column("sifir", width=30, minwidth=70, anchor="center")
        self.birinci_bolum.column("bir", width=10, minwidth=30, anchor="center")
        self.birinci_bolum.column("iki", width=200, minwidth=100, anchor="center")
        self.birinci_bolum.column("uc", width=15, minwidth=15, anchor="center")  # stretch=tk.NO boyutu değiştirememe özelliği
        self.birinci_bolum.column("dort", width=5, minwidth=140, anchor="center")
        self.birinci_bolum.column("bes", width=15, minwidth=15, anchor="center")

        self.birinci_bolum.heading("#0", text="No", anchor='center')
        self.birinci_bolum.heading("sifir", text="Host", anchor='center')
        self.birinci_bolum.heading("bir", text="Method", anchor='center')
        self.birinci_bolum.heading("iki", text="URL", anchor='center')
        self.birinci_bolum.heading("uc", text="Status", anchor='center')
        self.birinci_bolum.heading("dort", text="Lenght", anchor='center')
        self.birinci_bolum.heading("bes", text="MIME type", anchor='center')


#------------------- Hedef bölümündeki cevap kısmı ----------------------

        self.ikinci_bolum = ttk.Notebook(self.hedef) #bu sefer ana bölüm içinde bir sekme oluşturduk

        self.ikinci_bolum_baslik1 = Frame(self.ikinci_bolum)
        self.ikinci_bolum.add(self.ikinci_bolum_baslik1, text="Requests")
        self.ikinci_bolum_baslik1_text = Text(self.ikinci_bolum_baslik1, width=200, height=30)
        self.ikinci_bolum_baslik1_text.pack()


        # sağ tık yapıldığında oluşacak olaylar
        def ikinci_bolum_menu_encode_decode():
            print("Encode/Decode")

        def ikinci_bolum_menu_istek():
            print("İstek")

        def ikinci_bolum_menu_dongu():
            print("Döngü")

        ikinci_bolum_menu = Menu(w, tearoff=0)
        ikinci_bolum_menu.add_command(label="Encode/Decode", command=ikinci_bolum_menu_encode_decode)
        ikinci_bolum_menu.add_command(label="İstek", command=ikinci_bolum_menu_istek)
        ikinci_bolum_menu.add_command(label="Döngü", command=ikinci_bolum_menu_dongu)

        def pencere(event):
            ikinci_bolum_menu.post(event.x_root, event.y_root)

        self.ikinci_bolum_baslik1_text.bind("<Button-2>", pencere)



        self.ikinci_bolum_baslik2 = Frame(self.ikinci_bolum)
        self.ikinci_bolum.add(self.ikinci_bolum_baslik2, text="Response")
        self.ikinci_bolum_baslik2_text = Text(self.ikinci_bolum_baslik2, width=200, height=30)
        self.ikinci_bolum_baslik2_text.pack()

        self.ikinci_bolum_baslik3 = Frame(self.ikinci_bolum)
        self.ikinci_bolum.add(self.ikinci_bolum_baslik3, text="Json Decode")
        self.ikinci_bolum_baslik3_text = Text(self.ikinci_bolum_baslik3, width=200, height=30)
        self.ikinci_bolum_baslik3_text.pack()

        self.secenekler.pack()
        self.hedef_baslik.pack()
        self.hedef_veriyi_al.pack()
        self.hedef_buton.pack()
        self.birinci_bolum.pack(side=TOP, fill=X)
        self.ikinci_bolum.pack()


        # -------------------------------------- İSTEK BÖLÜMÜ --------------------------------------


        self.istek = Frame(self.secenekler)
        self.secenekler.add(self.istek, text="İstek")


        # -------------------------------------- ENCODE/DECODE BÖLÜMÜ --------------------------------------



        self.encode_decode = Frame(self.secenekler)
        self.secenekler.add(self.encode_decode, text="Encode/Decode")

        self.encode_decode_text = Text(
                            self.encode_decode,
                            width=80,
                            height=18,
                            bg="#E7E2E2",
                            font=("open sans", 15, "bold"),
                            relief=SUNKEN,
                            bd=1,
        )
        self.encode_decode_text.pack(anchor=W)

        self.encode_decode_text2 = Text(
                            self.encode_decode,
                            width=80,
                            height=18,
                            bg="#E7E2E2",
                            font=("open sans", 15, "bold"),
                            relief=SUNKEN,
                            bd=1,
        )
        self.encode_decode_text2.pack(anchor=W)

        '''
        anchor = posizyonu ayarlıyoruz

                  N
           NW            NE

        W                     E

            SW           SE

                  S
        '''

        self.encode_decode_url_encode = Button(
            self.encode_decode,
            text="Url Encode",
            command = None,
            font=("open sans", 13, "bold"),
            width=11,
            height=2
        )
        self.encode_decode_url_encode.place(x=1000, y=50) #place = yer konumunu ayarlıyoruz
        ''':arg
        place ise yer konumunu ayarlıyor. x=1000 dediysek bu soldan sağa 1000 git
        yukardan aşşağı 50 git
        '''

        self.encode_decode_url_decode = Button(
            self.encode_decode,
            text="Url Decode",
            command = None,
            font=("open sans", 13, "bold"),
            width=11,
            height=2
        )
        self.encode_decode_url_decode.place(x=1120, y=50)

        self.encode_decode_base64_encode = Button(
            self.encode_decode,
            text="Base64 Encode",
            command = None,
            font=("open sans", 13, "bold"),
            width=11,
            height=2,

        )
        self.encode_decode_base64_encode.place(x=1000, y=100)

        self.encode_decode_base64_decode = Button(
            self.encode_decode,
            text="Base64 Decode",
            command = None,
            font=("open sans", 13, "bold"),
            width=11,
            height=2,

        )
        self.encode_decode_base64_decode.place(x=1120, y=100)


        # -------------------------------------- LOG BÖLÜMÜ --------------------------------------


        self.log = Frame(self.secenekler)

        self.log_kutu = Text( #Log çıktıları
            self.log,
            width=190,
            height=50,
            bg="#E7E2E2",
            font=("open sans", 15, "bold"),
            relief=SUNKEN,
            bd=1,)
        self.secenekler.add(self.log, text="Log")
        self.log_kutu.pack()
        self.log_kutu.insert(END, "Giriş: "+ str(datetime.datetime.now()) + "\n")


        # -------------------------------------- Intruder --------------------------------------


        self.intruder = Frame(self.secenekler)
        self.secenekler.add(self.intruder, text="Döngü")


        # --------------------------------------------------------------------------------------
        self.secenekler.pack(expand=1, fill="both") #fill yapılıcak dolgudur. Both veriyoruz çünkü her yeri doldurmasını istiyoruz



    def Url_Crawler_SECTION_1(self): # sayfa içerisindeki bütün url'leri çekiyoruz
        html_page = self.req_text
        soup = BeautifulSoup(html_page,'html.parser')
        links1 = re.findall('"((http|ftp)s?://.*?)"', html_page)
        links2 = re.findall("'((http|ftp)s?://.*?)'", html_page)
        if links1:
            for t in links1:
                if self.host_strip_control in t[0]:
                    self.URL_LIST.add(t[0])
                else:
                    self.NOT_CONTENT_URL_LIST.add(t[0])

        if links2:
            for t2 in links2:
                if self.host_strip_control in t2[0]:
                    self.URL_LIST.add(t2[0])
                else:
                    self.NOT_CONTENT_URL_LIST.add(t2[0])

        for i in list(self.URL_LIST):
            if self.host_strip_control in i.split('/')[2]:  # [2] = domain
                try:
                    if i.split('/')[3]:  # Neden 12 tane derseniz en son ihtimale kadar parçalama yapmaya çalıştım. Arttırılabilir
                        self.DIRECTORY_2.add(str(i.split('/')[3]))
                    if i.split('/')[4]:
                       self.DIRECTORY_2.add(str(i.split('/')[3] + '/' + i.split('/')[4]))
                    if i.split('/')[5]:
                        self.DIRECTORY_2.add(str(i.split('/')[3] + '/' + i.split('/')[4]) + '/' + i.split('/')[5])
                    if i.split('/')[6]:
                        self.DIRECTORY_2.add(str(i.split('/')[3] + '/' + i.split('/')[4]) + '/' + i.split('/')[5] + '/' +i.split('/')[6])
                    if i.split('/')[7]:
                        self.DIRECTORY_2.add(str(i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6]) + '/' + i.split('/')[7])
                    if i.split('/')[8]:
                        self.DIRECTORY_2.add(str(i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5]) + '/' +i.split('/')[6] + '/' + i.split('/')[7] + '/' + i.split('/')[8])
                    if i.split('/')[9]:
                        self.DIRECTORY_2.add(str(
                            i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6]) + '/' + i.split('/')[7] + '/' + i.split('/')[8] + '/' + i.split('/')[9])
                    if i.split('/')[10]:
                        self.DIRECTORY_2.add(str(
                            i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' + i.split('/')[7] + '/' + i.split('/')[8] + '/' + i.split('/')[9] + '/' +i.split('/')[10]))
                    if i.split('/')[11]:
                        self.DIRECTORY_2.add(str(
                            i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' + i.split('/')[7] + '/' + i.split('/')[8] + '/' + i.split('/')[9] + '/' +i.split('/')[10] + '/' + i.split('/')[11]))
                    if i.split('/')[11]:
                        self.DIRECTORY_2.add(str(i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' + i.split('/')[7] + '/' + i.split('/')[8] + '/' + i.split('/')[9] + '/' +i.split('/')[10] + '/' + i.split('/')[11] + '/' + i.split('/')[11]))
                        """
                        test/test1/test2
                        |
                        |_______test1
                        |_________test1/test2
                        |____________test1/test2/test3
                        |_______________test1/test2/test3/test4 ...
                        """
                except:
                    continue

        try:

            for i in self.DIRECTORY_2:

                self.Section_3_Request = requests.get(
                            self.host +
                            '/' +
                            i,
                            timeout=0.8,
                            headers={'User-Agent': self.Random_Useragent})

                self.Section_3_Content = self.Section_3_Request.content

                links = re.findall('"((http|ftp)s?://.*?)"', self.Section_3_Content)

                for t in links:
                    if self.host_strip_control in t[0]:
                        self.TOTAL_URL.add(t[0])
                    else:
                        self.NOT_CONTENT_URL_LIST.add(t[0])

        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.SSLError:
            pass
        except:
            pass

        for jj in list(self.TOTAL_URL):
            self.URL_LIST.add(str(jj))


        threading.Thread(target=self.Tarama).start()
        # self.CONTENT_URL_LIST'da url'ler yer alıyor
        # self.NOT_CONTENT_URL_LIST'da ise kaynak'da yer alan fakat aynı domaine ait olmayan URL'ler





    def ISTEK(self, veri,istek_arttir):

        self.istek_arttir = istek_arttir
        self.veri = veri

        try:

            self.req_istek = requests.get(str(self.veri), timeout=0.8)
            self.headers = self.req_istek.headers

        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except:
            pass


        if "http" in self.veri and "https" in self.veri:

            self.http_veri = self.veri

        else:

            self.http_veri = self.veri

        self.content_type = ""

        for v,k in self.headers.items():
            if v == 'Content-Type':
                if ";" in k:
                    self.content_type = k.split(';')[0]
                else:
                    self.content_type = k
            else:
                if v == "Content-Type":
                    self.content_type = k

        folder1 = self.birinci_bolum.insert(
                                                "",
                                                'end',
                                                text=str(self.istek_arttir),
                                                values=(str(self.host_strip),"GET",
                                                str(self.veri),
                                                str(self.req_istek.status_code),
                                                str(len(self.req_istek.content)),
                                                str(self.content_type),
                                                ))

        """        self.data = {}
        self.data['site'] = str(self.req_istek.url)
        self.data['headers'] = str(self.req_istek.headers)
        self.data['content'] = str(self.req_istek.content)
        #response bölümüne yazarken kullanıcağımız data

        #0.json vb. dosyayı açarak yazıyoruz
        self.dosya_olustur = open('data/' + str(self.istek_arttir) + '.json', 'w+')

        self.dosya_olustur.write(json.dumps(self.data))"""





    def Tarama(self):
        thread = []
        self.tarama_sayi = 0
        for i in list(self.URL_LIST):
            self.ISTEK(i, self.tarama_sayi)
            self.tarama_sayi += 1
            # tarama_sayi: Her yaptığımız isteğe bir sayı değeri veriyoruz.
            #request ve responsu gösterirken bu değer ile dosyayı çağırmamız gerekiyor


if __name__ == "__main__":
    w = Window()
    w.govde()
    w.mainloop()


