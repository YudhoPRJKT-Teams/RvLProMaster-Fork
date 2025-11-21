from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from typing import Union
from ...config import Auth
from ...utils import CreateLog
import json

api = Auth.Read.api_url

class deleteMessage:
  raw_json = "N/A"
  serialize_json = "N/A"
  status_code = "N/A"
  
  @classmethod
  async def Initialize(cls, chat_id: Union[str, int], message_id: str):
    try:
      if chat_id and message_id is not None:
        payload = {
          'chat_id': chat_id,
          'message_id': message_id
        }
        async with ClientSession() as client:
          async with client.post(f"{api}/deleteMessage", data=payload) as session:
            if session.status == 200:
              cls.serialize_json = json.dumps(cls.raw_json, indent=2)
              cls.status_code = session.status
            else:
              CreateLog.Error("Unable to get response from methods deleteMessage", str(cls.status_code))
            return cls
        
    except ClientConnectionError as e:
      CreateLog.Error(f"Unable to fetch from url {api}/getMe", str(e))
      return cls