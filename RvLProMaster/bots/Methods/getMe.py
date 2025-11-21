from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from ...config import Auth
from ...utils import CreateLog
import json

api = Auth.Read.api_url

class getMe:
  @classmethod
  async def Initialize(cls):
    try:
      async with ClientSession() as client:
        async with client.get(f"{api}/getMe") as session:
          cls.raw_json = await session.json()
          if session.status == 200:
            cls.serialize_json = json.dumps(cls.raw_json, indent=2)
            cls.status_code = session.status
          else:
            CreateLog.Error("Unable to get response from methods getMe", str(cls.status_code))
          return cls
        
    except ClientConnectionError as e:
      CreateLog.Error(f"Unable to fetch from url {api}/getMe", str(e))
      return cls