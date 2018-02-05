# Basit USIS ders seçim botu

# Kurulum

```bash
      $ git clone https://github.com/Emre-Kul/USISBOT
      $ cd USISBOT
      $ virtualenv venv
      $ source venv/bin/activate
(venv)$ pip install -r requirements.txt
(venv)$ # Bu kisimda config.json dosyasini guncellemeyi unutmayin.
(venv)$ python main.py 
```

## Alt kisimlari config.json icerisine uygulayin.
### Bu kısma eklemek istediğiniz derslerin kodu ve grubunu örnekteki gibi giriniz.

```
courses = [
	{ 'code' : 'BLM4520' , 'gr' : '1'},
	{ 'code' : 'BLM4821' , 'gr' : '1'}
]
```

### Bu kısmı USIS sistemine giriş yaptıktan sonra size özel oluşturulan JSSESIONID isimli cookie ile değiştiriniz.
#### Cokkie'yi gösterildiği şekilde bulabilirsiniz.
<iframe src='https://gfycat.com/ifr/OptimisticShallowCopperbutterfly' frameborder='0' scrolling='no' width='1014' height='772' allowfullscreen></iframe>
```
cookie = ""

```
