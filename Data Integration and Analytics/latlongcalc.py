from math import sin, cos, sqrt, atan2, radians

def getc(n1, w1, n2, w2):
  dlat = n2 - n1
  dlon = w2 - w1
  lat1 = radians(n1)
  lon1 = radians(w1)
  lat2 = radians(n2)
  lon2 = radians(w2)
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  return 2 * atan2(sqrt(a), sqrt(1 - a))

def miles(n1, w1, n2, w2):
  im = 3959
  return im * getc(n1, w1, n2, w2)

def meters(n1, w1, n2, w2):
  m = 6.371 * 1000000
  return m * getc(n1, w1, n2, w2)

def km(n1, w1, n2, w2):
  km = 6371
  return km * getc(n1, w1, n2, w2)

def nm(c1,c2):
  nm = 3440
  return km * getc(c1,c2)