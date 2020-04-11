# TDT4140 - Programvareutvlikling gruppe 54 2020  
<img src="https://gitlab.stud.idi.ntnu.no/tdt4140-2020/54/-/raw/master/afkforum/forumApp/static/images/homelogo.png" width="150"> 



Gruppeprosjekt i faget [TDT4140 - Programvareutvliklig](https://www.ntnu.no/studier/emner/TDT4140#tab=omEmnet)  

# Motivasjon 
Norges gamere skriker etter et forum for å dele tanker og erfaringer. Deres bønner har blitt hørt. Det nye AFK-forumet er skreddersydd for den norske gamer. På AFK-forum skal gamere kunne opprette tråder under emner for å diskutere alt fra spill til konsoller. Alle kan kommentere og vurdere hverandres tråder og kommentarer. På AFK-forumet er det mulig å opprette egen profil, hvor man kan fylle ut informasjon om seg selv, og hvilke spill man liker, osv. I tillegg kan man legge til venner og diskutere privat I chattesystemet. Her skal man også kunne få spennende tilbud og informasjon fra spillselskaper.
  
  # Utviklere
  * Elias Søvik Gunnarsson
  * Sondre Westby Liestøl
  * Vår Sørensen Sæbøe-Larssen
  * Karoline Kanestrøm Sæbø
  * Bård Olstad
  * Jørgen Nummedal Sveberg
  * Nora Vaage Valen
  
  # Teknologier og rammeverk  
 [Python 3.8+](https://www.python.org/): Språk benyttet for frontend og backend.  
 [Django](https://www.djangoproject.com/): Web-rammeverk skrevet i Python, nyttet både i frontend og backend.  
 [Heroku](https://heroku.com): Platform as a service ([PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service)) - Skyplattform med funksjoner for å bygge, skalere og kjøre applikasjoner.    
 [PostgreSQL](https://www.postgresql.org): Open-source DBMS ([Heroku Postgres](https://www.heroku.com/postgres)).  
 [Amazon S3](https://aws.amazon.com/s3): Skylagring til bilder.  
 [Bootstrap](https://getbootstrap.com/): Frontend-rammeverk skrevet i HTML, CSS og JavaScript.   
 [HTML](https://whatwg.org): Språk benyttet i frontend.  
 [CSS](https://www.w3.org/Style/CSS/): Språk i benyttet frontend.    
 [JavaScript](https://www.javascript.com): Språk i benyttet frontend.

# Installasjon
Installasjonen tar forbehold om at [git](https://git-scm.com/downloads), samt [postgres.app](https://postgresapp.com) (kun nødvendig for macOS) er installert.  
1. Klon prosjektet:  
 `git clone https://gitlab.stud.idi.ntnu.no/tdt4140-2020/54.git`  
2. Naviger til repository:  
 `cd 54`  
3. Installer avhengigheter:  
 `pip install -r requirements.txt`

**Kjøre applikasjonen lokalt:**
1. Kjøre Djangos utviklingsserver (Kun til bruk under utvikling, og ikke i produksjon):  
 `python afkforum/manage.py runserver`  
2. Åpne adresse:  
 http://localhost:8000/  

# Deployment  
Applikasjonen er deployed på Herokus [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service). Alle Herokus tjenester er hostet på Amazons [EC2](https://aws.amazon.com/ec2/) cloud-computing platform.
 Bilder som blir lastet opp i applikasjonen blir lagret i skylagringen [Amazon S3](https://aws.amazon.com/s3). Håndtering av API-nøkler knyttet til applikasjonen blir tatt for seg i sekjonen [Environment variables](#environment-variables).  
 Adresse til applikasjon:  
   
 http://www.afkforum.no  
 Prøv [her](http://afk-forum.herokuapp.com/forumApp/) dersom adressen ikke fungerer.
 
# Environment variables

**Environment variables i Heroku:**  
 Last ned [Heroku Command Line Interface (CLI)](https://devcenter.heroku.com/articles/heroku-cli) for å håndtere herokuapplikasjonen direkte fra terminalen.
  Alternativt kan dette gjøres inne i [innstillingene](https://dashboard.heroku.com/apps) til herokuapplikasjonen. Det kreves også tilgang som contributor fra [eier](mailto:eliassg@stud.ntnu.no) av Herokuapplikasjonen.  

*Vise nåværende variabelverdier:*  
 `heroku config`  
  
*legge til variabelverdier:*  
Variabler settes inn en etter en. Nye variabler legges til på samme måte som eksisterende variabler har blitt lagt inn:  
 `heroku config:set AWS_ACCESS_KEY_ID=<Legg inn AWS access key ID> `  
 `heroku config:set AWS_SECRET_ACCESS_KEY=<Legg inn AWS secret access key> `   
 `heroku config:set AWS_STORAGE_BUCKET_NAME=<Legg inn AWS storage bucket name> `  
  
*fjerne en variabelverdi:*  
 `heroku config:unset AWS_ACCESS_KEY_ID `  

**Legge til environment variables lokalt:**  
Dersom det er ønskelig at bilder blir lastet opp i AWS S3 når applikasjonen kjøres lokalt, må environment variables legges til lokalt også.  
  
I *Windows* legges environment variables inn på [følgende måte](https://www.youtube.com/watch?v=IolxqkL7cD8&t=2s).  
  
*OS X & Linux:*
1. Naviger til hjem-katalogen:  
 `cd`  
2. Åpne .bash_profile:  
 `nano .bash_profile`  
Merk: hvilken som helst kode-editor kan benyttes i stedet for nano  
3. Legg til variabler:  
`export AWS_ACCESS_KEY_ID:"<Legg inn AWS access key ID>" `  
`export AWS_SECRET_ACCESS_KEY:"<Legg inn AWS secret access key>" `   
`export AWS_STORAGE_BUCKET_NAME:"<Legg inn AWS storage bucket name>" `  

# Vedlikehold  
  
For vedlikehold i Heroku er installasjon av [Heroku Command Line Interface (CLI)](https://devcenter.heroku.com/articles/heroku-cli) nødvedig.
  
**Nullstille database i Heroku**   
1. `heroku pg:reset DATABASE`  

**Nullstille database lokalt**  
1. `cd 54/afkforum`  
2. `python manage.py flush`  
3. Følg instruksjoner i terminal

**Lage ny superbruker i Heroku**  
1. `heroku run python manage.py createsuperuser`  
2. Følg instruksjoner i terminal  

**Lage ny superbruker lokalt**  
1. `cd 54/afkforum`
2. `python manage.py createsuperuser`
3. Følg instruksjoner i terminal

**Ved endringer i models**  
Ved endringer i applikasjonens models må følgende steg utføres:
1. Lage nye migrations basert på endringene som har vært gjort i models:  
 `afkforum/manage.py makemigrations`  
2. Påføre eller fjerne migrations:  
 `afkforum/manage.py migrate`  
3. Pushe endret kode til CI Pipeline  
4. Påføre eller fjerne migrations i Heroku:  
 `heroku run python manage.py migrate`   

# Testing 
Applikasjonen benytter seg av Unit-tester. Test - coverage dekkes i [oversikt over kodekvalitet](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/54/-/wikis/Oversikt-over-kodekvalitet).  
Tester kjøres automatisk ved kjøring av CI Pipeline ved deployment til Heroku, og kan kjøres inne i GitLab. For å kjøre testene lokalt:  
1. `cd 54/afkforum`  
2. `python manage.py test`  

[![coverage report](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/54/badges/master/coverage.svg)](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/54/-/commits/master)  
  
# Bidrag  
AFK-Forum er et open source prosjekt, og bidrag er velkomne.  
Bidrag gjøres gjennom en ["fork-and-pull" Git workflow](https://reflectoring.io/github-fork-and-pull/).  
1. **Fork** repository på GitLab  
2. **Clone** prosjektet på egen maskin  
3. **Commit** endringer til egen branch  
4. **Push** arbeidet til egen fork  
5. Publiser en **merge request** så bidraget kan bli gjennomgått  
  
# Lisens  
[MIT Licence](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/54/-/blob/master/LICENSE)  

