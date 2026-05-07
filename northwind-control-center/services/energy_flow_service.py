"""Global Oil & Gas Energy Flow Simulation — Max-Flow / Min-Cut service."""
import math
from datetime import datetime
import networkx as nx

# ── Oil producers ──────────────────────────────────────────────────────────────
OIL_PRODUCERS = [
    # Middle East
    {'key':'prod-sau','label':'Saudi Arabia (Ras Tanura)',  'lat': 26.6, 'lng': 50.1, 'kbd':9800},
    {'key':'prod-irq','label':'Iraq (Basra Terminal)',       'lat': 29.7, 'lng': 48.8, 'kbd':3900},
    {'key':'prod-irq-n','label':'Iraq (Kirkuk / Ceyhan)',   'lat': 35.5, 'lng': 44.4, 'kbd': 600},
    {'key':'prod-uae','label':'UAE (Fujairah)',              'lat': 25.1, 'lng': 56.3, 'kbd':3200},
    {'key':'prod-kwt','label':'Kuwait (Al-Ahmadi)',          'lat': 29.1, 'lng': 48.1, 'kbd':2200},
    {'key':'prod-irn','label':'Iran (Kharg Island)',         'lat': 29.2, 'lng': 50.3, 'kbd':1500},
    {'key':'prod-omn','label':'Oman (Mina al-Fahal)',       'lat': 23.6, 'lng': 58.6, 'kbd': 900},
    # Russia & FSU
    {'key':'prod-rus','label':'Russia (Samara / trunk)',     'lat': 53.2, 'lng': 50.2, 'kbd':6200},
    {'key':'prod-kaz','label':'Kazakhstan (Tengiz/CPC)',     'lat': 45.4, 'lng': 53.1, 'kbd':1400},
    {'key':'prod-aze','label':'Azerbaijan (Sangachal/BTC)', 'lat': 40.1, 'lng': 49.6, 'kbd':1000},
    # Africa
    {'key':'prod-nga','label':'Nigeria (Bonny)',             'lat':  4.5, 'lng':  7.2, 'kbd':1400},
    {'key':'prod-lby','label':'Libya (Es Sider / Zueitina)','lat': 30.6, 'lng': 18.5, 'kbd':1100},
    {'key':'prod-ago','label':'Angola (Luanda / Malongo)',  'lat': -8.8, 'lng': 13.2, 'kbd':1200},
    {'key':'prod-alg','label':'Algeria (Arzew terminal)',   'lat': 35.8, 'lng': -0.3, 'kbd': 800},
    # Europe & North Sea
    {'key':'prod-nor','label':'Norway (Mongstad / Sture)',  'lat': 60.8, 'lng':  5.0, 'kbd':1300},
    {'key':'prod-uk', 'label':'UK (Sullom Voe / Forties)', 'lat': 60.5, 'lng': -1.3, 'kbd': 700},
    # Americas
    {'key':'prod-usa','label':'USA (LOOP / Houston channel)','lat':28.9,'lng':-89.2,  'kbd':4300},
    {'key':'prod-mex','label':'Mexico (Dos Bocas / Cayo)',  'lat': 18.3, 'lng':-93.1, 'kbd':1600},
    {'key':'prod-can','label':'Canada (Atlantic)',           'lat': 47.0, 'lng':-53.0, 'kbd':1100},
    {'key':'prod-ven','label':'Venezuela (Maracaibo/Aruba)','lat': 10.5, 'lng':-71.6, 'kbd': 700},
    {'key':'prod-bra','label':'Brazil (Santos/Campos)',     'lat':-23.0, 'lng':-43.0, 'kbd':1000},
    # Asia-Pacific
    {'key':'prod-idn','label':'Indonesia (Dumai / Ardjuna)','lat':  1.7, 'lng':101.4, 'kbd': 800},
]

# ── Maritime chokepoints ───────────────────────────────────────────────────────
CHOKEPOINTS = [
    {'key':'chk-hormuz',   'label':'Strait of Hormuz',   'lat': 26.60,'lng': 56.27,'normal_kbd':18500,'gas_bcm':200},
    {'key':'chk-malacca',  'label':'Strait of Malacca',  'lat':  1.30,'lng':103.80,'normal_kbd':16000,'gas_bcm':200},
    {'key':'chk-bab',      'label':'Bab-el-Mandeb',      'lat': 12.60,'lng': 43.30,'normal_kbd': 6200,'gas_bcm':80},
    {'key':'chk-suez',     'label':'Suez Canal',         'lat': 30.70,'lng': 32.30,'normal_kbd': 4600,'gas_bcm':40},
    {'key':'chk-bosphorus','label':'Bosphorus Strait',   'lat': 41.10,'lng': 29.10,'normal_kbd': 3000,'gas_bcm':5},
    {'key':'chk-capegood', 'label':'Cape of Good Hope',  'lat':-34.40,'lng': 18.50,'normal_kbd':99000,'gas_bcm':9999},
    {'key':'chk-panama',   'label':'Panama Canal',       'lat':  9.10,'lng':-79.70,'normal_kbd':  800,'gas_bcm':50},
    {'key':'chk-gibraltar','label':'Strait of Gibraltar','lat': 36.00,'lng': -5.30,'normal_kbd': 3500,'gas_bcm':100},
    {'key':'chk-danish',   'label':'Danish Straits',     'lat': 56.50,'lng': 12.00,'normal_kbd': 2000,'gas_bcm':10},
    {'key':'chk-druzhba',  'label':'Druzhba Pipeline',   'lat': 52.85,'lng': 32.68,'normal_kbd': 2200,'gas_bcm':30},
]

# ── Pipeline junctions (intermediate cross-border routing nodes) ───────────────
PIPELINE_JUNCTIONS = [
    # Druzhba northern branch
    {'key':'jct-mozyr',    'label':'Mozyr (Belarus) — Druzhba split',   'lat': 52.00,'lng': 29.20},
    {'key':'jct-plock',    'label':'Płock (Poland) — Druzhba north',    'lat': 52.55,'lng': 19.72},
    {'key':'jct-schwedt',  'label':'Schwedt (Germany) — PCK refinery',  'lat': 53.06,'lng': 14.27},
    {'key':'jct-gdansk',   'label':'Gdańsk Naftoport (Poland)',          'lat': 54.38,'lng': 18.67},
    # Druzhba southern branch
    {'key':'jct-brody',    'label':'Brody (Ukraine) — Druzhba south',   'lat': 50.08,'lng': 25.15},
    {'key':'jct-bratislava','label':'Bratislava (Slovakia) — Transpetrol','lat':48.13,'lng': 17.11},
    {'key':'jct-budapest', 'label':'Százhalombatta (Hungary) — Danube refinery','lat':47.33,'lng':18.90},
    # Turkey / Caspian
    {'key':'jct-ceyhan',   'label':'Ceyhan (Turkey) — BTC / Kirkuk endpoint','lat':36.90,'lng':35.90},
    # Russia export terminals
    {'key':'jct-primorsk', 'label':'Primorsk (Russia) — Baltic terminal','lat': 60.37,'lng': 28.64},
    {'key':'jct-novorss',  'label':'Novorossiysk (Russia) — Black Sea', 'lat': 44.73,'lng': 37.79},
    {'key':'jct-kozmino',  'label':'Kozmino (Russia) — Pacific ESPO',   'lat': 42.64,'lng':133.04},
    # Southern Europe entries
    {'key':'jct-trieste',  'label':'Trieste (Italy) — TAL pipeline entry','lat':45.65,'lng':13.77},
    # Saudi bypass
    {'key':'jct-yanbu',    'label':'Yanbu (Saudi Arabia) — Red Sea terminal','lat':24.09,'lng':38.06},
    # ESPO (Eastern Siberia – Pacific Ocean pipeline)
    {'key':'jct-taishet',     'label':'Taishet (Russia) — ESPO source',             'lat': 55.93,'lng': 98.00},
    {'key':'jct-skovorodino', 'label':'Skovorodino (Russia) — ESPO / China split',  'lat': 53.99,'lng':123.92},
    # BTC (Baku–Tbilisi–Ceyhan pipeline)
    {'key':'jct-tbilisi',     'label':'Tbilisi (Georgia) — BTC transit',             'lat': 41.69,'lng': 44.83},
    # Kirkuk–Ceyhan pipeline (Iraq)
    {'key':'jct-fesh-khabur', 'label':'Fesh Khabur (Iraq-Turkey border) — KTC',     'lat': 37.10,'lng': 42.35},
    # Kazakhstan routing hub
    {'key':'jct-atyrau',      'label':'Atyrau (Kazakhstan) — CPC / KCP hub',         'lat': 47.11,'lng': 51.90},
    {'key':'jct-alashankou',  'label':'Alashankou (China border) — KCP entry',       'lat': 45.18,'lng': 82.57},
    # Gas pipeline junctions (rendered as pipeline_junction type on map)
    {'key':'jct-gorzyca',     'label':'Górzyca (Poland-Germany) — Yamal-Europe',     'lat': 52.55,'lng': 14.93},
    {'key':'jct-kipoi',       'label':'Kipoi (Greece) — TANAP / TAP junction',       'lat': 41.35,'lng': 26.14},
    {'key':'jct-kiyköy',      'label':'Kıyköy (Turkey) — TurkStream landfall',      'lat': 41.57,'lng': 27.96},
    {'key':'jct-erzurum',     'label':'Erzurum (Turkey) — TANAP transit',            'lat': 39.91,'lng': 41.28},
    {'key':'jct-blagoveshchensk','label':'Blagoveshchensk (Russia) — Power of Siberia','lat':50.27,'lng':127.54},
]

