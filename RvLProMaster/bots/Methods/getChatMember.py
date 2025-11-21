from ...utils.create_log import CreateLog
from ...config.auth import Auth
from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from typing import Union
import json

api = Auth.Read.api_url

class getChatMember:
  @classmethod
  async def Initialize(cls, chat_id: Union[str, int],user_id: Union[str, int]):
    try:
      async with ClientSession() as client:
        payload = {'chat_id': chat_id, 'user_id': user_id}
        async with client.post(f"{api}/getChatMember", data=payload) as session:
          cls.raw_json = await session.json()
          if session.status == 200:
            cls.serialize_json = json.dumps(cls.raw_json, indent=2)
            cls.status_code = session.status
          else:
            CreateLog.Error("Unable to get response from methods getChatMember", str(cls.status_code))
          return cls
    except ClientConnectionError as e:
      CreateLog.Error(f"Unable to fetch from url {api}/getChatMember", str(e))
      return cls