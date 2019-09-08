from neko import Nekopoi

poi = Nekopoi(headers={"User-Agent": 'Nekopoi/1.69'})
#Initialize Nekopoi instance

#search hentai
hentai = poi.hentai(page=1)
print(hentai)

#search jav
jav = poi.jav(page=3)
print(jav[0])

#search 3D
_3d = poi._3d(page=2)
print(_3d[0].extras)

#search cosplay
cosplay = poi.cosplay()
for cos in cosplay:
	print(cos)

#sure you can get detail manualy from url
detail = poi.detail("https://3z094n2681j06q8k14w31cu4q80d5p.com/hime-sama-love-life-episode-2-subtitle-indonesia/")
print(detail)

#get stream_url
#Note: if embeded url hosted from streamcherry this will returning error
#for now streamcherry not supported yet
stream = poi.get_stream(detail.extras.streams[0])
print(stream)

#download video
download = poi.download(stream_url=stream, path="neko.mp4")
print(download)
print(download._url)
download.download()