# ── Oil consumers (more granular) ──────────────────────────────────────────────
OIL_CONSUMERS = [
    {'key':'cons-china-e', 'label':'China E. Coast (Qingdao/Ningbo)',  'lat': 32.0,'lng':121.5,'kbd': 9000},
    {'key':'cons-china-s', 'label':'China S. Coast (Guangzhou/Huizhou)','lat':22.7,'lng':113.6,'kbd': 2800},
    {'key':'cons-india-w', 'label':'India West (Jamnagar/Mumbai)',      'lat': 22.5,'lng': 70.1,'kbd': 2900},
    {'key':'cons-india-e', 'label':'India East (Chennai/Paradip)',      'lat': 15.0,'lng': 80.3,'kbd': 2300},
    {'key':'cons-eu-nw',   'label':'NW Europe (Rotterdam/ARA)',         'lat': 51.9,'lng':  4.5,'kbd': 4500},
    {'key':'cons-eu-med',  'label':'S. Europe (Italy/Spain/Greece)',    'lat': 41.5,'lng': 12.5,'kbd': 2500},
    {'key':'cons-eu-ee',   'label':'E. Europe (Poland/Slovakia/Hungary)','lat':50.1,'lng': 19.9,'kbd': 1500},
    {'key':'cons-de',      'label':'Germany (Schwedt/Leuna)',           'lat': 52.1,'lng': 11.6,'kbd': 1200},
    {'key':'cons-usa-g',   'label':'USA Gulf Coast (Houston/NOLA)',     'lat': 29.8,'lng':-93.9,'kbd': 3500},
    {'key':'cons-usa-e',   'label':'USA East Coast (NY/Philadelphia)',  'lat': 39.9,'lng':-74.8,'kbd': 1500},
    {'key':'cons-japan',   'label':'Japan (Yokohama/Chiba)',            'lat': 35.5,'lng':139.7,'kbd': 3200},
    {'key':'cons-kor',     'label':'S. Korea (Ulsan/Busan)',            'lat': 35.5,'lng':129.4,'kbd': 2700},
    {'key':'cons-sgp',     'label':'Singapore (Jurong Island)',         'lat':  1.3,'lng':103.7,'kbd': 1200},
]

