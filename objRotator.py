import numpy as np
import math

def RotatorFactory(vecRot):
  r = np.linalg.norm(vecRot)
  if r > 0.0:
    return YESRotator(vecRot)

class Rotator:
    def Loc2Glo(self, C):
        return C
        
class NOTRotator(Rotator):
    def __init__(self):
        pass

class YESRotator(Rotator):
    def __init__(self, angles):
        self.angles = angles
    
    def Loc2Glo(self, C):
        index = int( C.shape[0] / 3 - 1 )

        myFun = [self.Loc2GloPS, self.Loc2Glo3D]

        return myFun[index](C)

    def Loc2GloPS(self, C):
        ang = -np.radians(self.angles[0])

        l1 = math.cos(float(ang)) ; l2 = -math.sin(float(ang))
        m1 = math.sin(float(ang)) ; m2 =  math.cos(float(ang))
        
        OpeA = np.array([[ l1, l2],
                         [ m1, m2]])
        
        OpeR = np.array([[ l1**2, l2**2,     2*l1*l2],
                         [ m1**2, m2**2,     2*m1*m2],
                         [ l1*m1, l2*m2, l1*m2+m1*l2]])

        OpeRbar = np.array([[   l1**2,   l2**2,       l1*l2],
                            [   m1**2,   m2**2,       m1*m2],
                            [ 2*l1*m1, 2*l2*m2, l1*m2+m1*l2]])
        
        return np.matmul( OpeR, np.matmul(C,np.transpose(OpeR)))

    def Loc2Glo3D(self, C):
        FI	  = math.radians(self.angles[0])
        TETHA = math.radians(self.angles[1])
        HI	  = math.radians(self.angles[2])
      
        c1 = math.cos(FI)
        s1 = math.sin(FI)
        c2 = math.cos(TETHA)
        s2 = math.sin(TETHA)
        c3 = math.cos(HI)
        s3 = math.sin(HI)

        l1 = c1*c3 - s1*c2*s3   ;  l2 = -c1*s3 - s1*c2*c3  ;  l3 = s1*s2
        m1 = s1*c3 + c1*c2*s3   ;  m2 = -s1*s3 + c1*c2*c3  ;  m3 = -c1*s2
        n1 = s2*s3              ;  n2 = s2*c3              ;  n3 = c2
        
        OpeA = np.zeros((3,3))
        
        OpeA[0,0] = l1 ;  OpeA[0,1] = l2 ;  OpeA[0,2] = l3
        OpeA[1,0] = m1 ;  OpeA[1,1] = m2 ;  OpeA[1,2] = m3
        OpeA[2,0] = n1 ;  OpeA[2,1] = n2 ;  OpeA[2,2] = n3
        
        OpeR = np.zeros((6,6))
        
        OpeR[1-1,1-1] = l1**2          ; OpeR[1-1,2-1] = l2**2           ;  OpeR[1-1,3-1] = l3**2
        OpeR[1-1,4-1] = 2*l1*l2        ; OpeR[1-1,5-1] = 2*l1*l3         ;  OpeR[1-1,6-1] = 2*l2*l3
        OpeR[2-1,1-1] = m1**2          ; OpeR[2-1,2-1] = m2**2           ;  OpeR[2-1,3-1] = m3**2
        OpeR[2-1,4-1] = 2*m1*m2        ; OpeR[2-1,5-1] = 2*m1*m3         ;  OpeR[2-1,6-1] = 2*m2*m3
        OpeR[3-1,1-1] = n1**2          ; OpeR[3-1,2-1] = n2**2           ;  OpeR[3-1,3-1] = n3**2
        OpeR[3-1,4-1] = 2*n1*n2        ; OpeR[3-1,5-1] = 2*n1*n3         ;  OpeR[3-1,6-1] = 2*n2*n3
        OpeR[4-1,1-1] = l1*m1          ; OpeR[4-1,2-1] = l2*m2           ;  OpeR[4-1,3-1] = l3*m3
        OpeR[4-1,4-1] = l1*m2 + l2*m1  ; OpeR[4-1,5-1] = l1*m3 + l3*m1   ;  OpeR[4-1,6-1] = l2*m3 + l3*m2
        OpeR[5-1,1-1] = l1*n1          ; OpeR[5-1,2-1] = l2*n2           ;  OpeR[5-1,3-1] = l3*n3
        OpeR[5-1,4-1] = l1*n2 + l2*n1  ; OpeR[5-1,5-1] = l1*n3 + l3*n1   ;  OpeR[5-1,6-1] = l2*n3 + l3*n2
        OpeR[6-1,1-1] = m1*n1          ; OpeR[6-1,2-1] = m2*n2           ;  OpeR[6-1,3-1] = m3*n3
        OpeR[6-1,4-1] = m1*n2 + m2*n1  ; OpeR[6-1,5-1] = m1*n3 + m3*n1   ;  OpeR[6-1,6-1] = m2*n3 + m3*n2

        OpeRbar = np.zeros((6,6))
        
        OpeRbar[1-1,1-1] = l1**2          ; OpeRbar[1-1,2-1] = l2**2           ;  OpeRbar[1-1,3-1] = l3**2
        OpeRbar[1-1,4-1] = l1*l2          ; OpeRbar[1-1,5-1] = l1*l3           ;  OpeRbar[1-1,6-1] = l2*l3
        OpeRbar[2-1,1-1] = m1**2          ; OpeRbar[2-1,2-1] = m2**2           ;  OpeRbar[2-1,3-1] = m3**2
        OpeRbar[2-1,4-1] = m1*m2          ; OpeRbar[2-1,5-1] = m1*m3           ;  OpeRbar[2-1,6-1] = m2*m3
        OpeRbar[3-1,1-1] = n1**2          ; OpeRbar[3-1,2-1] = n2**2           ;  OpeRbar[3-1,3-1] = n3**2
        OpeRbar[3-1,4-1] = n1*n2          ; OpeRbar[3-1,5-1] = n1*n3           ;  OpeRbar[3-1,6-1] = n2*n3
        OpeRbar[4-1,1-1] = 2*l1*m1        ; OpeRbar[4-1,2-1] = 2*l2*m2         ;  OpeRbar[4-1,3-1] = 2*l3*m3
        OpeRbar[4-1,4-1] = l1*m2 + l2*m1  ; OpeRbar[4-1,5-1] = l1*m3 + l3*m1   ;  OpeRbar[4-1,6-1] = l2*m3 + l3*m2
        OpeRbar[5-1,1-1] = 2*l1*n1        ; OpeRbar[5-1,2-1] = 2*l2*n2         ;  OpeRbar[5-1,3-1] = 2*l3*n3
        OpeRbar[5-1,4-1] = l1*n2 + l2*n1  ; OpeRbar[5-1,5-1] = l1*n3 + l3*n1   ;  OpeRbar[5-1,6-1] = l2*n3 + l3*n2
        OpeRbar[6-1,1-1] = 2*m1*n1        ; OpeRbar[6-1,2-1] = 2*m2*n2         ;  OpeRbar[6-1,3-1] = 2*m3*n3
        OpeRbar[6-1,4-1] = m1*n2 + m2*n1  ; OpeRbar[6-1,5-1] = m1*n3 + m3*n1   ;  OpeRbar[6-1,6-1] = m2*n3 + m3*n2

        return np.matmul( OpeR, np.matmul(C,np.transpose(OpeR)))
        


        
