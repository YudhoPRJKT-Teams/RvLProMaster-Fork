from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from ...config import Auth
from ...utils import CreateLog
from ..datas import BotsData
from typing import Optional, Any
import json

api = Auth.Read.api_url

async def getMe():
  async with ClientSession() as session:
    async with session.get(f"{api}/getMe") as client:
      raw_output = await client.json()
      return BotsData(
        raw_json = raw_output,
        status_code = client.status,
        serialize_json = json.dumps(raw_output, indent=2)
      )