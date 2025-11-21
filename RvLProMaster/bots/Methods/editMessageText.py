from ...utils.create_log import CreateLog
from ...config.auth import Auth
from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from typing import Union, Any
import json

api = Auth.Read.api_url

class editMessageText:
  @classmethod
  async def Initialize(cls, chat_id: Union[str, int], text: Any, message_id: Union[str, int], parse_mode: str):
    try:
      async with ClientSession() as client:
        payload = {
          'chat_id': chat_id,
          'text': text,
          'message_id': message_id,
          'parse_mode': parse_mode
        }
        async with client.post(f"{api}/editMessageText", data=payload) as session:
          cls.raw_json = await session.json()
          if session.status == 200:
            cls.serialize_json = json.dumps(cls.raw_json, indent=2)
            cls.status_code = session.status
            cls.message_id = cls.raw_json['result']['message_id']
          else:
            CreateLog.Error("Unable to get response from methods editMessageText", str(cls.status_code))
          return cls
    except ClientConnectionError as e:
      CreateLog.Error(f"Unable to fetch from url {api}/editMessageText", str(e))
      return cls