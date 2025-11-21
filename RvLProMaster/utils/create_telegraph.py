from telegraph.aio import Telegraph
import asyncio

class telegraph:
  @classmethod
  async def create(cls, short_name: str, html_content: str,title: str):
    t = Telegraph()
    await t.create_account(short_name)
    response = await t.create_page(title, html_content)
    return response['url']