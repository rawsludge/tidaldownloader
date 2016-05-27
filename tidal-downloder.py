#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tidalapi
import argparse
import urllib2
import os
from mutagen.flac import FLAC

config = tidalapi.Config(quality=tidalapi.Quality.lossless)
session = tidalapi.Session(config=config)
session.login("rawsludge@hotmail.com", "ozturk.99")

def downloadFile(url, path, fileName):
	u = urllib2.urlopen(url)
	meta = u.info()
	contentLength = meta.getheaders("Content-Length")
	print len(contentLength)
	if len(contentLength):
		fileSize = int(contentLength[0])
	else:	
		fileSize = 1
	print "Downloading: %s Bytes: %s" % (fileName.encode("utf8"), fileSize)
	if not os.path.exists(path.encode("utf8")):
    		os.makedirs(path.encode("utf8"))
	fileName = path + fileName
	if os.path.isfile(fileName.encode("utf8")):
		return 
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


parser = argparse.ArgumentParser()
parser.add_argument("--albums", help="get user album lists", action="store_true")
parser.add_argument("--download", help="download album lists", action="store_true")
parser.add_argument("--album", help="album id would be downloaded", nargs='?')

args = parser.parse_args()
if args.albums:
	albums = session.user.favorites.albums()
	for album in albums:
		print `album.id` + ' --> ' + album.artist.name.encode("utf8") + " - " + album.name.encode('utf8')
if args.download:
	album = session.get_album(args.album)
	artist = session.get_artist(album.artist.id)	
	tracks = session.get_album_tracks(album_id=args.album)
	albumPath = "./" + artist.name + " - " + album.name + "/"
	downloadFile( album.image, albumPath, "Folder.jpg")
	for track in tracks:
		url = session.get_media_url(track.id)
		fileName = artist.name + ' - ' + track.name + '.flac'
		#print album.image
		downloadFile(url, albumPath, fileName)
		fileName = albumPath + fileName
		audiofile = FLAC(fileName.encode("utf8"))
		audiofile["artist"] = track.artist.name
		audiofile["album"] = album.name
		audiofile["albumartist"] = artist.name
		audiofile["title"] = track.name
		audiofile["tracknumber"] = str(track.track_num)
		#print audiofile.pprint().encode("utf8")
		audiofile.save()
    		#print fileName.encode("utf8")
		#print track.name.encode("utf8")
