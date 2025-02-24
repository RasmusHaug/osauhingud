# RIK Assignment

## Kirjeldus

Katse lahendada RIK Python Arendaja koduülesanne.

Veebileht on loodud kasutades [Django](https://www.djangoproject.com/) koos [PostgreSql](https://www.postgresql.org/) andmebaasiga.

Veebileht lubab kasutajal osaühinguid __asutada__, __otsida__ ning __andmeid vaadata__.

### Failistruktuur
Veebirakendus ise asub kaustas `companyApp` ning kõik Djangoga seotud konfiguratsiooni failid `config` kaustas.

#### config kaust
Veebirakendusel puudub Django klassikaline `settings.py` file ning see on asendatud 3 failiga kaustas `config/django/`.
- `base.py`
	- Django `settings.py` baas seaded mis kehtivad olenemata mis keskkonnas rakendus jooksutatakse: kas **lokaalselt** või **productionis**
- `local.py`
	- Django seadeid üle kirjutav fail mis konfigureerib seaded lokaalseks arenduseks ja testimiseks.
- `production.py`
	- Django baasseadeid üle kirjutav fail mis konfigureerib seaded production serveri jaoks, põhiliselt eemaldades `debug` mode ja nõuab [HTTPS](https://en.wikipedia.org/wiki/HTTPS) protokolli ja seadistab [HSTS](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security) seaded.

#### companyApp
Veebirakenduse enda failid asuvad kõik oma appis `companyApp`. 
+ `migrations/`
	+ Kaust kus kõik andmebaasi muudatused kirjas. 
+ `static/`
	+ Kaust kus asub rakenduse CSS fail.
+ `templates/`
	+ `base/`
		+ Rakenduse baas HTML fail mille peale kõik ülejäänud failid oma koodi kirjutavad.
	+ Kõik veebirakenduse HTML failid asuvad `templates` kaustas.
+ `forms.py`
	+ companyApp vormid mida HTML failid kasutavad ja mille põhjal andmed andmebaasi salvestatakse
+ `models.py`
	+ Rakenduse mudelite kaust kust defineeritakse kuidas ja mis andmeid andmebaasi salvestada
+ `urls.py`
	+ Rakenduses kasutatavad URL andmed
+ `views.py`
	+ Front-endi poolt kasutatavad Pythonis kirjutatud meetodid.

### Avaleht
Avalehel näeb kõiki andmebaasi lisatuid firmasid: nende ___nimesid___, ___registrikoode___ ja kes on selle firma ___osanikud___.

Otsinguga saab otsida **osaühinguid** või **osanikke** nime, registrikoodi või isikukoodi alusel. 
Alustades otsingut klikates nuppu `Otsi` või vajutades klahvile `Enter` filtreeritakse alumises tabelis kõik firmad välja arvatud mis vastasid otsingu tulemusele.

Otsingu funktsioon ei ole dünaamiline ega kasuta Javascripti, et realajas filtreerida vaid alles siis jooksutab koodi kui kasutaja spetsiifiliselt vajutab `Otsi`.

#### Osaühingute tabel
Osaühingute tabelis on 3 tulpa: 
+ ___osaühingu nimi___
	+ Osaühingu nimi millele klikates avatakse osaühingu andmete vaade.
+ ___osaühingu registrikood___
	+ Osaühingu salvestatud registrikood.
+ ___osaühingu osanikud___
	+ Kõik osanikud kes on osaühinguga seotud.

#### Lisa Uus Osaühing
Klikates nupule `Lisa uus Osaühing` navigeeritakse kasutaja uuele vaatele kus täpsemalt saab lugeda siit.

### Osaühingu andmete vaade
Klikates osaühingu nimele avalehel avaneb osaühingu andmete vaade.

Kõik osaühingud on andmebaasis salvestatud unikaalse numbriga mille tulemusena on projekti URL aadressid alati uuenevad kui navigeeritakse veebilehel. Sama omapära annab kasutajale mugava võimaluse spetsiifilise firma andmete vaate link kopeerida ja jagada.

Iga osaühingu kohta näeb selle ___registrikoodi___, ___asutamise kuupäeva (dd,mm,yyyy)___ ja osaühingu ___kogukapitali___.

Igal osaühingul on Osanikud välja toodud tabeli näol, kust näeb:
+ **Osanike tüüp**
	+ Kas tegu on Juriidilise või füüsilise osanikuga
+ **Osaniku nimi**
	+ Kas juriidilise firma või füüsilise isiku nimi.
+ **Osaniku registri- või isikukood**
	+ Olenevalt osaniku tüübist.
+ **Osaniku suurus (€)**
	+ Osaniku suurus osaühingus.
+ **Osaniku staatus**
	+ Kas tegu on ainu asutajaga, üks asutajatest või hiljem lisatud osanik.


### Osaühingu asutamise vorm
Osaühingu asutamise vormil saab teha järgnevaid tegevusi.
+ Lisada uus osaühing
	+ Täpsemalt saab lugeda [siit]
+ Lisada osaühingu asutajad
	+ Täpsemalt saab lugeda [siit]
+ Lisada uus asutaja vorm
	+ Täpsemalt saab lugeda [siit]
+ Salvestada osaühing ja osaniku
	+ Saadab Django Back-endile informatsiooni uuest Osaühingust ning sellega seotud asutajatest. Django salvestab informatsiooni PostgreSQL andmebaasi.
+ Navigeerida tagasi avalehele
	+ Ei salvesta muudatusi ning navigeerib tagasi avalehele.


#### Lisa uus Osaühing
Osaühingu asutamise vormil tuleb täita iga osaühingu kohta selle ___nimi___, ___registrikood___, ___asutamise kuupäev___ ja ___kogukapital___.

Osaühingu nimi peab olema 3-100 tähemärki ning seda kontrollib järgmine regex:
- **[\p{L}\p{N}\p{P}\p{Zs}]{3,100}**
	- - **\p{L}** → Vastab tähtedele mis tahes keeles (A-Z, ä, ö, ü, ß, jne.).
	- **\p{N}** → Vastab numbritele (0-9, jne.).
	- **\p{P}** → Vastab kirjavahemärkidele (.,!?(){} jne.).
	- **\p{Zs}** → Vastab tühikutega seotud märkidele (tühikud, mittemurdvad tühikud jne.).
	- **{3,100}** → Nõuab, et nimi oleks vahemikus 3 kuni 100 tähemärki.

Osaühingu registrikood peab olema täpselt 7 tähemärki pikk ning veebirakendus ei luba üle selle lisada. Juhul kui kasutaja lisab vähem kui 7 numbrit tuleb veateade ette.

Osaühingu asutamise kuupäeva puhul kasutab browserite sisseehitatud kuupäeva formaati, mis ei nõua kellaaega.

Osaühingu kogukapitalil on kontroll kas see on vähemalt 2500 €.

#### Lisa Asutajad
Pärast osaühingu asutamise vormi asub asutajate lisamise vorm. 
Vormi kohal on olemas otsing mis töötab dünaamiliselt ning realajas otsib firmasid ning isikuid sisestades vähemalt 3 tähemärki. 

Identselt avalehe otsingule saab otsida  **osaühinguid** või **osanikke** nime, registrikoodi või isikukoodi alusel. 
Klikates otsingu tulemusel leitud nimele täidetakse alumine vorm füüsilise isiku või juriidilise firma andmetega kasutaja eest. 

Vaikimisi on Asutaja staatus märgitud kui **Asutaja**. Juhul kui lisatakse uus asutaja kas läbi otsingu või klikates nupule `Lisa uus asutaja vorm` muudetakse staatus ära `üks asutajatest`.

Soovi korral saab vormi kustutata kasutaja kliendilt. Iga vormi üleval paremal nurgas asub oranž X millele klikates vormi taotlus kaob. Seda ei saa tagasi võtta.

Kõige viimast vormi ei saa kustudata.

Esimene vorm saadakse Pythoni back-endist ning edaspidi majandab vormidega Javascript kliendi browseris. Lisades uus vorm kloonib javascript esimese vormi ning loob sellele uue elemendi. 
See lahendus tähendab, et kasutaja veebileht ei pea konstantselt serverilt küsima uut vormi vaid ainult korra navigeerides saadab server uue vormi malli.

## Veebirakenduse tarkvara installeerimine
### Projekti kloonimine
Projekti lokaalseks jooksmiseks tuleb kõigepealt projekt kloonida oma arvutisse. 
Lähemalt saab selle kohta lugeda [GitHub guides veebilehelt](https://github.com/git-guides/git-clone)


### PostgreSQL installimine
Projekt loodi [PostgreSQL](https://www.postgresql.org/) andmebaasi kasutamisega. 
Selleks, et projekti jooksutada lokaalselt peab olema PostgreSQL installitud, vastasel juhul rakendus ei jookse.

PostgreSQL installimis asukoha võib suvaliselt valida kus soovite, aga meelde tuleb jätta järgnevad seadistused:
+ kasutajanimi (vaikimisi **postgres**)
+ port (vaikimisi **5432**)
+ parool - kasutaja enda määrata

### Pythoni installimine
Veebirakenduse lokaalseks jooksmiseks tuleb kõigepealt alla laadida [Python](https://www.python.org/downloads/). Rakenduses kasutati Python versioon **3.12.7**, mis esmakordselt väljastati 2023-10-24 ja mille tugi lõpetatakse 2028-10.

Pythoni installitud versiooni saab kontrollida terminali käsklusega:
```shell
python --version
```
Vastuseks peaks tulema installitud Pythoni versioon.

Juhul kui Python pole installitud tuleks see alla laadida [siit](https://www.python.org/downloads/)

### Venv keskkonna seadistamine
Pythonit kasutades on rangelt soovituslik igale projektile uus keskkond luua. 
Kui projekt on kloonitud navigeeri konsooliga (nt [powershell](https://learn.microsoft.com/en-us/powershell/)) projekti kausta ning loo uus **venv** keskkond.

Täpsemalt saab virtuaal keskkondadest lugeda [Python dokumentatsioonist](https://docs.python.org/3/tutorial/venv.html)

Venv keskkonna loomiseks tuleks järgnevad käsklused konsooli sisestada
```shell
python -m venv venv-osauhingud
```
Viimane käsklus loob hetkel asuvasse kausta uue kausta nimega `venv-osauhingud` ning seejärel tuleb see aktiveerida järgneva käsklusega

Windowsi arvutis:
```shell
.\env_osauhingud\Scripts\activate
```

Pärast keskkonna aktiveerimist peaks visuaalselt nägema terminalis keskkonna nime.

Järgnevalt navigeeri kloonitud GitHub projekti kausta (juhul kui juba ei asu seal) ning installi [PIP](https://pypi.org/project/pip/) paketid.
```shell
python -m pip install -r requirements.txt
```


## Veebirakenduse jooksutamine
Enne rakenduse jooksutamist tuleb seadistada keskkonna parameetrid.
Seda tuleb teha kõige viimasena.

Navigeeri kloonitud projekti juur kausta ning loo sinna uus fail:
```powershell
New-Item .env
```
Pärast käskluse jooksutamist peaks tulema järgnev teade:
```PowerShell
╰─ New-Item .TEST

        Directory: C:\Projects\osauhingud\osauhingud


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a---        24/02/2025     13:38              0   .env
```

Lisaks seda saab kontrollida järgneva käsklusega PowerShellis:
```PowerShell
╰─ dir

        Directory: C:\Projects\osauhingud\osauhingud


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d----        24/02/2025     11:28                  companyApp
d----        19/02/2025     11:10                  config
-a---        18/02/2025     18:12            259   .env
-a---        19/02/2025     11:10           1990   .gitignore
-a---        18/02/2025     18:24            764   manage.py
-a---        18/02/2025     17:22              0 󰪷  README.md
-a---        18/02/2025     18:03            154 󰈙  requirements.txt
```

Kui `.env` on edukalt installitud avada see endale sobiliku programmiga ([Vim](https://www.vim.org/), [Vs Code](, https://code.visualstudio.com/), [Notepad](https://apps.microsoft.com/detail/9msmlrh6lzf3?hl=en-us&gl=US)) kas läbi konsooli või läbi File Explorer'i.

`.env` faili tuleb järgmised read lisada
```
# Defineerib, et rakendusele kehtivad lokaalse arenduse reeglid.
DJANGO_SETTINGS_MODULE='config.django.local'

# Suvaliselt genereeritud võti Django jaoks
DJANGO_SECRET_KEY='django-insecure-q^r(w#t@z&)$c!_q8_cv(l$953wmol**b2q9buak-h_(zv8glh'

# Django Debug seaded sees. Veateate puhul annab täpsema informatsiooni.
DJANGO_DEBUG=True

# PostgreSQL andmebaasi nimi
POSTGRESQL_NAME=postgres

# PostgreSQL andmebaasi kasutajanimi
POSTGRESQL_USER=postgres

# PostgreSQL andmebaasi kasutaja parool
POSTGRESQL_PASSWORD=
```

Ainult viimased 3 rida tuleb täita eelnevalt TODO: [PostgreSQL seadistamisel]() valitud seadetega. 
- `POSTGRESQL_NAME` - andmebaasi nimi, vaikimisi seadistatud **postgres**
- `POSTGRESQL_USER` - andmebaasi kasutajanimi mis installeerides valisid
- `POSTGRESQL_PASSWORD` - andmebaasi parool mis installeerides seadistasid.

Kui kõik andmed on korrektselt sisestatud saab rakendust jooksutada ning ei tule ühtegi vea teavitust.

Veebirakenduse saab jooksutada järgneva käsklusega:
```shell
python .\manage.py runserver
```


## Veateated
Kõige tõenäolisemad veateated tekivad andmebaasist seotud probleemidega. 
Juhul kui Django ei leia andmebaasi vastavalt `.env` faili lisatud infole ütleb konsooli tekkinud veateade selle otse viimasel real välja. 
Näiteks kui puudub andmebaasi **nimi**, **kasutaja** või **parool** on veateade umbes selline:
```powerShell
  File "C:\Projects\osauhingud\env_osauhingud\Lib\site-packages\environ\environ.py", line 413, in get_value
    raise ImproperlyConfigured(error_msg) from exc
django.core.exceptions.ImproperlyConfigured: Set the POSTGRESQL_USER environment variable
```

Kui konsool näitab järgnevat veateadet:
```powerShell
django.db.utils.OperationalError: connection to server at "localhost" (::1), port 5432 failed: FATAL:  password authentication failed for user "postgresS"
```
võib see tähendada, et kas andmebaasi kasutajanimi või parool on vale. Hetke näites on andmebaasi kasutajanimele lisatud lisa `S`.

Kui andmebaasi nimi on valesti kirjutatud ning Django seda ei leia tuleb järgnev veateade:
```powerShell
django.db.utils.OperationalError: connection to server at "localhost" (::1), port 5432 failed: FATAL:  database "postgresD" does not exist
```
Andmebaasi nime lõppu on lisatud lisa `D` mille tulemusena Django DB utils esitab veateate, et sellist andmebaasi ei leidnud.
