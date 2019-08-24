import urllib
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import youtube_dl
import threading
import pafy
import time
import os
import sys
YOUTUBE_URL ="https://www.youtube.com/results?search_query="

class youtube_download:
    def __init__(self):
        self.stream = []
        self.youtube_url = []
        self.current_stream_idx = 0
        self.downloads = './downloads'
        self.current_youtube_url_idx = 0
        self.run = True
        if not os.path.exists(self.downloads):
            os.makedirs(self.downloads)

    def search_youtube_urls(self,text_to_search):
        query = urllib.parse.quote(text_to_search)
        #query = text_to_search
        url = YOUTUBE_URL + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        self.youtube_url = []
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            self.youtube_url.append('https://www.youtube.com' + vid['href'])
        
    def generate_urls_list(self, youtube_url, playlist = True):
        playlist = pafy.get_playlist(youtube_url)
        for i_video in range(len(playlist['items'])):
            v = playlist['items'][i_video]['pafy']
            print(i_video)
            try:
                self.stream.append(v)
            except:
                pass

    def download_song(self, request_key_words):
        self.run = True
        if "playlist" not in request_key_words:
            text_to_search = 'playlist '+ request_key_words
        self.search_youtube_urls(text_to_search)
        for vid_url in self.youtube_url:
            print(vid_url)
            self._download_song(request_key_words, vid_url)
    def _download_song(self, request_key_words, song_url):
        outtmpl = request_key_words + '%(id)s.%(ext)s'
        ydl_opts = {
          'format': 'bestaudio/best',
          'outtmpl': outtmpl,
          'postprocessors':[
			  {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 
				  'preferredquality': '192',
			  },
			  {'key': 'FFmpegMetadata'},
		  ],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(song_url, download=True)


    def return_information_of_current_song(self):
        v = self.stream[self.current_stream_idx]
        return {"title": v.title,
                "length": v.length,
                "viewcount": v.viewcount,
                "category": v.category,
                "dislikes": v.dislikes,
                "likes": v.likes,
                "rating": v.rating}
if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("please input the key words about which you want to download from youtube")
    else:
      yp = youtube_download()
      yp.download_song(sys.argv[1])
