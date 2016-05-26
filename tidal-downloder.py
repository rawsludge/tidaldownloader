import tidalapi
import argparse
import urllib2


config = tidalapi.Config(quality=tidalapi.Quality.lossless)
session = tidalapi.Session(config=config)
session.login("rawsludge@hotmail.com", "xxxxxxxxx")


parser = argparse.ArgumentParser()
parser.add_argument("--albums", help="get user album lists", action="store_true")
parser.add_argument("--download", help="download album lists", action="store_true")
parser.add_argument("--album", help="album id would be downloaded", nargs='?')

args = parser.parse_args()
if args.albums:
	albums = session.user.favorites.albums()
	for album in albums:
		print `album.id` + ' --> ' + album.name.encode('utf8')
if args.download:
	album = session.get_album(args.album)
	artist = session.get_artist(album.artist.id)	
	tracks = session.get_album_tracks(album_id=args.album)
	for track in tracks:
		url = session.get_media_url(track.id)
		fileName = artist.name + ' - ' + track.name + '.flac'
    		#print fileName.encode("utf8")
		u = urllib2.urlopen(url)
		meta = u.info()
		fileSize = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (fileName.encode("utf8"), fileSize)
		f = open(fileName.encode("utf8"), 'wb')
		fileDownloaded = 0
		blockSize = 8192
		while True:
			buffer = u.read(blockSize)
			if not buffer:
				break
			fileDownloaded += len(buffer)
			f.write(buffer)
			status = r"%10d [%3.2f%%]" % (fileDownloaded, fileDownloaded * 100. / fileSize)
			status = status + chr(8) * (len(status)+1)
			print status,
		f.close()
		#print track.name.encode("utf8")
