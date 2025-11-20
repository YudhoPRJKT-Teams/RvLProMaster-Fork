# Parse Mode: Markdown
def _Markdown():
  return "Markdown"

# Parse Mode: MarkdownV2
def _MarkdownV2():
  return "MarkdownV2"

# Parse Mode: HTML
def _HTML():
  return "HTML"


class ParseMode:
  Markdown = _Markdown()
  MarkdownV2 = _MarkdownV2()
  HTML = _HTML()
  
  