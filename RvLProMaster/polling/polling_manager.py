from ..config import Auth
from ..types import Message, ChatJoinRequest, NewChatParticipant, LeftChatParticipant
from ..utils import CreateLog
from aiohttp import ClientSession
from ..bots.Updates import getUpdates
from typing import Any
import asyncio
import json

api = Auth.Read.api_url

class Polling:
  # Clear all polling
  @classmethod
  async def ClearPolling(cls):
    """clearing all polling"""
    async with ClientSession() as session:
      async with session.get(f"{api}/getUpdates") as client:
        raw_data = await client.json()
        if raw_data["result"]:
          search_offset = max(update["update_id"] for update in raw_data["result"]) + 1
          payload = {'offset': search_offset}
          async with session.get(f"{api}/getUpdates", params=payload) as clients:
            await clients.read()
        else:
          pass
        
  # Long polling
  @classmethod
  async def LongPolling(cls):
      await cls.ClearPolling()

      offset = None
      while True:
        fr = await getUpdates.Initialize(offset)
        iu = fr.raw_json
        if iu and 'result' in iu:
          for ou in iu['result']:
            offset = ou['update_id'] + 1
            return ou
          await asyncio.sleep(1)
          
class Dispatch:
  msg = Message
  # dispatch command
  @classmethod
  async def Command(cls):
    from ..bots import pick_command
    if cls.msg.text:
      command = cls.msg.text.split()[0]
      if command in pick_command:
        await pick_command[command]()
  # Chat Join Request
  @classmethod
  async def ChatJoinRequest(cls):
    from ..bots import bot
    for handlers in bot.event.handlers_user_join:
      await handlers()
      
  # new chat member
  @classmethod
  async def NewChatMember(cls):
    from ..bots import bot
    for handlers in bot.event.handlers_joined_user:
      await handlers()
      
  # user left member
  @classmethod
  async def UserChatLeft(cls):
    from ..bots import bot
    for handlers in bot.event.handlers_user_left:
      await handlers()
      
  @classmethod
  async def Filter(cls):
    from ..bots import bot
    for handlers in bot.event.handlers_filter:
      await handlers(Message)