# ── Oil edges ──────────────────────────────────────────────────────────────────
OIL_EDGES = [
    # ── Saudi Arabia ─────────────────────────────────────────────────
    {'key':None,             'src':'prod-sau','dst':'chk-hormuz',  'kbd': 9800,'type':'maritime','label':'Saudi (Ras Tanura) → Hormuz'},
    # Saudi East-West pipeline bypasses Hormuz → Red Sea (Yanbu)
    {'key':'pipe-east-west', 'src':'prod-sau','dst':'jct-yanbu',   'kbd': 5000,'type':'pipeline','label':'Saudi East-West Pipeline → Yanbu'},
    {'key':None,             'src':'jct-yanbu','dst':'chk-bab',    'kbd': 5000,'type':'maritime','label':'Yanbu → Bab-el-Mandeb'},
    # ── Iraq ─────────────────────────────────────────────────────────
    {'key':None,             'src':'prod-irq', 'dst':'chk-hormuz', 'kbd': 3900,'type':'maritime','label':'Iraq (Basra) → Hormuz'},
    # ── UAE, Kuwait, Iran, Oman ────────────────────────────────────
    {'key':None, 'src':'prod-uae','dst':'chk-hormuz','kbd':3200,'type':'maritime','label':'UAE (Fujairah) → Hormuz'},
    {'key':None, 'src':'prod-kwt','dst':'chk-hormuz','kbd':2200,'type':'maritime','label':'Kuwait → Hormuz'},
    {'key':None, 'src':'prod-irn','dst':'chk-hormuz','kbd':1500,'type':'maritime','label':'Iran (Kharg Island) → Hormuz'},
    {'key':None, 'src':'prod-omn','dst':'chk-hormuz','kbd': 900,'type':'maritime','label':'Oman → Hormuz'},
    # ── Hormuz routing ──────────────────────────────────────────────
    {'key':None, 'src':'chk-hormuz','dst':'chk-malacca','kbd':16000,'type':'maritime','label':'Hormuz → Malacca (Asia-bound)'},
    {'key':None, 'src':'chk-hormuz','dst':'chk-bab',    'kbd': 8000,'type':'maritime','label':'Hormuz → Red Sea (West-bound)'},
    {'key':None, 'src':'chk-hormuz','dst':'chk-capegood','kbd':3000,'type':'maritime','label':'Hormuz → Cape (bypass)'},
    # ── Malacca → Asian consumers ──────────────────────────────────
    {'key':None, 'src':'chk-malacca','dst':'cons-china-e','kbd':9000,'type':'maritime','label':'Malacca → China East'},
    {'key':None, 'src':'chk-malacca','dst':'cons-china-s','kbd':2800,'type':'maritime','label':'Malacca → China South'},
    {'key':None, 'src':'chk-malacca','dst':'cons-japan',  'kbd':3200,'type':'maritime','label':'Malacca → Japan'},
    {'key':None, 'src':'chk-malacca','dst':'cons-kor',    'kbd':2700,'type':'maritime','label':'Malacca → Korea'},
    {'key':None, 'src':'chk-malacca','dst':'cons-india-e','kbd':1500,'type':'maritime','label':'Malacca → India East'},
    {'key':None, 'src':'chk-malacca','dst':'cons-sgp',    'kbd':1200,'type':'maritime','label':'Malacca → Singapore'},
    # ── Red Sea → Suez / Cape ──────────────────────────────────────
    {'key':None,         'src':'chk-bab','dst':'chk-suez',      'kbd':4600,'type':'maritime','label':'Bab-el-Mandeb → Suez'},
    {'key':None,         'src':'chk-bab','dst':'chk-capegood',  'kbd':2000,'type':'maritime','label':'Red Sea → Cape (bypass)'},
    {'key':'pipe-sumed', 'src':'chk-bab','dst':'chk-gibraltar', 'kbd':2400,'type':'pipeline','label':'SUMED Pipeline (Egypt)'},
    {'key':None,         'src':'chk-suez','dst':'chk-gibraltar','kbd':4600,'type':'maritime','label':'Suez → Gibraltar (Med)'},
    # ── BTC Pipeline (Baku–Tbilisi–Ceyhan) via Georgia ───────────
    {'key':'pipe-btc-1', 'src':'prod-aze',    'dst':'jct-tbilisi', 'kbd':1000,'type':'pipeline','label':'BTC: Sangachal (Azerbaijan) → Tbilisi (Georgia)'},
    {'key':'pipe-btc-2', 'src':'jct-tbilisi', 'dst':'jct-ceyhan',  'kbd':1000,'type':'pipeline','label':'BTC: Tbilisi (Georgia) → Ceyhan (Turkey)'},
    # ── Kirkuk–Ceyhan (Iraq northern fields → Turkey) ─────────────
    {'key':'pipe-ktc-iraq','src':'prod-irq-n',    'dst':'jct-fesh-khabur','kbd': 500,'type':'pipeline','label':'Kirkuk → Fesh Khabur (KTC, N. Iraq)'},
    {'key':'pipe-ktc-turk','src':'jct-fesh-khabur','dst':'jct-ceyhan',    'kbd': 500,'type':'pipeline','label':'Fesh Khabur → Ceyhan (KTC, Turkey)'},
    # ── Ceyhan export terminal → Med ──────────────────────────────
    {'key':None,         'src':'jct-ceyhan','dst':'chk-gibraltar','kbd':1700,'type':'maritime','label':'Ceyhan → Gibraltar (Med tankers)'},
    {'key':None,         'src':'jct-ceyhan','dst':'cons-eu-med', 'kbd': 800,'type':'maritime','label':'Ceyhan → S. Europe (direct)'},
    # ── Bosphorus / Black Sea ──────────────────────────────────────
    {'key':None, 'src':'chk-bosphorus','dst':'chk-gibraltar','kbd':3000,'type':'maritime','label':'Bosphorus → Gibraltar'},
    # ── Gibraltar → NW Europe ─────────────────────────────────────
    {'key':None, 'src':'chk-gibraltar','dst':'cons-eu-nw', 'kbd':4500,'type':'maritime','label':'Gibraltar → NW Europe'},
    {'key':None, 'src':'chk-gibraltar','dst':'cons-eu-med','kbd':2500,'type':'maritime','label':'Gibraltar → S. Europe'},
    # ── Russia: Primorsk (Baltic terminal) ────────────────────────
    {'key':'pipe-rus-primorsk','src':'prod-rus','dst':'jct-primorsk','kbd':3000,'type':'pipeline','label':'Russia → Primorsk Baltic terminal (BPS-2)'},
    {'key':None,               'src':'jct-primorsk','dst':'chk-danish','kbd':2000,'type':'maritime','label':'Primorsk → Baltic (Danish Straits)'},
    # ── Russia: Novorossiysk (Black Sea terminal) ─────────────────
    {'key':'pipe-rus-novorss', 'src':'prod-rus','dst':'jct-novorss','kbd':1500,'type':'pipeline','label':'Russia → Novorossiysk (Black Sea)'},
    {'key':'pipe-kcp-1',       'src':'prod-kaz',       'dst':'jct-atyrau',     'kbd':1700,'type':'pipeline','label':'Kazakhstan → Atyrau hub (CPC + KCP combined)'},
    {'key':'pipe-cpc-2',       'src':'jct-atyrau',     'dst':'jct-novorss',    'kbd':1400,'type':'pipeline','label':'CPC: Atyrau → Novorossiysk (Black Sea)'},
    {'key':'pipe-kcp-2',       'src':'jct-atyrau',     'dst':'jct-alashankou', 'kbd': 300,'type':'pipeline','label':'KCP: Atyrau → Alashankou (Kazakhstan-China)'},
    {'key':'pipe-kcp-3',       'src':'jct-alashankou', 'dst':'cons-china-e',   'kbd': 300,'type':'pipeline','label':'KCP: Alashankou → Dushanzi refinery (China)'},
    {'key':None,               'src':'jct-novorss','dst':'chk-bosphorus','kbd':3000,'type':'maritime','label':'Novorossiysk → Bosphorus'},
    # ── Russia: ESPO pipeline (Eastern Siberia → Pacific) ─────────
    {'key':'pipe-espo-1',    'src':'prod-rus',        'dst':'jct-taishet',     'kbd':1600,'type':'pipeline','label':'Russia → ESPO (Taishet origin)'},
    {'key':'pipe-espo-2',    'src':'jct-taishet',     'dst':'jct-skovorodino', 'kbd':1600,'type':'pipeline','label':'ESPO trunk (Taishet → Skovorodino)'},
    {'key':'pipe-espo-china','src':'jct-skovorodino', 'dst':'cons-china-e',    'kbd': 300,'type':'pipeline','label':'ESPO China spur (Skovorodino → Daqing, 300 kbd)'},
    {'key':'pipe-espo-3',    'src':'jct-skovorodino', 'dst':'jct-kozmino',     'kbd':1000,'type':'pipeline','label':'ESPO (Skovorodino → Kozmino Pacific terminal)'},
    {'key':None,             'src':'jct-kozmino','dst':'cons-china-e','kbd': 800,'type':'maritime','label':'Kozmino → China East (Pacific tankers)'},
    {'key':None,             'src':'jct-kozmino','dst':'cons-japan',  'kbd': 400,'type':'maritime','label':'Kozmino → Japan'},
    {'key':None,             'src':'jct-kozmino','dst':'cons-kor',    'kbd': 300,'type':'maritime','label':'Kozmino → Korea'},
    # ── Druzhba Pipeline System (Russia → EU via Belarus) ─────────
    # Trunk routes through chk-druzhba chokepoint (Unecha, Russia-Belarus border)
    {'key':None,              'src':'prod-rus',    'dst':'chk-druzhba','kbd':2200,'type':'pipeline','label':'Russia → Druzhba pipeline (Unecha)'},
    {'key':None,              'src':'chk-druzhba', 'dst':'jct-mozyr',  'kbd':9999,'type':'pipeline','label':'Druzhba → Mozyr (Belarus) split point'},
    # Northern branch: Mozyr → Płock → Schwedt/Gdańsk
    {'key':'pipe-druzhba-n1',   'src':'jct-mozyr',   'dst':'jct-plock',    'kbd':1200,'type':'pipeline','label':'Druzhba North → Płock (Poland)'},
    {'key':'pipe-druzhba-n2',   'src':'jct-plock',   'dst':'jct-schwedt',  'kbd': 700,'type':'pipeline','label':'Druzhba North → Schwedt (Germany)'},
    {'key':'pipe-druzhba-n3',   'src':'jct-plock',   'dst':'jct-gdansk',   'kbd': 500,'type':'pipeline','label':'Druzhba → Gdańsk Naftoport'},
    {'key':'pipe-druzhba-n4',   'src':'jct-schwedt', 'dst':'cons-de',      'kbd': 700,'type':'pipeline','label':'Schwedt → German refineries'},
    {'key':'pipe-druzhba-n5',   'src':'jct-gdansk',  'dst':'cons-eu-nw',   'kbd': 300,'type':'pipeline','label':'Gdańsk → NW European market'},
    {'key':'pipe-druzhba-pl',   'src':'jct-plock',   'dst':'cons-eu-ee',   'kbd': 500,'type':'pipeline','label':'Płock → Polish refineries'},
    # Southern branch: Mozyr → Brody → Bratislava → Budapest
    {'key':'pipe-druzhba-s1',   'src':'jct-mozyr',     'dst':'jct-brody',     'kbd':1000,'type':'pipeline','label':'Druzhba South → Brody (Ukraine)'},
    {'key':'pipe-druzhba-s2',   'src':'jct-brody',     'dst':'jct-bratislava','kbd': 400,'type':'pipeline','label':'Druzhba South → Bratislava (Slovakia)'},
    {'key':'pipe-druzhba-s3',   'src':'jct-brody',     'dst':'cons-eu-ee',    'kbd': 600,'type':'pipeline','label':'Druzhba → Ukrainian / Czech refineries'},
    {'key':'pipe-druzhba-s4',   'src':'jct-bratislava','dst':'jct-budapest',  'kbd': 200,'type':'pipeline','label':'Druzhba → Százhalombatta (Hungary)'},
    {'key':'pipe-druzhba-s5',   'src':'jct-bratislava','dst':'cons-eu-ee',    'kbd': 200,'type':'pipeline','label':'Bratislava → Slovak refineries'},
    {'key':'pipe-druzhba-s6',   'src':'jct-budapest',  'dst':'cons-eu-ee',    'kbd': 200,'type':'pipeline','label':'Százhalombatta → Hungarian market'},
    # ── Danish Straits → NW Europe ────────────────────────────────
    {'key':None, 'src':'chk-danish','dst':'cons-eu-nw','kbd':2000,'type':'maritime','label':'Baltic → NW Europe'},
    # ── Norway ────────────────────────────────────────────────────
    {'key':None, 'src':'prod-nor','dst':'chk-danish','kbd':1300,'type':'maritime','label':'Norway North Sea → Baltic'},
    {'key':None, 'src':'prod-nor','dst':'cons-eu-nw', 'kbd': 800,'type':'maritime','label':'Norway → NW Europe (direct)'},
    {'key':None, 'src':'prod-uk', 'dst':'cons-eu-nw', 'kbd': 700,'type':'maritime','label':'UK North Sea → NW Europe'},
    # ── Libya / Algeria / Angola ───────────────────────────────────
    {'key':None, 'src':'prod-lby','dst':'cons-eu-med','kbd':1100,'type':'maritime','label':'Libya → S. Europe (Med)'},
    {'key':None, 'src':'prod-alg','dst':'cons-eu-med','kbd': 800,'type':'maritime','label':'Algeria → S. Europe (Med)'},
    {'key':None, 'src':'prod-alg','dst':'chk-gibraltar','kbd': 500,'type':'maritime','label':'Algeria → Gibraltar'},
    {'key':None, 'src':'prod-ago','dst':'chk-capegood','kbd': 800,'type':'maritime','label':'Angola → Cape'},
    {'key':None, 'src':'prod-ago','dst':'chk-bab',    'kbd': 400,'type':'maritime','label':'Angola → Bab (Indian Ocean route)'},
    # ── Nigeria ────────────────────────────────────────────────────
    {'key':None, 'src':'prod-nga','dst':'chk-gibraltar','kbd':1400,'type':'maritime','label':'Nigeria → Gibraltar (Atlantic)'},
    {'key':None, 'src':'prod-nga','dst':'chk-capegood', 'kbd': 500,'type':'maritime','label':'Nigeria → Cape (southern)'},
    # ── Cape of Good Hope routing ──────────────────────────────────
    {'key':None, 'src':'chk-capegood','dst':'cons-eu-nw',  'kbd':2000,'type':'maritime','label':'Cape → NW Europe'},
    {'key':None, 'src':'chk-capegood','dst':'cons-eu-med', 'kbd':1000,'type':'maritime','label':'Cape → S. Europe'},
    {'key':None, 'src':'chk-capegood','dst':'cons-china-e','kbd':3000,'type':'maritime','label':'Cape → China East'},
    {'key':None, 'src':'chk-capegood','dst':'cons-india-w','kbd':2000,'type':'maritime','label':'Cape → India West'},
    {'key':None, 'src':'chk-capegood','dst':'cons-japan',  'kbd':1000,'type':'maritime','label':'Cape → Japan'},
    # ── Americas ───────────────────────────────────────────────────
    {'key':None, 'src':'prod-usa','dst':'cons-usa-g',  'kbd':3000,'type':'maritime','label':'USA Gulf (domestic)'},
    {'key':None, 'src':'prod-usa','dst':'cons-eu-nw',  'kbd': 800,'type':'maritime','label':'USA → NW Europe'},
    {'key':None, 'src':'prod-usa','dst':'chk-panama',  'kbd': 800,'type':'maritime','label':'USA Gulf → Panama'},
    {'key':None, 'src':'prod-mex','dst':'cons-usa-g',  'kbd':1200,'type':'maritime','label':'Mexico → USA Gulf'},
    {'key':None, 'src':'prod-mex','dst':'chk-panama',  'kbd': 400,'type':'maritime','label':'Mexico → Panama'},
    {'key':None, 'src':'prod-can','dst':'cons-usa-e',  'kbd': 600,'type':'maritime','label':'Canada → USA East Coast'},
    {'key':None, 'src':'prod-can','dst':'cons-eu-nw',  'kbd': 500,'type':'maritime','label':'Canada → NW Europe'},
    {'key':None, 'src':'prod-ven','dst':'cons-usa-g',  'kbd': 500,'type':'maritime','label':'Venezuela → USA Gulf'},
    {'key':None, 'src':'prod-ven','dst':'cons-eu-nw',  'kbd': 200,'type':'maritime','label':'Venezuela → Europe'},
    {'key':None, 'src':'prod-bra','dst':'cons-usa-g',  'kbd': 400,'type':'maritime','label':'Brazil → USA'},
    {'key':None, 'src':'prod-bra','dst':'cons-eu-nw',  'kbd': 600,'type':'maritime','label':'Brazil → Europe'},
    {'key':None, 'src':'chk-panama','dst':'cons-japan','kbd': 500,'type':'maritime','label':'Panama → Japan'},
    {'key':None, 'src':'chk-panama','dst':'cons-kor',  'kbd': 300,'type':'maritime','label':'Panama → Korea'},
    {'key':None, 'src':'chk-panama','dst':'cons-usa-e','kbd': 300,'type':'maritime','label':'Panama → USA East'},
    # ── India west ─────────────────────────────────────────────────
    {'key':None, 'src':'chk-bab','dst':'cons-india-w','kbd':1000,'type':'maritime','label':'Red Sea → India West'},
]

