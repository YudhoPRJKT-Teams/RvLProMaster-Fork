from .Methods import (
  getMe,
  sendMessage,
  deleteMessage,
  restrictChatMember,
  editMessageText,
  getChatAdministrators,
  getChatMemberCount
)
from .Updates import (
  getUpdates
)
from typing import Callable, Dict, Awaitable, Any, Optional, Union
from functools import wraps
from ..utils import CreateLog, ParseMode
from ..polling import Telegram
from ..types.message import MESSAGE
import asyncio
import re

message = MESSAGE()
pick_command: Dict[str, Callable[[], Awaitable[Any]]] = {}
LEET_MAP = {
    "a": "[aA4@Λ^•àáâãäåΑα]",
    "b": "[bB8ßβ]",
    "c": "[cCĊċÇç¢©]",
    "d": "[dDÐđ]",
    "e": "[eE3€èéêëΣΕεɛɘ]",
    "f": "[fFƒ]",
    "g": "[gG69ɢɡ]",
    "h": "[hHнНḧḣħ]",
    "i": "[iI1!|íìîïΙι]",
    "j": "[jJĵј]",
    "k": "[kKΚκ]",
    "l": "[lL1|!ΙІ]",
    "m": "[mMΜмМ]",
    "n": "[nNηиΗΝ]",
    "o": "[oO0°ºοΟΘθöóòôõ]",
    "p": "[pPρРр]",
    "q": "[qQ9]",
    "r": "[rRЯřŕ]",
    "s": "[sS5$§šŚśzZ2]",  # sengaja campur Z dikit (spam sering swap)
    "t": "[tT7+τтТ]",
    "u": "[uUùúûüµυ]",
    "v": "[vVν∨]",
    "w": "[wWωψvv]",
    "x": "[xXχΧ×✖]",
    "y": "[yY¥γү]",
    "z": "[zZ2žźż]"
}

def to_leet_regex(word: str):
    out = ""
    for ch in word:
        c = ch.lower()
        if c in LEET_MAP:
            out += LEET_MAP[c]
        else:
            out += f"[{ch.lower()}{ch.upper()}]"
    return out
