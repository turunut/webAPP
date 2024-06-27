import numpy as np
import sys

def CTFactory(flag):
  flag = flag.lower() # lo pasamos a minusculas
  if flag == "isotrop":
    return Isotrop()
  if flag == "traniso":
    return TranIso()
  if flag == "orthotrop":
    return Orthotrop()
  sys.exit("Non defined CT")

class CT:
  def __init__(self):
    pass
      
  def getEdir(self, vec=None):
    return np.dot(vec,self.getEvec)

class Isotrop(CT):
  def __init__(self):
    super(Isotrop, self).__init__()

  def read(self, lines, line):    
    while line[0] != "end":        
      if line[0] == "e":
        self.E = float( line[2] )
      if line[0] == "v":
        self.v = float( line[2] )
      lines, line = nextLine(lines)

  def check(self):
    flag = True
    if self.E <= 0:
      flag = False
    return flag

  def compute3D(self, C):
    Sarray = np.zeros((6,6))
    Sarray[0,0] = 1/self.E
    Sarray[1,1] = 1/self.E
    Sarray[2,2] = 1/self.E
    Sarray[0,1] = -self.v/self.E
    Sarray[0,2] = -self.v/self.E
    Sarray[1,0] = -self.v/self.E
    Sarray[1,2] = -self.v/self.E
    Sarray[2,0] = -self.v/self.E
    Sarray[2,1] = -self.v/self.E
    Sarray[3,3] = (2+2*self.v)/self.E
    Sarray[4,4] = (2+2*self.v)/self.E
    Sarray[5,5] = (2+2*self.v)/self.E
    C[:,:] = np.round( np.linalg.inv(Sarray), 2 )
    return C

  def computePS(self, C):
    Sarray = np.zeros((3,3))
    Sarray[0,0] = 1/self.E
    Sarray[1,1] = 1/self.E
    Sarray[1,0] = -self.v/self.E
    Sarray[0,1] = Sarray[1,0]
    Sarray[2,2] = (2+2*self.v)/self.E
    C[:,:] = np.round( np.linalg.inv(Sarray[:,:]), 2 )
    return C

  def computeH(self, H):
    Sarray = np.zeros((2,2))
    Sarray[0,0] = (2+2*self.v)/self.E
    Sarray[1,1] = (2+2*self.v)/self.E
    H[:,:] = np.round( np.linalg.inv(Sarray), 2 )
    return H

  def getEvec(self, vec):
      return np.array([self.E,self.E,self.E])

class TranIso(CT):
  # https://www.efunda.com/formulae/solid_mechanics/mat_mechanics/hooke_iso_transverse.cfm
  def __init__(self):
    super(TranIso, self).__init__()

  def read(self, lines, line):    
    while line[0] != "end":        
      if line[0] == "ep":
        self.Ep = float( line[2] )
      if line[0] == "vp":
        self.vp = float( line[2] )  
      if line[0] == "epz":
        self.Epz = float( line[2] )
      if line[0] == "vpz":
        self.vpz = float( line[2] )
      if line[0] == "gpz":
        self.Gpz = float( line[2] )
      lines, line = nextLine(lines)

  def check(self):
    flag = True
    if self.Ep  <= 0:
      flag = False
    if self.Epz <= 0:
      flag = False
    if self.Gpz <= 0:
      flag = False
    return flag

  def compute3D(self, C):
    Sarray = np.zeros((6,6))
    Sarray[0,0] = 1/self.Ep
    Sarray[1,1] = 1/self.Ep
    Sarray[2,2] = 1/self.Epz
    Sarray[1,0] = -self.vp/self.Ep
    Sarray[2,0] = -self.vpz/self.Ep
    Sarray[2,1] = -self.vpz/self.Ep
    Sarray[0,1] = Sarray[1,0]
    Sarray[0,2] = Sarray[2,0]
    Sarray[1,2] = Sarray[2,1]
    Sarray[3,3] = (2+2*self.vp)/self.Ep
    Sarray[4,4] = 1/self.Gpz
    Sarray[5,5] = 1/self.Gpz
    C[:,:] = np.round( np.linalg.inv(Sarray), 2 )
    return C

  def computePS(self, C):
    Sarray = np.zeros((3,3))
    Sarray[0,0] = 1/self.Ep
    Sarray[1,1] = 1/self.Ep
    Sarray[0,1] = -self.vp/self.Ep
    Sarray[1,0] = Sarray[0,1]
    Sarray[2,2] = (2+2*self.vp)/self.Ep
    C[:,:] = np.round( np.linalg.inv(Sarray), 2 )
    return C

  def computeH(self, H):
    Sarray = np.zeros((2,2))
    Sarray[0,0] = 1/self.Gpz
    Sarray[1,1] = 1/self.Gpz
    H[:,:] = np.round( np.linalg.inv(Sarray), 2 )
    return H

  def getEvec(self, vec):
      return np.array([self.Ep,self.Ep,self.Ep])

class Orthotrop(CT):
  def __init__(self):
    super(Orthotrop, self).__init__()

  def read(self, lines, line):    
    while line[0] != "end":        
      if line[0] == "e11":
        self.E11 = float( line[2] ) 
      if line[0] == "e22":
        self.E22 = float( line[2] ) 
      if line[0] == "e33":
        self.E33 = float( line[2] ) 
      if line[0] == "g12":
        self.G12 = float( line[2] ) 
      if line[0] == "g13":
        self.G13 = float( line[2] ) 
      if line[0] == "g23":
        self.G23 = float( line[2] )
      if line[0] == "v12":
        self.v12 = float( line[2] )
      if line[0] == "v13":
        self.v13 = float( line[2] )
      if line[0] == "v23":
        self.v23 = float( line[2] )
      lines, line = nextLine(lines)

  def check(self):
    flag = True
    if self.E11 <= 0:
      flag = False
    if self.E22 <= 0:
      flag = False
    if self.E33 <= 0:
      flag = False
    if self.G12 <= 0:
      flag = False
    if self.G13 <= 0:
      flag = False
    if self.G23 <= 0:
      flag = False
    return flag

  def compute3D(self, C):
    Sarray = np.zeros((6,6))
    Sarray[0,0] = 1/self.E11
    Sarray[1,1] = 1/self.E22
    Sarray[2,2] = 1/self.E33
    Sarray[1,0] = -self.v12/self.E11
    Sarray[2,0] = -self.v13/self.E11
    Sarray[2,1] = -self.v23/self.E22
    Sarray[0,1] = Sarray[1,0]
    Sarray[0,2] = Sarray[2,0]
    Sarray[1,2] = Sarray[2,1]
    Sarray[3,3] = 1/self.G12
    Sarray[4,4] = 1/self.G13
    Sarray[5,5] = 1/self.G23
    C[:,:] = np.round( np.linalg.inv(Sarray), 2 )

  def computePS(self, C):
    Sarray = np.zeros((3,3))
    Sarray[0,0] = 1/self.E11
    Sarray[1,1] = 1/self.E22
    Sarray[1,0] = -self.v12/self.E11
    Sarray[0,1] = Sarray[1,0]
    Sarray[2,2] = 1/self.G12
    C[:,:] = np.round( np.linalg.inv(Sarray), 2 )

  def computeH(self, H):
    Sarray = np.zeros((2,2))
    Sarray[0,0] = 1/self.G13
    Sarray[1,1] = 1/self.G23
    H[:,:] = np.round( np.linalg.inv(Sarray), 2 )

  def getEvec(self, vec):
      return np.array([self.E11,self.E22,self.E33])

def nextLine(lines):
    line = lines.pop(0).lower().split(); line.append("")
    return lines, line


