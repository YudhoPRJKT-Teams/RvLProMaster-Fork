import json
from .create_log import CreateLog
from typing import Optional

class Inline:
  class Button:
    @classmethod
    def add(cls, text, callback_data=None, url=None):
      """This function creates a button for the inline keyboard.

      Args:
          text (str): The text that will be displayed on the button.
          callback_data (str): The data that will be sent to the bot when the button is clicked. Defaults to None.
          url (str): The URL that will be opened when the button is clicked. Defaults to None.
      """
      if callback_data and url:
        CreateLog.Error("A button can only have either callback_data or a URL, not both.")
      button = {'text': text}
      if callback_data:
        button['callback_data'] = callback_data
      elif url:
        button['url'] = url
      return button
  class Keyboard:
    @classmethod
    def Add(cls, text, callback_data=None, url=None):
      """This function creates an inline keyboard.

      Args:
          text (str): The text that will be displayed on the keyboard.
          callback_data (str): The data that will be sent to the bot when the keyboard is clicked. Defaults to None.
          url (str): The URL that will be opened when the keyboard is clicked. Defaults to None.
          resize_keyboard (bool): Whether to resize the keyboard. Defaults to True.
          one_time_keyboard (bool): Whether to show the keyboard only once. Defaults to True.
      """
      if callback_data and url:
        CreateLog.Error("A button can only have either callback_data or a URL, not both.")
      button = {'text': text}
      if callback_data:
        button['callback_data'] = callback_data
      elif url:
        button['url'] = url
      return button
    
  class CreateInline:
    @classmethod
    def button(cls, *rows):
      """This function creates an inline button."""
      keyboard = {'inline_keyboard': [list(row) for row in rows]}
      return json.dumps(keyboard)
    @classmethod
    def keyboard(cls, *rows, resize_keyboard: Optional[bool] = True, one_time_keyboard: Optional[bool] = True):
      """This function creates an inline keyboard."""
      keyboard = {'keyboard': [list(row) for row in rows], 'resize_keyboard': resize_keyboard, 'one_time_keyboard': one_time_keyboard}
      return json.dumps(keyboard)