# ── Gas producers & LNG export terminals ──────────────────────────────────────
GAS_PRODUCERS = [
    {'key':'gas-qatar',  'label':'Qatar LNG (Ras Laffan)', 'lat': 25.90,'lng': 51.50,'bcm':107,'type':'lng_export'},
    {'key':'gas-usa-lng','label':'USA LNG (Sabine Pass)',   'lat': 29.70,'lng':-93.90,'bcm': 90,'type':'lng_export'},
    {'key':'gas-aus',    'label':'Australia LNG',            'lat':-20.70,'lng':116.80,'bcm': 80,'type':'lng_export'},
    {'key':'gas-rus',    'label':'Russia (Yamal Gas)',       'lat': 68.00,'lng': 68.00,'bcm':200,'type':'gas_producer'},
    {'key':'gas-nor',    'label':'Norway Gas (offshore)',    'lat': 61.00,'lng':  2.50,'bcm':110,'type':'gas_producer'},
    {'key':'gas-nga-lng','label':'Nigeria LNG (Bonny Is.)', 'lat':  4.40,'lng':  7.20,'bcm': 25,'type':'lng_export'},
    {'key':'gas-alg',    'label':'Algeria Gas (Hassi R.)',  'lat': 26.00,'lng':  6.00,'bcm': 40,'type':'gas_producer'},
    {'key':'gas-aze',    'label':'Azerbaijan (Shah Deniz)', 'lat': 39.00,'lng': 49.50,'bcm': 17,'type':'gas_producer'},
    {'key':'gas-usa-pipe','label':'USA (Appalachian gas)',  'lat': 38.00,'lng':-81.00,'bcm': 50,'type':'gas_producer'},
    {'key':'gas-malaysia','label':'Malaysia LNG (Bintulu)', 'lat':  3.23,'lng':113.07,'bcm': 42,'type':'lng_export'},
    {'key':'gas-sabetta', 'label':'Yamal LNG (Sabetta)',    'lat': 71.26,'lng': 72.10,'bcm': 24,'type':'lng_export'},
]

LNG_IMPORTS = [
    {'key':'lng-eu-med','label':'EU Med LNG (Spain/France/It.)','lat':41.40,'lng':  2.20,'bcm':65,'type':'lng_import','consumer':'cons-eu-nw'},
    {'key':'lng-eu-uk', 'label':'UK LNG (Isle of Grain)',        'lat':51.40,'lng':  0.60,'bcm':30,'type':'lng_import','consumer':'cons-eu-nw'},
    {'key':'lng-japan', 'label':'Japan LNG (Tokyo/Yokohama)',    'lat':35.60,'lng':139.80,'bcm':100,'type':'lng_import','consumer':'cons-japan'},
    {'key':'lng-korea', 'label':'Korea LNG (Pyeongtaek/Incheon)','lat':37.00,'lng':126.70,'bcm':60,'type':'lng_import','consumer':'cons-kor'},
    {'key':'lng-china', 'label':'China LNG (Tianjin/Tangshan)',  'lat':39.00,'lng':117.70,'bcm':80,'type':'lng_import','consumer':'cons-china-e'},
    {'key':'lng-india', 'label':'India LNG (Dahej/Hazira)',      'lat':21.70,'lng': 72.60,'bcm':40,'type':'lng_import','consumer':'cons-india-w'},
    {'key':'lng-sgp',        'label':'Singapore LNG (Jurong)',        'lat':  1.27,'lng':103.75,'bcm': 15,'type':'lng_import','consumer':'cons-sgp'},
    {'key':'lng-eu-belgium', 'label':'Zeebrugge LNG (Belgium)',     'lat': 51.34,'lng':  3.21,'bcm':  9,'type':'lng_import','consumer':'cons-eu-nw'},
    {'key':'lng-eu-greece',  'label':'Revithoussa LNG (Greece)',     'lat': 37.94,'lng': 23.35,'bcm': 12,'type':'lng_import','consumer':'cons-eu-med'},
]

GAS_CONSUMER_DEMAND = {
    'cons-eu-nw':450, 'cons-eu-med':150, 'cons-eu-ee':100,
    'cons-japan':110, 'cons-kor':65, 'cons-china-e':160,
    'cons-india-w':50, 'cons-sgp':18, 'cons-usa-g':55,
}

