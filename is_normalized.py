# -*- coding: utf-8 -*-
import unicodedata

def is_normalized(text):
    normalized = ''.join(c for c in unicodedata.normalize('NFD', u''.join(text))
                  if unicodedata.category(c) != 'Mn')
    if normalized == text:
        print 'nie'
        return False
    else:
        print 'tak'
        return True

if __name__ == "__main__":
    is_normalized('ŻABA')