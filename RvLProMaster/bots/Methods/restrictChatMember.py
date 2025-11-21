from ...utils.create_log import CreateLog
from ...config.auth import Auth
from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from typing import Union, Optional
import json

api = Auth.Read.api_url

class restrictChatMember:
  @classmethod
  async def Initialize(cls,
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
    try:
      async with ClientSession() as client:
        permission = json.dumps(
          {
            'can_send_messages': canSendMessage,
            'can_send_audios': canSendAudios,
            'can_send_documents': canSendDocuments,
            'can_send_photos': canSendPhotos,
            'can_send_videos': canSendVideos,
            'can_send_video_notes': canSendVideoNotes,
            'can_send_voice_notes': canSendVoiceNotes,
            'can_send_other_messages': canSendOtherMessages,
            'can_add_web_page_previews': canAddWebPagePreviews,
            'can_change_info': canChangeInfo,
            'can_invite_users': canInviteUsers,
            'can_pin_messages': canPinMessages,
            'can_manage_topics':canManageTopics,
            'can_send_polls': canSendPolls
          }
        )
        payload = {
          'chat_id': chat_id,
          'user_id': user_id,
          'permissions': permission
        }
        if until_date is not None:
          payload['until_date'] = until_date
        async with client.post(f"{api}/restrictChatMember", data=payload) as session:
          cls.raw_json = await session.json()
          if session.status == 200:
            cls.serialize_json = json.dumps(cls.raw_json, indent=2)
            cls.status_code = session.status
          else:
            CreateLog.Error("Unable to get response from methods: restrictChatMember",str(cls.status_code))
            return cls
    except ClientConnectionError as e:
      CreateLog.Error("Unable to get response from methods: restrictChatMember",str(e))
