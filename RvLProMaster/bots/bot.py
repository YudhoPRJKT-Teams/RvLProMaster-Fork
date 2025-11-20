from .Methods import (
  getMe,
  sendMessage
)
from .Updates import (
  getUpdates
)
from typing import Callable, Dict, Awaitable, Any, Optional, Union
from functools import wraps
from ..utils import CreateLog
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
  async def sendMessage(cls, chat_id: Union[int, str], text: str, parse_mode: Any, disable_notification: bool = False, protect_content: bool = True, reply_markup: Optional[dict] = None, reply_chat: Optional[Union[int,str]] = None):
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