# ── Maritime waypoints (intermediate lat/lng to route around land) ─────────────
# Key format: 'src_key|dst_key'  Values: [[lat,lng], ...] in normal -180..180 coords.
# The JS normalizeAntimeridian() stitches consecutive points into a continuous line
# on the Leaflet Mercator map, so Pacific routes that cross -180/+180 work correctly.
MARITIME_WAYPOINTS = {
    # Indian Ocean — avoid Indian subcontinent
    'chk-hormuz|chk-malacca':  [[20,62],[13,66],[8,74],[4,82],[2,96]],
    'chk-hormuz|chk-capegood': [[20,62],[12,60],[5,52],[-5,48],[-20,44],[-30,34]],
    # Red Sea / East Africa
    'chk-bab|chk-capegood':    [[6,48],[-2,46],[-12,44],[-22,40],[-30,34]],
    'chk-bab|cons-india-w':    [[14,52],[18,60],[20,67]],
    'jct-yanbu|chk-bab':       [[22,40],[16,43]],
    # Mediterranean — avoid North Africa / Southern Europe land cuts
    'chk-suez|chk-gibraltar':  [[32,28],[35,18],[37,6],[36.5,-2]],
    'jct-ceyhan|chk-gibraltar':[[37,30],[37,20],[37,10],[37,0],[36.5,-4]],
    'jct-ceyhan|cons-eu-med':  [[37,30],[38,24],[40,18],[41.5,14]],
    'chk-bosphorus|chk-gibraltar':[[40,26],[38,20],[37,10],[37,0],[36.5,-3]],
    # Cape → East (around Africa's east coast then Indian Ocean)
    'chk-capegood|cons-china-e':[[-28,36],[-14,42],[-2,46],[5,50],[10,60],[8,74],[4,82],[8,100],[16,114]],
    'chk-capegood|cons-india-w':[[-28,36],[-14,42],[-2,46],[5,50],[10,62],[16,68]],
    'chk-capegood|cons-japan':  [[-28,36],[-14,42],[-2,46],[5,50],[10,60],[8,74],[4,82],[8,100],[20,122],[30,136]],
    'chk-capegood|lng-india':   [[-28,36],[-14,42],[-2,46],[5,50],[10,58],[16,70]],
    # Cape → West (around Africa's west coast into Atlantic)
    'chk-capegood|cons-eu-nw':  [[-25,13],[-12,6],[-2,0],[5,-6],[16,-18],[28,-16],[40,-12],[48,-6],[51,3]],
    'chk-capegood|cons-eu-med': [[-25,13],[-12,6],[-2,0],[5,-6],[16,-18],[28,-14],[36,-8],[38,2],[40,8]],
    'chk-capegood|lng-eu-med':  [[-25,13],[-12,6],[-2,0],[5,-6],[16,-18],[28,-14],[36,-8],[38,2],[40,8]],
    # West Africa → Cape (hug coastline)
    'prod-nga|chk-capegood':   [[2,5],[0,4],[-8,8],[-16,11],[-26,15]],
    'prod-ago|chk-capegood':   [[-10,12],[-18,13],[-26,16]],
    'prod-ago|chk-bab':        [[-12,10],[-22,16],[-30,28],[-28,36],[-18,42],[-5,46],[6,46]],
    'gas-nga-lng|chk-capegood':[[2,5],[0,4],[-8,8],[-16,11],[-26,15]],
    # West Africa → Gibraltar / Atlantic (avoid African bulge at ~15°W)
    'prod-nga|chk-gibraltar':  [[5,5],[8,-2],[15,-18],[25,-16],[33,-8]],
    'gas-nga-lng|chk-gibraltar':[[5,5],[8,-2],[15,-18],[25,-15],[33,-8]],
    # Americas
    'prod-usa|chk-panama':     [[24,-88],[16,-85],[12,-82]],
    'prod-mex|chk-panama':     [[14,-88],[12,-84]],
    'prod-usa|cons-eu-nw':     [[28,-82],[34,-74],[40,-55],[44,-30],[48,-15],[51,3]],
    'prod-bra|cons-eu-nw':     [[-14,-36],[-5,-28],[5,-22],[15,-22],[28,-18],[40,-12],[48,-6],[51,3]],
    'gas-usa-lng|chk-gibraltar':[[27,-88],[27,-80],[33,-74],[38,-40],[37,-10]],
    'gas-usa-lng|chk-panama':  [[27,-88],[22,-87],[16,-85],[12,-82]],
    # Trans-Pacific: use real Pacific coords; normalizeAntimeridian() in JS fixes the wrap
    'chk-panama|cons-japan':   [[6,-88],[0,-110],[-5,-140],[0,-165],[5,170],[20,152],[30,142]],
    'chk-panama|cons-kor':     [[6,-88],[0,-110],[-5,-140],[0,-165],[5,170],[20,148],[31,130]],
    'chk-panama|lng-japan':    [[6,-88],[0,-110],[-5,-140],[0,-165],[5,170],[20,152],[30,142]],
    'chk-panama|lng-korea':    [[6,-88],[0,-110],[-5,-140],[0,-165],[5,170],[20,148],[31,130]],
    # Baltic
    'jct-primorsk|chk-danish': [[60,24],[58,22],[57,18],[57,14.5]],
    # Australia LNG → Malacca (avoid Australian interior)
    'gas-aus|chk-malacca':     [[-15,112],[-10,108],[-3,104]],
    # Yamal LNG (Arctic routes)
    'gas-sabetta|lng-eu-belgium':[[74,55],[70,40],[65,25],[58,16],[52,5]],
    'gas-sabetta|lng-japan':   [[76,85],[75,108],[72,132],[60,148],[48,155],[38,142]],
    'gas-sabetta|lng-china':   [[76,85],[75,108],[72,130],[58,130],[44,122]],
}

GAS_EDGES = [
    # ── Overland gas pipelines ─────────────────────────────────────
    {'key':'gpipe-nor-eu',      'src':'gas-nor',    'dst':'cons-eu-nw', 'bcm':100,'type':'gas_pipeline','label':'Norway → EU (Europipe/Langeled/Franpipe)'},
    # ── Algeria → Europe ──────────────────────────────────────────
    {'key':'gpipe-transmed',    'src':'gas-alg',    'dst':'cons-eu-med','bcm': 30,'type':'gas_pipeline','label':'Trans-Mediterranean: Algeria → Tunisia → Sicily → Italy'},
    {'key':'gpipe-medgaz',      'src':'gas-alg',    'dst':'cons-eu-nw', 'bcm':  8,'type':'gas_pipeline','label':'Medgaz: Algeria → Spain (direct subsea)'},
    # ── Southern Gas Corridor (Azerbaijan → Italy via TANAP + TAP) ─
    {'key':'gpipe-tanap-1',     'src':'gas-aze',    'dst':'jct-erzurum','bcm': 10,'type':'gas_pipeline','label':'TANAP: Azerbaijan → Erzurum (Turkey)'},
    {'key':'gpipe-tanap-2',     'src':'jct-erzurum','dst':'jct-kipoi',  'bcm': 10,'type':'gas_pipeline','label':'TANAP: Erzurum → Kipoi (Greece border)'},
    {'key':'gpipe-tap',         'src':'jct-kipoi',  'dst':'cons-eu-med','bcm': 10,'type':'gas_pipeline','label':'TAP: Kipoi → Melendugno (Italy)'},
    # ── Russia → E. Europe pipelines ──────────────────────────────
    {'key':None,                'src':'gas-rus',     'dst':'chk-druzhba','bcm': 30,'type':'gas_pipeline','label':'Russia → Druzhba gas corridor (Unecha)'},
    {'key':'gpipe-druzhba-g',   'src':'chk-druzhba', 'dst':'cons-eu-ee', 'bcm': 30,'type':'gas_pipeline','label':'Brotherhood Pipeline → E. Europe'},
    {'key':'gpipe-turk-1',      'src':'gas-rus',    'dst':'jct-kiyköy', 'bcm': 32,'type':'gas_pipeline','label':'TurkStream: Anapa (Russia) → Kıyköy (Turkey, Black Sea)'},
    {'key':'gpipe-turk-2',      'src':'jct-kiyköy', 'dst':'cons-eu-ee', 'bcm': 16,'type':'gas_pipeline','label':'TurkStream: Kıyköy → Balkans (Bg/Srb/Hu/Sk/At)'},
    # ── Yamal-Europe pipeline ──────────────────────────────────────
    {'key':'gpipe-yamal-1',     'src':'gas-rus',    'dst':'jct-gorzyca','bcm': 33,'type':'gas_pipeline','label':'Yamal-Europe: Russia → Belarus → Poland → Górzyca'},
    {'key':'gpipe-yamal-2',     'src':'jct-gorzyca','dst':'cons-eu-nw', 'bcm': 33,'type':'gas_pipeline','label':'Yamal-Europe: Górzyca border → Germany'},
    # ── Nord Stream 1 ──────────────────────────────────────────────
    {'key':'gpipe-nord-stream', 'src':'gas-rus',    'dst':'lng-eu-uk',  'bcm': 55,'type':'gas_pipeline','label':'Nord Stream 1 (Russia → Lubmin, Germany)'},
    # ── Power of Siberia (Russia → China) ─────────────────────────
    {'key':'gpipe-pos-1',       'src':'gas-rus',    'dst':'jct-blagoveshchensk','bcm': 38,'type':'gas_pipeline','label':'Power of Siberia: Russia → Blagoveshchensk border'},
    {'key':'gpipe-pos-2',       'src':'jct-blagoveshchensk','dst':'cons-china-e','bcm': 38,'type':'gas_pipeline','label':'Power of Siberia: China (→ Songyuan / Changchun)'},
    # ── US domestic ───────────────────────────────────────────────
    {'key':'gpipe-us-domestic', 'src':'gas-usa-pipe','dst':'cons-usa-g','bcm': 50,'type':'gas_pipeline','label':'US domestic gas pipelines'},
    # ── Qatar LNG — must pass through Hormuz ──────────────────────
    {'key':None,'src':'gas-qatar','dst':'chk-hormuz',  'bcm':107,'type':'lng_maritime','label':'Qatar LNG → Hormuz'},
    {'key':None,'src':'chk-hormuz','dst':'chk-malacca','bcm': 60,'type':'lng_maritime','label':'Hormuz → Malacca (LNG)'},
    {'key':None,'src':'chk-hormuz','dst':'chk-bab',    'bcm': 40,'type':'lng_maritime','label':'Hormuz → Red Sea (LNG)'},
    {'key':None,'src':'chk-malacca','dst':'lng-japan', 'bcm': 50,'type':'lng_maritime','label':'Malacca → Japan LNG'},
    {'key':None,'src':'chk-malacca','dst':'lng-korea', 'bcm': 30,'type':'lng_maritime','label':'Malacca → Korea LNG'},
    {'key':None,'src':'chk-malacca','dst':'lng-china', 'bcm': 40,'type':'lng_maritime','label':'Malacca → China LNG'},
    {'key':None,'src':'chk-malacca','dst':'lng-sgp',   'bcm': 15,'type':'lng_maritime','label':'Malacca → Singapore LNG'},
    {'key':None,'src':'chk-bab','dst':'chk-suez',      'bcm': 25,'type':'lng_maritime','label':'Red Sea → Suez (LNG)'},
    {'key':None,'src':'chk-suez','dst':'lng-eu-med',   'bcm': 25,'type':'lng_maritime','label':'Suez → EU Med LNG'},
    {'key':None,'src':'chk-bab','dst':'chk-capegood',  'bcm': 10,'type':'lng_maritime','label':'Red Sea → Cape (LNG bypass)'},
    {'key':None,'src':'chk-capegood','dst':'lng-eu-med','bcm':10,'type':'lng_maritime','label':'Cape → EU Med LNG'},
    {'key':None,'src':'chk-bab','dst':'lng-india',     'bcm': 12,'type':'lng_maritime','label':'Red Sea → India LNG'},
    # ── Australia LNG → Asia via Malacca ──────────────────────────
    {'key':None,'src':'gas-aus',     'dst':'chk-malacca','bcm': 80,'type':'lng_maritime','label':'Australia LNG → Malacca'},
    # ── Malaysia LNG (Bintulu) → Asia via Malacca ─────────────────
    {'key':None,'src':'gas-malaysia','dst':'chk-malacca','bcm': 42,'type':'lng_maritime','label':'Malaysia LNG (Bintulu) → Malacca'},
    # ── Yamal LNG (Sabetta) → Europe + Asia ──────────────────────
    {'key':None,'src':'gas-sabetta', 'dst':'lng-eu-belgium','bcm': 8,'type':'lng_maritime','label':'Yamal LNG → Zeebrugge (ice-class tankers)'},
    {'key':None,'src':'gas-sabetta', 'dst':'lng-japan',     'bcm': 6,'type':'lng_maritime','label':'Yamal LNG → Japan (Arctic route)'},
    {'key':None,'src':'gas-sabetta', 'dst':'lng-china',     'bcm': 6,'type':'lng_maritime','label':'Yamal LNG → China'},
    # ── USA LNG ────────────────────────────────────────────────────
    {'key':None,'src':'gas-usa-lng','dst':'chk-panama',   'bcm':30,'type':'lng_maritime','label':'USA LNG → Panama (Pacific)'},
    {'key':None,'src':'gas-usa-lng','dst':'chk-gibraltar','bcm':40,'type':'lng_maritime','label':'USA LNG → Gibraltar (Atlantic)'},
    {'key':None,'src':'chk-panama','dst':'lng-japan','bcm':15,'type':'lng_maritime','label':'Panama → Japan LNG'},
    {'key':None,'src':'chk-panama','dst':'lng-korea','bcm':15,'type':'lng_maritime','label':'Panama → Korea LNG'},
    {'key':None,'src':'chk-gibraltar','dst':'lng-eu-med','bcm':20,'type':'lng_maritime','label':'Gibraltar → EU Med LNG'},
    {'key':None,'src':'chk-gibraltar','dst':'lng-eu-uk', 'bcm':20,'type':'lng_maritime','label':'Gibraltar → UK LNG'},
    # ── Nigeria LNG ────────────────────────────────────────────────
    {'key':None,'src':'gas-nga-lng','dst':'chk-gibraltar','bcm':15,'type':'lng_maritime','label':'Nigeria LNG → Gibraltar'},
    {'key':None,'src':'gas-nga-lng','dst':'chk-capegood', 'bcm':10,'type':'lng_maritime','label':'Nigeria LNG → Cape'},
    {'key':None,'src':'chk-capegood','dst':'lng-india',   'bcm':10,'type':'lng_maritime','label':'Cape → India LNG'},
    # ── LNG terminal → consumer (last-mile) ───────────────────────
    {'key':None,'src':'lng-eu-med','dst':'cons-eu-nw', 'bcm': 65,'type':'lng_delivery','label':'EU Med LNG → EU grid'},
    {'key':None,'src':'lng-eu-uk', 'dst':'cons-eu-nw', 'bcm': 30,'type':'lng_delivery','label':'UK LNG → EU grid'},
    {'key':None,'src':'lng-japan', 'dst':'cons-japan', 'bcm':100,'type':'lng_delivery','label':'Japan LNG grid'},
    {'key':None,'src':'lng-korea', 'dst':'cons-kor',   'bcm': 60,'type':'lng_delivery','label':'Korea LNG grid'},
    {'key':None,'src':'lng-china', 'dst':'cons-china-e','bcm':80,'type':'lng_delivery','label':'China LNG grid'},
    {'key':None,'src':'lng-india', 'dst':'cons-india-w','bcm':40,'type':'lng_delivery','label':'India LNG grid'},
    {'key':None,'src':'lng-sgp',        'dst':'cons-sgp',   'bcm': 15,'type':'lng_delivery','label':'Singapore LNG grid'},
    {'key':None,'src':'lng-eu-belgium', 'dst':'cons-eu-nw', 'bcm':  9,'type':'lng_delivery','label':'Zeebrugge → EU grid'},
    {'key':None,'src':'lng-eu-greece',  'dst':'cons-eu-med','bcm': 12,'type':'lng_delivery','label':'Revithoussa → EU Med grid'},
]