class Telegram:
  message = Message
  chat_join_request = ChatJoinRequest
  new_chat_participant = NewChatParticipant
  left_chat_participant = LeftChatParticipant
  @classmethod
  async def ExtractPolling(cls):
    while True:
      try:
        cls.out_updates = await Polling.LongPolling()
        # chat join request
        if 'chat_join_request' in cls.out_updates:
          req_key = cls.out_updates["chat_join_request"]
          
          # chat_join_request
          cls.chat_join_request.update_id =  req_key.get("update_id", "")
          cls.chat_join_request.date = req_key.get("date", "")
          cls.chat_join_request.user_chat_id = req_key.get("user_chat_id", "")
          # chat_join_request.chat
          cls.chat_join_request.chat.id = req_key["chat"].get("id", "")
          cls.chat_join_request.chat.title = req_key["chat"].get("title", "")
          cls.chat_join_request.chat.username = f"@{req_key['chat'].get('username', '')}"
          cls.chat_join_request.chat.type = req_key["chat"].get("type", "")
          # chat_join_request.from
          cls.chat_join_request.From.id = req_key["from"].get("id", "")
          cls.chat_join_request.From.is_bot = req_key["from"].get("is_bot", "")
          cls.chat_join_request.From.first_name = req_key["from"].get("first_name", "")
          cls.chat_join_request.From.last_name = req_key["from"].get("last_name", "")
          cls.chat_join_request.From.username = f"@{req_key['from'].get('username', '')}"
          cls.chat_join_request.From.language_code = req_key["from"].get("language_code", "")
          await Dispatch.ChatJoinRequest()
        # Message
        elif 'message' in cls.out_updates:
          msg_key = cls.out_updates["message"]
          
          # message
          cls.message.text = msg_key.get("text", "")
          cls.message.message_id = msg_key.get("message_id", "")
          cls.message.date = msg_key.get("date", "")
          
          # message.chat
          cls.message.chat.id = msg_key["chat"].get("id", "")
          cls.message.chat.title = msg_key["chat"].get("title", "")
          cls.message.chat.username = f"@{msg_key['chat'].get('username', '')}"

          # mmessage.chat.from
          cls.message.From.id = msg_key["from"].get("id", "")
          cls.message.From.first_name = msg_key["from"].get("first_name", "")
          cls.message.From.last_name = msg_key["from"].get("last_name", "")
          cls.message.From.username = f"@{msg_key['from'].get('username', '')}"
          
          if "reply_to_message" in msg_key:
            reply_key = msg_key["reply_to_message"]
            # message.reply_to_message
            cls.message.reply_to_message.message_id = reply_key.get("message_id", "")
            cls.message.reply_to_message.text = reply_key.get("text", "")
            
            # message.reply_to_message.From
            cls.message.reply_to_message.From.id = reply_key["from"].get("id", "")
            cls.message.reply_to_message.From.first_name = reply_key["from"].get("first_name", "")
            cls.message.reply_to_message.From.last_name = reply_key["from"].get("last_name", "")
            cls.message.reply_to_message.From.username = f"@{reply_key['from'].get('username', '')}"

            # message.reply_to_message.chat
            cls.message.reply_to_message.chat.id = reply_key["chat"].get("id", "")
            cls.message.reply_to_message.chat.title = reply_key["chat"].get("title", "")
            cls.message.reply_to_message.chat.username = f"@{reply_key['chat'].get('username', '')}"
            cls.message.reply_to_message.chat.type = reply_key["chat"].get("type", "")
            cls.message.reply_to_message.chat.type = reply_key["chat"].get("type", "")
            
            # message.reply_to_message.photo
            if "photo" in reply_key and len(reply_key["photo"]) > 0:
                if reply_key["photo"][0]:
                    cls.message.reply_to_message.photo.file_id = reply_key["photo"][0].get("file_id", "")
                if len(reply_key["photo"]) > 1 and reply_key["photo"][1]:
                    cls.message.reply_to_message.photo.file_id = reply_key["photo"][1].get("file_id", "")
          # New User 
          elif 'new_chat_participant' in msg_key:
            # new_chat_participant
            cls.new_chat_participant.id = cls.out_updates["message"]["new_chat_participant"].get("id", "")
            cls.new_chat_participant.is_bot = cls.out_updates["message"]["new_chat_participant"].get("is_bot", "")  
            cls.new_chat_participant.first_name = cls.out_updates["message"]["new_chat_participant"].get("first_name", "")
            cls.new_chat_participant.last_name = cls.out_updates["message"]["new_chat_participant"].get("last_name", "")
            cls.new_chat_participant.username = f"@{cls.out_updates['message']['new_chat_participant'].get('username', '')}"
            cls.new_chat_participant.language_code = cls.out_updates["message"]["new_chat_participant"].get("language_code", "")
            # new_chat_participant.message
            cls.new_chat_participant.message.message_id = cls.out_updates["message"].get("message_id", "")            
            # new_chat_participant.message.chat
            cls.new_chat_participant.message.chat.id = cls.out_updates["message"]["chat"].get("id", "")
            cls.new_chat_participant.message.chat.title = cls.out_updates["message"]["chat"].get("title", "")
            cls.new_chat_participant.message.chat.username = f"@{cls.out_updates['message']['chat'].get('username', '')}"
            cls.new_chat_participant.message.chat.type = cls.out_updates["message"]["chat"].get("type", "")
            await Dispatch.NewChatMember()
          # User left
          elif "left_chat_participant" in msg_key:  
            cls.left_chat_participant.id = cls.out_updates["message"]["left_chat_participant"].get("id", "")
            cls.left_chat_participant.is_bot = cls.out_updates["message"]["left_chat_participant"].get("is_bot", "")  
            cls.left_chat_participant.first_name = cls.out_updates["message"]["left_chat_participant"].get("first_name", "")
            cls.left_chat_participant.last_name = cls.out_updates["message"]["left_chat_participant"].get("last_name", "")
            cls.left_chat_participant.username = f"@{cls.out_updates['message']['left_chat_participant'].get('username', '')}"
            cls.left_chat_participant.language_code = cls.out_updates["message"]["left_chat_participant"].get("language_code", "")
            # left_chat_participant.message
            cls.left_chat_participant.message.message_id = cls.out_updates["message"].get("message_id", "")            
            # left_chat_participant.message.chat
            cls.left_chat_participant.message.chat.id = cls.out_updates["message"]["chat"].get("id", "")
            cls.left_chat_participant.message.chat.title = cls.out_updates["message"]["chat"].get("title", "")
            cls.left_chat_participant.message.chat.username = f"@{cls.out_updates['message']['chat'].get('username', '')}"
            cls.left_chat_participant.message.chat.type = cls.out_updates["message"]["chat"].get("type", "")
            await Dispatch.UserChatLeft()
          await Dispatch.Command()
          if (Message.text):
            await Dispatch.Filter()
          await asyncio.sleep(1)
          return cls
      except KeyError as e:
        CreateLog.Error("Got error!", str(e))