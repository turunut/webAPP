import mesop as me
import numpy as np

from modState import State

import objMaterial

def tab_ABD():
  state = me.state(State)

  me.markdown("###Laminates CT matrices, ABD and H")
  me.text("Definition of the laminar constitutive tensors following tthe Timoshenko kinematics.")

  txt_iso = """
    begin laminate
      begin material
         CT: Isotrop
           E = 72400.0
           v = 0.33
         end CT
         zmin = -5.0
         zmax = -4.0
      end material
      begin material
         CT: Isotrop
           E = 1000.0
           v = 0.4
         end CT
         zmin = -4.0
         zmax = 4.0
      end material
      begin material
         CT: Isotrop
           E = 72400.0
           v = 0.33
         end CT
         zmin = 4.0
         zmax = 5.0
      end material
    end laminate
  """

  txt_trv = """
  """

  txt_ort = """
  """

  with me.box(style=_HEAD):
    with me.box():
      me.markdown("####Example 1")
      me.markdown(txt_iso)
      
    with me.box():
      me.markdown("####Example 2")
      me.markdown(txt_trv)

    with me.box():
      me.markdown("####Example 3")
      me.markdown(txt_ort)
  
  me.textarea(label="Basic input", on_input=on_prompt_input, autosize=True, min_rows=10, style=me.Style(width=600))
    
  with me.box():
    me.button("Compute", on_click=computeCT, type="raised")

  me.markdown("####ABD Matrix (Unrotated/Rotated)")
  
  with me.box(style=me.Style(display="flex", column_gap="1em")):
    with me.box():
      for i in range(0,len(state.outptCT_SLD)):
        me.text(np.array2string( np.asarray(state.outptABD[i])[:], suppress_small=True, precision=2)[1:-1] )
    with me.box():
      for i in range(0,len(state.outptCT_SLD_rot)):
        me.text(np.array2string( np.asarray(state.outptABD_rot[i])[:], suppress_small=True, precision=2)[1:-1] )

def on_prompt_input(e: me.InputEvent):
  state = me.state(State)
  state.inputABD = e.value

def computeCT(e: me.ClickEvent):
  state = me.state(State)
  
  textfield = state.inputABD
  lines = textfield.split("\n")

  lam = objMaterial.Laminate()
    
  line = lines.pop(0).lower().split(); line.append("")
  lines = lam.read(lines, line)

  ABD = np.zeros((6,6)); ABD_rot = np.zeros((6,6))

  lam.get_CT_ABD(ABD,     0)
  state.outptABD[:]     = ABD.tolist()
  
  lam.get_CT_ABD(ABD_rot, 1)
  state.outptABD_rot[:] = ABD_rot.tolist()

_HEAD = me.Style(
  display="grid",
  columns=3,
  grid_template_columns="1fr 1fr 1fr",
  #grid_template_rows="auto 5fr",
  width=600,
)