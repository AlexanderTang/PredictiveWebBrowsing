from urlparse import urlparse

s= ' https://www.google.com/search?q=ben+stiller&ie=utf-8&oe=utf-8#q=adam+sandler'

o = urlparse(s)

print o.path

print o