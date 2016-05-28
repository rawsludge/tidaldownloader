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
	if len(contentLength):
		fileSize = int(contentLength[0])
	else:	
		fileSize = 1
	print "Downloading: %s Bytes: %s" % (fileName.encode("utf8"), fileSize)
	if not os.path.exists(path.encode("utf8")):
    		os.makedirs(path.encode("utf8"))
	fileName = os.path.join( path, fileName)
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
parser.add_argument("--path", help="download path", nargs='?')

args = parser.parse_args()
if args.albums:
	albums = session.user.favorites.albums()
	print "Album ID    Artist Name                    Album Name"
	print "-------------------------------------------------------------------------"
	for album in albums:
		output = u"{:<11} {:30} {}".format(album.id, album.artist.name, album.name)
		print output.encode('utf8')
if args.download:
	album = session.get_album(args.album)
	artist = session.get_artist(album.artist.id)	
	tracks = session.get_album_tracks(album_id=args.album)
	albumPath = args.path
	albumPath = os.path.join(albumPath, u"{} - {}".format(artist.name, album.name))
	downloadFile( album.image, albumPath, "Folder.jpg")
	for track in tracks:
		url = session.get_media_url(track.id)
		fileName = u"{} - {}.flac".format(artist.name, track.name)
		downloadFile(url, albumPath, fileName)
		fileName = os.path.join(albumPath, fileName)
		audiofile = FLAC(fileName.encode("utf8"))
		audiofile["artist"] = track.artist.name
		audiofile["album"] = album.name
		audiofile["albumartist"] = artist.name
		audiofile["title"] = track.name
		audiofile["tracknumber"] = str(track.track_num)
		audiofile.save()
