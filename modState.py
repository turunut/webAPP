import mesop as me
from dataclasses import field
import numpy as np
from objMaterial import Material

@me.stateclass
class State:
  inputCT: str = ""

  outptCT_SLD:     list[list[float]] = field(default_factory=lambda: np.zeros((6,6)).tolist() )
  outptCT_SLD_rot: list[list[float]] = field(default_factory=lambda: np.zeros((6,6)).tolist() )

  outptCT_PSS:     list[list[float]] = field(default_factory=lambda: np.zeros((3,3)).tolist() )
  outptCT_PSS_rot: list[list[float]] = field(default_factory=lambda: np.zeros((3,3)).tolist() )

  lst_colr:   list[str] = field(default_factory=lambda: ["primary","accent","accent"])
  lst_vsblty: list[str] = field(default_factory=lambda: ["visible","hidden","hidden"])
  lst_height: list[int] = field(default_factory=lambda: [None,0,0])