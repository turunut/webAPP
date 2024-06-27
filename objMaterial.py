import numpy as np

import objCT
import objRotator

class Material:
  def __init__(self):
    self.rotator = objRotator.NOTRotator()
    self.CT      = None
      
  def read(self, lines, line):
    while (line[0:2] != ["end","material"]) and (len(lines) != 0):
      line = lines.pop(0).lower().split(); line.append("")
      
      if line[0] == "ct:":
          self.CT = objCT.CTFactory(line[1])
          self.CT.read(lines, line)
      
      if line[0].lower() == "rotation:":
          vecRot = np.array([float(num) for num in line[1:-1]])
          self.rotator = objRotator.RotatorFactory(vecRot)
      
      lines = self.readSpecific(lines, line)
      
    return lines

  def readSpecific(self, lines, line):
    return lines

  #def get_LocalCT_SLD(self, C):
  #  self.CT.compute3D(C)
  #  return C
  #
  #def get_GloblCT_SLD(self, C):
  #  self.CT.compute3D(C)
  #  self.rotator.Loc2Glo(C)
  #  return C
  #
  #def get_LocalCT_PSS(self, C):
  #  self.CT.computePS(C)
  #  return C
  #
  #def get_GloblCT_PSS(self, C):
  #  self.CT.computePS(C)
  #  self.rotator.Loc2Glo(C)
  #  return C

  @staticmethod
  def return_input(A):
    return A

  def get_CT_SLD(self, C, i):
    myFun = [self.return_input, self.rotator.Loc2Glo]
    self.CT.compute3D(C)
    return myFun[i](C)
  
  def get_CT_PSS(self, C, i):
    myFun = [self.return_input, self.rotator.Loc2Glo]
    self.CT.computePS(C)
    return myFun[i](C)



class Laminate(Material):
  def __init__(self):
    self.layers = []
      
  def read(self, lines, line):
    while (line[0:2] != ["end","laminate"]) and (len(lines) != 0):
      line = lines.pop(0).lower().split(); line.append("")
      
      if line[0:2] == ["begin","material"]:
        lay = Layer()
        lines = lay.read(lines,line)
        self.layers.append(lay)
    
    return lines

  def get_CT_ABD(self, ABD, i):
    temp = np.zeros((3,3))
    for layer in self.layers:
      layer.CT.computePS(temp[:,:])
      ABD[0:3,0:3] +=       (layer.zmax   -layer.zmin   ) * temp[:,:]
      ABD[0:3,3:6] += 1/2 * (layer.zmax**2-layer.zmin**2) * temp[:,:]
      ABD[3:6,3:6] += 1/3 * (layer.zmax**3-layer.zmin**3) * temp[:,:]
    ABD[3:6,0:3] = ABD[0:3,3:6]

    #return [ self.CT.compute3D(C), self.rotator.Loc2Glo(self.CT.compute3D(C)) ][i]
    #return [ ABD, ABD ][i]

  def get_CT_H(self, H, i):
    temp = np.ones((2,2))
    for layer in self.layers:
      layer.CT.computeH(temp[:,:])
      H[:,:] += (layer.zmax - layer.zmin ) * temp[:,:]

  def get_CT_PSS(self, C, i):      
    return [ self.CT.computePS(C), self.rotator.Loc2Glo(self.CT.computePS(C)) ][i]

  def computeShearCorrector(self):
    zMidline = - self.CTarray[0,1]/self.CTarray[0,0]
    
    DdNL = 0.0
    DbNL = 0.0
    for layer in self.layers:
      z1   = layer.z1 + zMidline
      z2   = layer.z2 + zMidline
      E    = layer.getE([1.0,0.0,0.0])
      DbNL += E*(z2**2-z1**2)*(1/2)
      DdNL += E*(z2**3-z1**3)*(1/3)
  
    if DbNL > 0.000001:
      print("Db is not 0 when computing shear corrector factor.")
  
    Ds = self.CTarray[2,2]
  
    for layer in self.layers:
      SUM = 0.0
      for indexR, LayerActual in enumerate(self.layers):
        R = 0.0
        for LayerAnterior in self.layers[0:indexR]:
          z1 = LayerAnterior.z1 + zMidline
          z2 = LayerAnterior.z2 + zMidline
          E  = LayerAnterior.getE([1.0,0.0,0.0])
          G  = LayerAnterior.getG([1.0,0.0,0.0])
    
          R += (z2**2-z1**2)*E
    
        z1 = LayerActual.z1 + zMidline
        z2 = LayerActual.z2 + zMidline
        E  = LayerActual.getE([1.0,0.0,0.0])
        G  = LayerActual.getG([1.0,0.0,0.0])
    
        R = - E*z1**2 + R
    
        Si = ((1/5)*E**2*z2**5+(2/3)*R*E*z2**3+R**2*z2) - ((1/5)*E**2*z1**5+(2/3)*R*E*z1**3+R**2*z1)
        Si = Si*1/(4*G)
        SUM += Si
    
    factorK = ((DdNL**2)/((Ds)))*(1/SUM)
  
    print("The shear corrector factor is :" + str(factorK))
    
    return factorK



class Layer(Material):
  def __init__(self):
    super(Layer, self).__init__()
    self.zmin = 0.0
    self.zmax = 0.0

  def readSpecific(self, lines, line):
    if line[0] == "zmin":
      self.zmin = float(line[2])
    if line[0] == "zmax":
      self.zmax = float(line[2])
    return lines
  

#c = Material()
##causes an error if any field in someclass has another class instance. 
#import json  
#json.dumps(Material) 