# class methods
class methods:
  # Methods: getMe
  @classmethod
  async def getMe(cls):
    """A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a [User](https://core.telegram.org/bots/api#user) object."""
    return await getMe.Initialize()
  # Methods: sendMessage
  @classmethod
  async def sendMessage(cls, chat_id: Union[int, str], text: str, parse_mode: Any, disable_notification: bool = False, protect_content: bool = True, reply_markup: Optional[str] = None, reply_chat: Optional[Union[int,str]] = None):
    """Use this method to send text messages. On success, the sent [Message](https://core.telegram.org/bots/api#message) is returned.

    Args:
        chat_id (Union[int, str]):  Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        text (str): Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        parse_mode (Any): Mode for parsing entities in the message text. See formatting options for more details.
        disable_notification (bool, optional): Sends the message [silently](https://telegram.org/blog/channels-2-0#silent-messages). Users will receive a notification with no sound.. Defaults to False.
        protect_content (bool, optional): Protects the contents of the sent message from forwarding and saving. Defaults to True.
        reply_markup (Optional[dict], optional): Additional interface options. A JSON-serialized object for an [inline keyboard](https://core.telegram.org/bots/features#inline-keyboards), [custom reply keyboard](https://core.telegram.org/bots/features#keyboards), instructions to remove a reply keyboard or to force a reply from the user. Defaults to None.
        reply_chat (Optional[int,str], optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    return await sendMessage.Initialize(chat_id, text, parse_mode, disable_notification, protect_content, reply_markup, reply_chat)
  
  # Methods: deleteMessage
  @classmethod
  async def deleteMessage(cls, chat_id: Union[str, int], message_id: str):
    """Use this method to delete a message, including service messages, with the following limitations:
      - A message can only be deleted if it was sent less than 48 hours ago.
      - Service messages about a supergroup, channel, or forum topic creation can't be deleted.
      - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
      - Bots can delete outgoing messages in private chats, groups, and supergroups.
      - Bots can delete incoming messages in private chats.
      - Bots granted can_post_messages permissions can delete outgoing messages in channels.
      - If the bot is an administrator of a group, it can delete any message there.
      - If the bot has can_delete_messages administrator right in a supergroup or a channel, it can delete any message there.
      - If the bot has can_manage_direct_messages administrator right in a channel, it can delete any message in the corresponding direct messages chat.
      Returns True on success.

    Args:
        chat_id (Union[str, int]): Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        message_id (int): Identifier of the message to delete
    """
    return await deleteMessage.Initialize(chat_id, message_id)
  
  # Methods: restrictChatMembers
  @classmethod
  async def restrictChatMember(cls,
    chat_id: Union[str,int],
    user_id: Union[str, int],
    canSendMessage: Optional[bool] = True,
    canSendAudios: Optional[bool] = True,
    canSendDocuments: Optional[bool] = True,
    canSendPhotos: Optional[bool] = True,
    canSendVideos: Optional[bool] = True,
    canSendVideoNotes: Optional[bool] = True,
    canSendVoiceNotes: Optional[bool] = True,
    canSendPolls: Optional[bool] = False,
    canSendOtherMessages: Optional[bool] = True,
    canAddWebPagePreviews: Optional[bool] = True,
    canChangeInfo: Optional[bool] = False,
    canInviteUsers: Optional[bool] = False,
    canPinMessages: Optional[bool] = False,
    canManageTopics: Optional[bool] = False,
    until_date: Optional[str] = None
  ):
    """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success.

    Args:
        chat_id (Union[str,int]): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        user_id (Union[str, int]): Unique identifier of the target user
        canSendMessage (Optional[bool], optional): Optional. True, if the user is allowed to send text messages, contacts, giveaways, giveaway winners, invoices, locations and venues. Defaults to True.
        canSendAudios (Optional[bool], optional): Optional. True, if the user is allowed to send audios. Defaults to True.
        canSendDocuments (Optional[bool], optional): Optional. True, if the user is allowed to send documents. Defaults to True.
        canSendPhotos (Optional[bool], optional): Optional. True, if the user is allowed to send photos. Defaults to True.
        canSendVideos (Optional[bool], optional): Optional. True, if the user is allowed to send videos. Defaults to True.
        canSendVideoNotes (Optional[bool], optional): Optional. True, if the user is allowed to send video notes. Defaults to True.
        canSendVoiceNotes (Optional[bool], optional): Optional. True, if the user is allowed to send voice notes. Defaults to True.
        canSendPolls (Optional[bool], optional): Optional. True, if the user is allowed to send polls and checklists. Defaults to False.
        canSendOtherMessages (Optional[bool], optional): Optional. True, if the user is allowed to send animations, games, stickers and use inline bots. Defaults to True.
        canAddWebPagePreviews (Optional[bool], optional): Optional. True, if the user is allowed to add web page previews to their messages. Defaults to True.
        canChangeInfo (Optional[bool], optional): Optional. True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups. Defaults to False.
        canInviteUsers (Optional[bool], optional): Optional. True, if the user is allowed to invite new users to the chat. Defaults to False.
        canPinMessages (Optional[bool], optional): Optional. True, if the user is allowed to pin messages. Ignored in public supergroups. Defaults to False.
        canManageTopics (Optional[bool], optional): Optional. True, if the user is allowed to create forum topics. If omitted defaults to the value of can_pin_messages. Defaults to False.
        until_date (Optional[str], optional): Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever. Defaults to None.

    Returns:
        _type_: _description_
    """
    return await restrictChatMember.Initialize(chat_id, user_id, canSendMessage, canSendAudios, canSendDocuments, canSendPhotos, canSendVideos, canSendVideoNotes, canSendVoiceNotes, canSendPolls, canSendOtherMessages, canAddWebPagePreviews, canChangeInfo, canInviteUsers, canPinMessages, canManageTopics, until_date)
  
  # Methods: editMessageText
  @classmethod
  async def editMessageText(cls, chat_id: Union[str, int], text: Any, message_id: Union[str, int], parse_mode: str):
    """Use this method to edit text and [game](https://core.telegram.org/bots/api#games) messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api#message) is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

    Args:
        chat_id (Union[str, int]): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        text (Any): New text of the message, 1-4096 characters after entities parsing
        message_id (Union[str, int]): Required if inline_message_id is not specified. Identifier of the message to edit
        parse_mode (ParseMode): Mode for parsing entities in the message text
    """
    return await editMessageText.Initialize(chat_id, text, message_id, parse_mode)
  
  # Methods: getChatAdministrators
  @classmethod
  async def getChatAdministrators(cls, chat_id: Union[str, int]):
    """Use this method to get a list of administrators in a chat, which aren't bots. Returns an Array of [ChatMember](https://core.telegram.org/bots/api#chatmember) objects.

    Args:
        chat_id (Union[str, int]): https://core.telegram.org/bots/api#chatmember
    """
    return await getChatAdministrators.Initialize(chat_id)
  
  # Methods: getChatMemberCount
  @classmethod
  async def getChatMemberCount(cls, chat_id: Union[str, int]):
    """Use this method to get the number of members in a chat. Returns Int on success.

    Args:
        chat_id (Union[str, int]): Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
    """
    return await getChatMemberCount.Initialize(chat_id)
# class updates
class updates:
  @classmethod
  async def getUpdates(cls, offset: Optional[int] = None):
    """Use this method to receive incoming updates using long polling ([wiki](https://en.wikipedia.org/wiki/Push_technology#Long_polling)). Returns an Array of [Update](https://core.telegram.org/bots/api#update) objects.

    Args:
        offset (Optional[int], optional): Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will be forgotten. Defaults to None.
    """
    return await getUpdates.Initialize(offset)

# class Event
class Event:
  handlers_user_join = []
  handlers_joined_user = []
  handlers_user_left = []
  handlers_filter = []
  
  # User Request Join
  @classmethod
  def UserRequest(cls):
    def decorator(func):
      cls.handlers_user_join.append(func)
      return func
    return decorator
  
  # New User Joined
  @classmethod
  def NewUser(cls):
    def decorator(func):
      cls.handlers_joined_user.append(func)
      return func
    return decorator
  
  # User Left
  @classmethod
  def UserLeft(cls):
    def decorator(func):
      cls.handlers_user_left.append(func)
      return func
    return decorator

class bot:
  Methods = methods()
  Updates = updates()
  event = Event()

  @classmethod
  async def run(cls):
    """Run Bot Polling"""
    CreateLog.Info("Bot Is Running!")
    while True:
      await Telegram.ExtractPolling()
      await asyncio.sleep(1)
  
  @classmethod
  def command(cls, command: str) -> Callable[[Callable[[], Awaitable[Any]]], Callable[[], Awaitable[Any]]]:
    """Use this decorator to register a command in the bot.

    Args:
        command (str): Your command name. Example: /start, /help, etc.
    """
    def decorator(func: Callable[[], Awaitable[Any]]) -> Callable[[], Awaitable[Any]]:
        @wraps(func)
        async def wrapper() -> Any:
            return await func()
        pick_command[command] = wrapper
        return wrapper
    return decorator
  
  @classmethod
  def filter(cls, filter_file: str):
    def decorator(func):
      @wraps(func)
      async def wrapper(msg: MESSAGE):
        with open(filter_file, 'r') as r:
            raw_filter_list = r.read().splitlines()
        regex_list = [to_leet_regex(w) for w in raw_filter_list]
        text = msg.text or ""
        match_found = False
        for pattern in regex_list:
            if re.search(pattern, text, re.IGNORECASE):
                match_found = True
                break
        return await func(match_found)
      cls.event.handlers_filter.append(wrapper)
      return wrapper
    return decorator
