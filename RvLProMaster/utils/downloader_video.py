from yt_dlp import YoutubeDL
from .create_log import CreateLog

class Download:
  @classmethod
  async def Video(cls, links: str):
    if links is not None:
      conf = {
        'outtmpl': 'video.mp4',
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'logtostderr': False
      }
      with YoutubeDL(conf) as dl: # type: ignore
        dl.download([links])
    else:
      CreateLog.Error('Please insert links')