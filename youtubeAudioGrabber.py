import tornado.ioloop
import tornado.web
from pytube import YouTube
import threading
import string

import os
import subprocess

#pip install python-slugify
from slugify import slugify

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    form = """<form method="post">
    YouTube URL: <input type="text" name="yturl" value=""/><br>
    Download Path: <input type="text" name="path" value=""/><br>
    <input class="button" type="submit" value="Fetch"/>
    </form>"""
    self.write(form)

  def post(self):
    yturl = self.get_argument('yturl')
    dlpath = self.get_argument('path')
    print("yturl: " + yturl + " to " + dlpath )
    dlThread = DLHandler(yturl,dlpath)
    dlThread.start()
    self.write("Thanks. I will now download " + yturl + " to " + dlpath + ".")
    
class DLHandler(threading.Thread):
  def __init__(self,yturl,dlpath):
    threading.Thread.__init__(self)
    self.yturl = yturl 
    self.dlpath = dlpath 

  def run(self):
    yt = YouTube(self.yturl)
    stream = yt.streams.filter(only_audio=True,file_extension='mp4').first()
    f = os.path.join(self.dlpath,slugify(yt.title) + '.mp3')
    stream.download(self.dlpath)
    default_filename = os.path.join(self.dlpath,stream.default_filename)
    
    subprocess.call(['ffmpeg','-i',default_filename,f])
    os.remove(default_filename)
    print("Done.")


def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
  ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