# ── Timeline snapshots ─────────────────────────────────────────────────────────
TIMELINE_SNAPSHOTS = {
    '2021-01': {
        'label': '2021 Q1 — Global Baseline',
        'description': 'Pre-crisis baseline. All Druzhba branches, pipelines, and maritime routes at full capacity.',
        'oil_overrides': {}, 'gas_overrides': {},
    },
    '2022-02': {
        'label': '2022-02 — Russia Invades Ukraine',
        'description': 'Sanctions begin. Druzhba volumes drop. Yamal-Europe pipeline stopped Apr 2022. Russia raises price but exports continue.',
        'oil_overrides': {'prod-rus':5000, 'chk-druzhba':1800, 'pipe-druzhba-n1':900, 'pipe-druzhba-s1':700},
        'gas_overrides': {'chk-druzhba':20, 'gpipe-turk-1':28, 'gpipe-yamal-1':15, 'gpipe-yamal-2':15},
    },
    '2022-09': {
        'label': '2022-09 — Nord Stream Sabotage',
        'description': 'Nord Stream 1 & 2 sabotaged (Sep 26, 2022). Yamal-Europe fully stopped since Apr. EU gas crisis deepens.',
        'oil_overrides': {'prod-rus':4800, 'chk-druzhba':1600, 'pipe-druzhba-n1':700, 'pipe-druzhba-s1':800},
        'gas_overrides': {'gpipe-nord-stream':0, 'chk-druzhba':12, 'gpipe-turk-1':25, 'gpipe-yamal-1':0, 'gpipe-yamal-2':0, 'gpipe-pos-1':20},
    },
    '2023-01': {
        'label': '2023-01 — EU Full Oil Embargo',
        'description': 'EU bans Russian seaborne oil. Druzhba northern branch to Germany/Poland collapses. Only HU/SK/CZ pipeline exemptions survive. Russia reroutes via shadow fleet to Asia.',
        'oil_overrides': {
            'prod-rus':5500,
            'chk-druzhba':600,  # total remaining Druzhba capacity (southern branch only)
            'pipe-druzhba-n1':0, 'pipe-druzhba-n2':0, 'pipe-druzhba-n3':0,
            'pipe-druzhba-n4':0, 'pipe-druzhba-n5':0, 'pipe-druzhba-pl':0,
            'pipe-druzhba-s1':600, 'pipe-druzhba-s2':350, 'pipe-druzhba-s3':250,
            'pipe-druzhba-s4':150, 'pipe-druzhba-s5':150, 'pipe-druzhba-s6':150,
            'pipe-rus-primorsk':0,
        },
        'gas_overrides': {'gpipe-nord-stream':0, 'chk-druzhba':0, 'gpipe-turk-1':32, 'gpipe-yamal-1':0, 'gpipe-yamal-2':0, 'gpipe-pos-1':25},
    },
    '2024-01': {
        'label': '2024-01 — Red Sea / Houthi Crisis',
        'description': 'Houthi attacks reduce Bab-el-Mandeb throughput by ~84%. LNG carriers add 14 days rerouting via Cape. Oil also partially reroutes.',
        'oil_overrides': {
            'prod-rus':5500,
            'chk-druzhba':600, 'pipe-druzhba-n1':0, 'pipe-druzhba-n2':0,
            'pipe-druzhba-n3':0, 'pipe-druzhba-n4':0, 'pipe-druzhba-pl':0,
            'pipe-druzhba-s1':600, 'pipe-druzhba-s2':350, 'pipe-druzhba-s3':250,
            'pipe-druzhba-s4':150, 'pipe-druzhba-s5':150, 'pipe-druzhba-s6':150,
            'pipe-rus-primorsk':0, 'chk-bab':1000,
        },
        'gas_overrides': {'gpipe-nord-stream':0, 'chk-druzhba':0, 'gpipe-yamal-1':0, 'gpipe-yamal-2':0, 'gpipe-turk-1':32, 'gpipe-pos-1':30, 'chk-bab':12},
    },
    '2025-01': {
        'label': '2025-01 — Status Quo',
        'description': 'Russian oil diverted to Asia via shadow fleet (Kozmino/Cape). EU supplied by Norway, USA LNG, MENA. Red Sea partially recovers. Power of Siberia at full contract.',
        'oil_overrides': {
            'prod-rus':5500,
            'chk-druzhba':600, 'pipe-druzhba-n1':0, 'pipe-druzhba-n2':0,
            'pipe-druzhba-n3':0, 'pipe-druzhba-n4':0, 'pipe-druzhba-pl':0,
            'pipe-druzhba-s1':600, 'pipe-druzhba-s2':350, 'pipe-druzhba-s3':250,
            'pipe-druzhba-s4':150, 'pipe-druzhba-s5':150, 'pipe-druzhba-s6':150,
            'pipe-rus-primorsk':0, 'chk-bab':3000,
        },
        'gas_overrides': {'gpipe-nord-stream':0, 'chk-druzhba':0, 'gpipe-yamal-1':0, 'gpipe-yamal-2':0, 'gpipe-turk-1':32, 'gpipe-pos-1':38},
    },
    '2026-05': {
        'label': '2026-05 — Iran War: Hormuz Blockade',
        'description': 'Iran War (2026). Strait of Hormuz closed. ~20% of global oil supply cut. Qatar LNG stranded — cross-commodity crisis hits Asia. Iraq reroutes via Kirkuk–Ceyhan (250 kbd).',
        'oil_overrides': {
            'prod-rus':5500,
            'chk-druzhba':600, 'pipe-druzhba-n1':0, 'pipe-druzhba-n2':0,
            'pipe-druzhba-n3':0, 'pipe-druzhba-n4':0, 'pipe-druzhba-pl':0,
            'pipe-druzhba-s1':600, 'pipe-druzhba-s2':350, 'pipe-druzhba-s3':250,
            'pipe-druzhba-s4':150, 'pipe-druzhba-s5':150, 'pipe-druzhba-s6':150,
            'pipe-rus-primorsk':0, 'chk-hormuz':0,
        },
        'gas_overrides': {'gpipe-nord-stream':0, 'chk-druzhba':0, 'gpipe-yamal-1':0, 'gpipe-yamal-2':0, 'gpipe-turk-1':32, 'gpipe-pos-1':38, 'chk-hormuz':0, 'gas-qatar':0},
    },
}

