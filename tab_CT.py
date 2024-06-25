import mesop as me
from modEvents import on_prompt_input
import numpy as np

from modState import State

import objMaterial

def tab_3():
  state = me.state(State)

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
  
  me.textarea(label="Basic input", on_input=on_prompt_input, autosize=True, min_rows=10, style=me.Style(width=600))
    
  with me.box():
    me.button("Compute", on_click=computeCT, type="raised")

  me.markdown("####Solido")
  
  with me.box(style=me.Style(display="flex", column_gap="1em")):
    with me.box():
      for i in range(0,len(state.outptCT_SLD)):
        me.text(np.array2string( np.asarray(state.outptCT_SLD[i])[:], prefix='     ', suppress_small=True, precision=3)[1:-1] )
    with me.box():
      for i in range(0,len(state.outptCT_SLD_rot)):
        me.text(np.array2string( np.asarray(state.outptCT_SLD_rot[i])[:], prefix='     ', suppress_small=True, precision=3)[1:-1] )

  me.markdown("####Plane Stress")

  with me.box(style=me.Style(display="flex", column_gap="1em")):
    with me.box():
      for i in range(0,len(state.outptCT_PSS)):
        me.text(np.array2string( np.asarray(state.outptCT_PSS[i])[:], prefix='     ', suppress_small=True, precision=3)[1:-1] )
    with me.box():
      for i in range(0,len(state.outptCT_PSS_rot)):
        me.text(np.array2string( np.asarray(state.outptCT_PSS_rot[i])[:], prefix='     ', suppress_small=True, precision=3)[1:-1] )



def computeCT(e: me.ClickEvent):
  state = me.state(State)
  
  textfield = state.inputCT
  lines = textfield.split("\n")

  mat = objMaterial.Material()
    
  line = lines.pop(0).lower().split(); line.append("")
  lines = mat.read(lines, line)

  CT3D = np.zeros((6,6)); CT3D_rot = np.zeros((6,6))
  CTPS = np.zeros((3,3)); CTPS_rot = np.zeros((3,3))

  mat.getCT_SLD(CT3D, 0)
  state.outptCT_SLD = CT3D.tolist()
  
  mat.getCT_SLD(CT3D_rot, 1)
  state.outptCT_SLD_rot = CT3D_rot.tolist()

  mat.getCT_PSS(CTPS, 0)
  state.outptCT_PSS = CTPS.tolist()
  
  mat.getCT_PSS(CTPS_rot, 1)
  state.outptCT_PSS_rot = CTPS_rot.tolist()

  state.outptCT = state.inputCT

_HEAD = me.Style(
  display="grid",
  columns=3,
  grid_template_columns="1fr 1fr 1fr",
  #grid_template_rows="auto 5fr",
  width=600,
)