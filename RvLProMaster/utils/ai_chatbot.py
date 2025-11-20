from google import genai


class AIChatBOT:
  @classmethod
  def Gemini(cls, prompt: str):
    from ..config.auth import Auth
    client = genai.Client(api_key=Auth.Read.genai_key)
    if prompt is not None:
      response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
      )
    return response.text