# ── Coordinate & baseline lookups ──────────────────────────────────────────────
_NODE_COORDS = {}
for _n in OIL_PRODUCERS:     _NODE_COORDS[_n['key']] = (_n['lat'], _n['lng'])
for _n in CHOKEPOINTS:        _NODE_COORDS[_n['key']] = (_n['lat'], _n['lng'])
for _n in OIL_CONSUMERS:      _NODE_COORDS[_n['key']] = (_n['lat'], _n['lng'])
for _n in GAS_PRODUCERS:      _NODE_COORDS[_n['key']] = (_n['lat'], _n['lng'])
for _n in LNG_IMPORTS:        _NODE_COORDS[_n['key']] = (_n['lat'], _n['lng'])
for _n in PIPELINE_JUNCTIONS: _NODE_COORDS[_n['key']] = (_n['lat'], _n['lng'])

_OIL_BASELINE = {}
for _p in OIL_PRODUCERS:  _OIL_BASELINE[_p['key']] = _p['kbd']
for _c in CHOKEPOINTS:     _OIL_BASELINE[_c['key']] = _c['normal_kbd']
for _j in PIPELINE_JUNCTIONS: pass  # junctions have no baseline capacity
for _e in OIL_EDGES:
    if _e['key']:  _OIL_BASELINE[_e['key']] = _e['kbd']

_GAS_BASELINE = {}
for _p in GAS_PRODUCERS:  _GAS_BASELINE[_p['key']] = _p['bcm']
for _c in CHOKEPOINTS:     _GAS_BASELINE[_c['key']] = _c['gas_bcm']
for _e in GAS_EDGES:
    if _e['key']:  _GAS_BASELINE[_e['key']] = _e['bcm']

_CHOKE_KEYS = {c['key'] for c in CHOKEPOINTS}
# Junction nodes are NOT split — they're flow-through nodes with no capacity limit
_JUNCTION_KEYS = {j['key'] for j in PIPELINE_JUNCTIONS}
# Consumer nodes (for shared gas demand mapping)
_CONSUMER_KEYS = {c['key'] for c in OIL_CONSUMERS}

# ── Timeline interpolation ─────────────────────────────────────────────────────
def _month_to_int(m):
    y, mo = m.split('-')
    return int(y)*12 + int(mo)


def _get_snapshot_overrides(month_key, commodity):
    override_field = f'{commodity}_overrides'
    months = sorted(TIMELINE_SNAPSHOTS.keys(), key=_month_to_int)
    if month_key in TIMELINE_SNAPSHOTS:
        return dict(TIMELINE_SNAPSHOTS[month_key].get(override_field, {}))
    target = _month_to_int(month_key)
    before, after = None, None
    for m in months:
        mi = _month_to_int(m)
        if mi <= target:   before = m
        elif after is None: after  = m
    if before is None: return dict(TIMELINE_SNAPSHOTS[months[0]].get(override_field, {}))
    if after  is None: return dict(TIMELINE_SNAPSHOTS[months[-1]].get(override_field, {}))
    bi = _month_to_int(before)
    ai = _month_to_int(after)
    t  = (target - bi) / (ai - bi) if ai != bi else 0.0
    b_ov = TIMELINE_SNAPSHOTS[before].get(override_field, {})
    a_ov = TIMELINE_SNAPSHOTS[after].get(override_field, {})
    baseline = _OIL_BASELINE if commodity == 'oil' else _GAS_BASELINE
    result = {}
    for k in set(b_ov) | set(a_ov):
        base_val = baseline.get(k, 0)
        result[k] = round(b_ov.get(k, base_val) + t * (a_ov.get(k, base_val) - b_ov.get(k, base_val)))
    return result

# ── Graph builders ─────────────────────────────────────────────────────────────
def _eff_cap(key, base, overrides, constrictions):
    cap = overrides.get(key, base)
    if key in constrictions:
        cap = cap * constrictions[key] / 100.0
    return max(0, cap)


def _build_oil_graph(oil_overrides, constrictions):
    G = nx.DiGraph()
    G.add_node('__src__')
    G.add_node('__snk__')
    # Chokepoints: split into in/out with capacity edge
    for c in CHOKEPOINTS:
        cap = _eff_cap(c['key'], c['normal_kbd'], oil_overrides, constrictions)
        G.add_edge(c['key']+'_in', c['key']+'_out', cap=cap)
    # Producers: __src__ → producer
    for p in OIL_PRODUCERS:
        cap = _eff_cap(p['key'], p['kbd'], oil_overrides, constrictions)
        G.add_edge('__src__', p['key'], cap=cap)
    # Consumers: consumer → __snk__
    for c in OIL_CONSUMERS:
        G.add_edge(c['key'], '__snk__', cap=c['kbd'])
    # Junction nodes: just exist, no special edges (capacity unlimited through junction)
    for j in PIPELINE_JUNCTIONS:
        G.add_node(j['key'])
    # Oil edges
    for e in OIL_EDGES:
        key  = e['key']
        base = e['kbd']
        cap  = _eff_cap(key, base, oil_overrides, constrictions) if key else base
        src = e['src'] + '_out' if e['src'] in _CHOKE_KEYS else e['src']
        dst = e['dst'] + '_in'  if e['dst'] in _CHOKE_KEYS else e['dst']
        if G.has_edge(src, dst):
            G[src][dst]['cap'] += cap
        else:
            G.add_edge(src, dst, cap=cap)
    return G


def _build_gas_graph(gas_overrides, constrictions):
    G = nx.DiGraph()
    G.add_node('__src__')
    G.add_node('__snk__')
    for j in PIPELINE_JUNCTIONS:
        G.add_node(j['key'])
    for c in CHOKEPOINTS:
        cap = _eff_cap(c['key'], c['gas_bcm'], gas_overrides, constrictions)
        G.add_edge(c['key']+'_in', c['key']+'_out', cap=cap)
    for p in GAS_PRODUCERS:
        cap = _eff_cap(p['key'], p['bcm'], gas_overrides, constrictions)
        G.add_edge('__src__', p['key'], cap=cap)
    for key, demand in GAS_CONSUMER_DEMAND.items():
        G.add_edge(key, '__snk__', cap=demand)
    for e in GAS_EDGES:
        key  = e['key']
        base = e['bcm']
        cap  = _eff_cap(key, base, gas_overrides, constrictions) if key else base
        src = e['src'] + '_out' if e['src'] in _CHOKE_KEYS else e['src']
        dst = e['dst'] + '_in'  if e['dst'] in _CHOKE_KEYS else e['dst']
        if G.has_edge(src, dst):
            G[src][dst]['cap'] += cap
        else:
            G.add_edge(src, dst, cap=cap)
    return G

