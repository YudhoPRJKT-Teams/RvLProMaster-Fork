import json
import os
import asyncio
import getpass
import httpx
from RvLProMaster.utils import CreateLog


class Account:
  @classmethod
  def _Create(cls):
    try:
      if os.path.exists(f"{os.getcwd()}/config.json"):
        CreateLog.Info("Configuration file already maked, skipping make configuration file")
      else:
        print("=======================|RvLProMaster Authentication Utils|=======================")
        token = str(getpass.getpass("Input your telegram bot token: ",))
        api_url = str(input("You have custom api telegram bot? (y/n): "))
        api_selector = None
        if token is not None:
          if api_url == "y":
            api_selector = str(input("Insert your custom api: "))
          else:
            api_selector = f"https://api.telegram.org/bot{token}"
          with open(f"{os.getcwd()}/config.json", "w") as f:
            payload = {'api_url': f"{api_selector}/bot{token}"}
            struct_json = json.dumps(payload, indent=2)
            f.write(struct_json)
            
            # Testing
            CreateLog.Info("Testing connection")
            base_api = json.loads(struct_json)
            cls.api = base_api['api_url']
            code = httpx.get(f"{cls.api}/getMe")
            if code == 200:
              CreateLog.Info("Connection Successfully!")
            else:
              CreateLog.Error("Connection uncessfully!, please check your token and api url")
    except httpx.ConnectError:
      CreateLog.Error(f"Unable to resolve {cls.api}")
      
  @classmethod
  def _Read(cls):
    """Read Authentication Class"""
    with open(f"{os.getcwd()}/config.json", "r") as r:
      output_json = json.loads(r.read())
      cls.api_url = output_json['api_url']
      cls.genai_key = output_json['genai_key']
      cls.github_pat = output_json['github_pat']
      return cls

class Auth:
  Create = Account._Create()
  Read = Account._Read()

