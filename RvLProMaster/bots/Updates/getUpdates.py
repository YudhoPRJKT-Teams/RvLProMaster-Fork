from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from typing import Optional
from ...config import Auth
from ...utils import CreateLog
import json

api = Auth.Read.api_url

class getUpdates:
  raw_json = None
  serialize_json = None
  status_code = None
  
  @classmethod
  async def Initialize(cls, offset: Optional[int] = None):
    try:
      payload = {'timeout': 0}
      if offset is not None:
        payload['offset'] = offset
      async with ClientSession() as client:
        async with client.get(f"{api}/getUpdates", params=payload) as session:
          if session.status == 200:
            cls.raw_json = await session.json()
            cls.serialize_json = json.dumps(cls.raw_json, indent=2)
            cls.status_code = session.status
          else:
            CreateLog.Error("Unable to get response from methods getUpdates", str(cls.status_code))
          return cls
    except ClientConnectionError as e:
      CreateLog.Error(f"Unable to fetch from url {api}/getUpdates", str(e))
      return cls