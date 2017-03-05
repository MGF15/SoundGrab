import requests, sys, re

# SoundGrab
# SoundCloud MP3 downloader
# Please use this script to download free tracks! 
# Coded by MGF15 - GitHub (http://github.com/MGF15)

tr   = 'https://api.soundcloud.com/i1/tracks/'
tr2 = '/streams?client_id='
id  = 'fDoItMDbsbZz8dY16ZzARCZmzgHBPotA' # be careful with this ;) please!
ver = '&app_version=14823339819'

def get(url):

	print '[+] Grabbing %s' % url

	site = requests.get(url).text

	track = re.findall(r':tracks:(.*?)"', site) # get track id

	print '[+] Got track id'

	name = re.findall(r'Stream(.*?)by(.*?)from', site) # get track name 

	trackid = track[0]

	apidown = tr + trackid + tr2 + id + ver

	getfile = requests.get(apidown).text

	findfile = re.findall(r'http_mp3_128_url":"(.*?)"',getfile) # our download link 

	refix = findfile[0].replace('\u0026', '&')

	fname = name[0][1] + '-' + name[0][0]

	return refix, fname

def downmp3(mp3file, name):
	
	file = open(name + '.mp3', 'wb')
	
	mp = requests.get(mp3file, stream=True)

	size = round(int(mp.headers['Content-Length'])/1024.0/1024.0,2)

	n = int(mp.headers['Content-Length'])

	print '[+] File size :' , size, 'Mb'

	print '[*] File name : '+ name +'.mp3'

	m = 0

	while m <= n:

		for i in mp.iter_content(1024):
		
			if i:
				m += 1024
				file.write(i)
				sys.stdout.write('\r')
    			sys.stdout.write("[*] Downloading [%-50s] %d%% " % ('*'*((m*100/n)/2), m*100/n))
    			sys.stdout.flush()
				
	print '\n[+] Download has been done!'

	return file
	
try:
	g = sys.argv[1]
	file = get(g)
	f = file[0]
	f2 = file[1]
	down = downmp3(f, f2)

except:
	print '\n[-] soundgrab.py <trackurl>\n[-] Or check your internet connection!'
