from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from typing import Optional, Union, Any
from ...config import Auth
from ...utils import CreateLog
from ...types.message import Message
import json
import re

api = Auth.Read.api_url

class sendMessage:
  @classmethod
  async def Initialize(cls, chat_id: Union[int, str], text: str, parse_mode: Any, disable_notification: bool = False, protect_content: bool = True, reply_markup: Optional[str ] = None, reply_chat: Optional[Union[int, str]] = None):
    try:
      payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'disable_notification': disable_notification,
        'protect_content': protect_content
      }
      if reply_markup is not None:
        payload['reply_markup'] = reply_markup
      if reply_chat is True:
        payload['reply_to_message_id'] = Message.message_id
      async with ClientSession() as client:
        async with client.post(f"{api}/sendMessage", data=payload) as session:
          cls.raw_json = await session.json()
          if session.status == 200:
            cls.serialize_json = json.dumps(cls.raw_json, indent=2)
            cls.status_code = session.status
            cls.message_id = cls.raw_json['result']['message_id']
          elif session.status == 400:
            # desc = cls.raw_json['description']
            des = cls.raw_json['description']
            pattern = r"is reserved and must be escaped with the preceding '\\'"
            desc = re.sub(pattern, "", des)
            desc = "Need Escaped text using '\\\'!" + desc.strip().replace("Bad Request: can't parse entities: Character '!'", "")
            CreateLog.Error("Please Escape Character", str(desc))
          else:
            CreateLog.Error("Unable to get response from methods sendMessage", str(cls.status_code))
          # Escaped
          return cls
        
    except ClientConnectionError as e:
      CreateLog.Error(f"Unable to fetch from url {api}/sendMessage", str(e))
      return cls