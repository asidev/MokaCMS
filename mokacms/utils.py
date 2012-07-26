#!/usr/bin/env python

from bs4 import BeautifulSoup
__all__ = ['classproperty', 'clean_html']


class classproperty(property):
    """ a property decorator for classmethods """
    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)()

    def __set__(self, obj, value):
        cls = type(obj)
        return self.fset.__get__(None, cls)(value)


def pshell_setup(env):
  env['mongodb_connection'] = env['registry'].mongodb_connection
  env['mdb'] = env['mongodb_connection'][env['registry'].mongodb_database]
  import mokacms.model
  env['m'] = mokacms.model


# Temporary solution until bleach/html5lib are ported to python3
#http://stackoverflow.com/questions/699468/python-html-sanitizer-scrubber-filter
acceptable_elements = ('a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
      'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
      'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
      'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
      'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
      'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
      'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
      'thead', 'tr', 'tt', 'u', 'ul', 'var')


acceptable_attributes = ('abbr', 'accept', 'accept-charset', 'accesskey',
  'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
  'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
  'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
  'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
  'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
  'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 
  'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
  'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
  'usemap', 'valign', 'value', 'vspace', 'width')


def clean_html(fragment):
    while True:
        soup = BeautifulSoup(fragment)
        removed = False
        for tag in soup.findAll(True):
            if tag.name not in acceptable_elements:
                tag.extract()
                removed = True

            #else:
                #for attr in tag._getAttrMap().keys():
                #    if attr not in acceptable_attributes:
                #        del tag[attr]

        fragment = str(soup)
        if removed:
            # we removed tags and tricky can could exploit that!
            # we need to reparse the html until it stops changing
            continue

        return fragment
