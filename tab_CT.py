import mesop as me
from modEvents import on_prompt_input
import numpy as np

from modState import State

import objMaterial

def tab_3():
  me.markdown("###Constutive tensor")
  me.text("Aqui va data")

  txt_iso = """
    begin material
      CT: Isotrop
        E = 10000.0
        v = 0.21
      end CT
    end material
  """

  txt_trv = """
    begin material
      CT: TranIso
        Ep = 10000.0
        vp = 0.21
        Epz = 15000.0
        vpz = 0.33
        Gpz = 4000.0
      end CT
    end material
  """

  txt_ort = """
    begin material
      CT: Orthotrop
        E11 = 20000.0
        E22 = 10000.0
        E33 = 10000.0
        G12 =  4000.0
        G13 =  4000.0
        G23 =  4000.0
        v12 =     0.3
        v13 =     0.3
        v23 =     0.3
      end CT
      rotation: 30 30 30
    end material
  """

  with me.box(style=_HEAD):
    with me.box():
      me.markdown("####Isotrop")
      me.markdown(txt_iso)
      
    with me.box():
      me.markdown("####Transv. Isotrop")
      me.markdown(txt_trv)

    with me.box():
      me.markdown("####Orthotrop")
      me.markdown(txt_ort)
  
  me.textarea(label="Basic input", on_input=on_prompt_input, style=me.Style(width=600))
    
  with me.box():
    me.button("Compute", on_click=computeCT, type="raised")

  me.text("holahola")

def computeCT(e: me.ClickEvent):
  state = me.state(State)
  
  textfield = state.inputCT
  lines = textfield.split("\n")

  mat = objMaterial.Material()
    
  line = lines.pop(0).lower().split(); line.append("")
  lines = mat.read(lines, line)

  CT3D = np.zeros((6,6)); CTPS = np.zeros((3,3))

  me.text(np.array2string(CT3D))
  me.text(np.array2string(mat.getCT_3D(CT3D, 0)) )
  #output_div = document.querySelector("#CT_3D_rot")
  #printArray(output_div, mat.getCT_3D(CT3D, 1) )
  #  
  #output_div = document.querySelector("#CT_PS")
  #printArray(output_div, mat.getCT_PS(CTPS, 0) )
  #output_div = document.querySelector("#CT_PS_rot")
  #printArray(output_div, mat.getCT_PS(CTPS, 1) )

  state.outptCT = state.inputCT

_HEAD = me.Style(
  display="grid",
  columns=3,
  grid_template_columns="1fr 1fr 1fr",
  #grid_template_rows="auto 5fr",
  width=600,
)