# ── Min-cut extraction ─────────────────────────────────────────────────────────
def _find_min_cut_edges(G, flow_dict):
    reachable = set()
    queue = ['__src__']
    while queue:
        u = queue.pop()
        if u in reachable: continue
        reachable.add(u)
        for v in G.successors(u):
            if v not in reachable and G[u][v]['cap'] - flow_dict.get(u,{}).get(v,0) > 0.001:
                queue.append(v)
        for v in G.predecessors(u):
            if v not in reachable and flow_dict.get(v,{}).get(u,0) > 0.001:
                queue.append(v)
    result, seen = [], set()
    for u in reachable:
        for v in G.successors(u):
            if v not in reachable:
                du = u.replace('_out','').replace('_in','')
                dv = v.replace('_out','').replace('_in','')
                if du != dv and (du, dv) not in seen:
                    seen.add((du, dv))
                    result.append({'src': du, 'dst': dv, 'label': f'{du} → {dv}'})
    return result

# ── Flow serialisation ─────────────────────────────────────────────────────────
def _serialise_edge_flows(G, flow_dict):
    seen_pairs, edge_flows = {}, []
    for u, v, data in G.edges(data=True):
        du = u.replace('_out','').replace('_in','')
        dv = v.replace('_out','').replace('_in','')
        if du == dv or '__src__' in (du,dv) or '__snk__' in (du,dv): continue
        flow = flow_dict.get(u,{}).get(v, 0)
        cap  = data['cap']
        pair = (du, dv)
        if pair in seen_pairs:
            seen_pairs[pair]['flow'] += flow
        else:
            lat1,lng1 = _NODE_COORDS.get(du, (0,0))
            lat2,lng2 = _NODE_COORDS.get(dv, (0,0))
            entry = {'src':du,'dst':dv,'flow':round(flow,2),'capacity':round(cap,2),
                     'pct':0.0,'saturated':False,
                     'lat1':lat1,'lng1':lng1,'lat2':lat2,'lng2':lng2,'label':f'{du}→{dv}'}
            seen_pairs[pair] = entry
            edge_flows.append(entry)
    for ef in edge_flows:
        if ef['capacity'] > 0.001:
            ef['pct']       = round(ef['flow'] / ef['capacity'] * 100, 1)
            ef['saturated'] = ef['pct'] >= 99.0
    return edge_flows

# ── Public API ─────────────────────────────────────────────────────────────────
def compute_multi_flow(month_key, constrictions=None):
    if constrictions is None: constrictions = {}
    oil_ov = _get_snapshot_overrides(month_key, 'oil')
    gas_ov = _get_snapshot_overrides(month_key, 'gas')

    G_oil = _build_oil_graph(oil_ov, constrictions)
    oil_v, oil_fd = nx.maximum_flow(G_oil, '__src__', '__snk__', capacity='cap')
    oil_cut = _find_min_cut_edges(G_oil, oil_fd)
    oil_ef  = _serialise_edge_flows(G_oil, oil_fd)

    G_gas = _build_gas_graph(gas_ov, constrictions)
    gas_v, gas_fd = nx.maximum_flow(G_gas, '__src__', '__snk__', capacity='cap')
    gas_cut = _find_min_cut_edges(G_gas, gas_fd)
    gas_ef  = _serialise_edge_flows(G_gas, gas_fd)

    G_ob = _build_oil_graph({}, {})
    oil_base, _ = nx.maximum_flow(G_ob, '__src__', '__snk__', capacity='cap')
    G_gb = _build_gas_graph({}, {})
    gas_base, _ = nx.maximum_flow(G_gb, '__src__', '__snk__', capacity='cap')

    def deficit(f, b): return round((1-f/b)*100,1) if b > 0 else 0.0

    def cut_locs(cut_edges):
        nodes = {}
        for e in cut_edges:
            for k in (e['src'], e['dst']):
                if k not in nodes and k in _NODE_COORDS:
                    lat,lng = _NODE_COORDS[k]
                    nodes[k] = {'key':k,'lat':lat,'lng':lng,'label':_key_to_label(k)}
        return list(nodes.values())

    snap = TIMELINE_SNAPSHOTS.get(month_key, {})
    return {
        'month': month_key,
        'snapshot_label': snap.get('label', month_key),
        'snapshot_desc':  snap.get('description', ''),
        'oil': {
            'total_flow':  round(oil_v), 'baseline': round(oil_base),
            'deficit_pct': deficit(oil_v, oil_base), 'unit': 'kbd',
            'edge_flows':  oil_ef, 'min_cut_edges': oil_cut,
            'min_cut_nodes': cut_locs(oil_cut),
        },
        'gas': {
            'total_flow':  round(gas_v), 'baseline': round(gas_base),
            'deficit_pct': deficit(gas_v, gas_base), 'unit': 'bcm',
            'edge_flows':  gas_ef, 'min_cut_edges': gas_cut,
            'min_cut_nodes': cut_locs(gas_cut),
        },
    }

# ── Label helper ───────────────────────────────────────────────────────────────
_KEY_LABELS = {}
for _n in OIL_PRODUCERS+CHOKEPOINTS+OIL_CONSUMERS+GAS_PRODUCERS+LNG_IMPORTS+PIPELINE_JUNCTIONS:
    _KEY_LABELS[_n['key']] = _n['label']

def _key_to_label(k): return _KEY_LABELS.get(k, k)

# ── Serialisation helpers ──────────────────────────────────────────────────────
def get_all_nodes():
    nodes = []
    for p in OIL_PRODUCERS:
        nodes.append({**p, 'type':'oil_producer', 'commodity':'oil'})
    for c in CHOKEPOINTS:
        nodes.append({'key':c['key'],'label':c['label'],'lat':c['lat'],'lng':c['lng'],
                      'normal_kbd':c['normal_kbd'],'gas_bcm':c['gas_bcm'],
                      'type':'chokepoint','commodity':'both'})
    for c in OIL_CONSUMERS:
        nodes.append({**c, 'type':'oil_consumer','commodity':'oil'})
    for p in GAS_PRODUCERS:
        nodes.append({**p,'commodity':'gas'})
    for l in LNG_IMPORTS:
        nodes.append({**l,'commodity':'gas'})
    for j in PIPELINE_JUNCTIONS:
        nodes.append({'key':j['key'],'label':j['label'],'lat':j['lat'],'lng':j['lng'],
                      'type':'pipeline_junction','commodity':'oil'})
    return nodes


def get_all_edges(month_key='2021-01'):
    oil_ov = _get_snapshot_overrides(month_key, 'oil')
    gas_ov = _get_snapshot_overrides(month_key, 'gas')
    edges  = []
    for e in OIL_EDGES:
        cap  = oil_ov.get(e['key'], e['kbd']) if e['key'] else e['kbd']
        lat1,lng1 = _NODE_COORDS.get(e['src'], (0,0))
        lat2,lng2 = _NODE_COORDS.get(e['dst'], (0,0))
        wpts = MARITIME_WAYPOINTS.get(f"{e['src']}|{e['dst']}", [])
        latlngs = [[lat1,lng1]] + wpts + [[lat2,lng2]]
        edges.append({'src':e['src'],'dst':e['dst'],'capacity':cap,'unit':'kbd',
                      'type':e['type'],'label':e['label'],
                      'lat1':lat1,'lng1':lng1,'lat2':lat2,'lng2':lng2,
                      'latlngs':latlngs,'commodity':'oil','key':e['key']})
    for e in GAS_EDGES:
        cap  = gas_ov.get(e['key'], e['bcm']) if e['key'] else e['bcm']
        lat1,lng1 = _NODE_COORDS.get(e['src'], (0,0))
        lat2,lng2 = _NODE_COORDS.get(e['dst'], (0,0))
        wpts = MARITIME_WAYPOINTS.get(f"{e['src']}|{e['dst']}", [])
        latlngs = [[lat1,lng1]] + wpts + [[lat2,lng2]]
        edges.append({'src':e['src'],'dst':e['dst'],'capacity':cap,'unit':'bcm',
                      'type':e['type'],'label':e['label'],
                      'lat1':lat1,'lng1':lng1,'lat2':lat2,'lng2':lng2,
                      'latlngs':latlngs,'commodity':'gas','key':e['key']})
    return edges


def get_timeline():
    months, idx = [], 0
    y, m = 2021, 1
    shocks = {k: TIMELINE_SNAPSHOTS[k]['label'] for k in TIMELINE_SNAPSHOTS}
    while (y, m) <= (2026, 5):
        key = f'{y}-{m:02d}'
        months.append({'key':key,'index':idx,'shock':shocks.get(key),'year':y,'month':m})
        idx += 1; m += 1
        if m > 12: m = 1; y += 1
    return months


def get_chokepoints_ui():
    return [{'key':c['key'],'label':c['label'],
             'normal_kbd':c['normal_kbd'],'gas_bcm':c['gas_bcm']} for c in CHOKEPOINTS]
