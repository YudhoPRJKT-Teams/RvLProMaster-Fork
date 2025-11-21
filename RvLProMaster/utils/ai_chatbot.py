from google import genai
from openai import OpenAI

class Gemini:
  # Generate text content
  @classmethod
  def text(cls, prompt: str) -> str:
    from ..config.auth import Auth
    client = genai.Client(api_key=Auth.Read.genai_key)
    if prompt is not None:
      response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
      )
    return str(response.text)

class AzureOpenAI:
  @classmethod
  def text(cls, prompt: str) -> str:
    if prompt is not None:
      from ..config.auth import Auth
      client = OpenAI(base_url="https://models.github.ai/inference", api_key=Auth.Read.github_pat)
      response = client.chat.completions.create(
        messages=[
          {
            "role": "system",
            "content":"You are a helpful assistant.",
          },
          {
            "role": "user",
            "content": prompt
          }
        ],
        temperature=1.0,
        top_p=1.0,
        model="openai/gpt-4.1-mini"
      )
    return str(response.choices[0].message.content)
class AIChatBOT:
  gemini = Gemini
  gpt = AzureOpenAI