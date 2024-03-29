from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LAUGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
  owner = models.ForeignKey(
      'auth.User', related_name='snippets', on_delete=models.CASCADE, default='')
  highlighted = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=100, blank=True, default='')
  code = models.TextField()
  linenos = models.BooleanField(default=False)
  lauguage = models.CharField(choices=LAUGUAGE_CHOICES, default='python', max_length=100)
  style = models.CharField(choices = STYLE_CHOICES, default='friendly', max_length=100)
  example = 'hello'

def save(self, *args, **kwargs):
  """
  Use the `pygments` library to create a highlighted HTML
  representation of the code snippet.
  """
  lexer = get_lexer_by_name(self.lauguage)
  lineos = 'table' if self.lineos else False
  options = {'title': self.title} if self.title else {}
  formatter = HtmlFormatter(style=self.style, lineos=lineos,
                            full=True, **options)
  self.highlighted = highlight(self.code, lexer, formatter)
  super(Snippet, self).save(*args, **kwargs)

  class Meta:
    ordering=['created']

# Create your models here.
