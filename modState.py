import mesop as me
from dataclasses import field

@me.stateclass
class State:
  inputCT: str = ""
  outptCT: str = ""

  lst_colr:   list[str] = field(default_factory=lambda: ["primary","accent","accent"])
  lst_vsblty: list[str] = field(default_factory=lambda: ["visible","hidden","hidden"])
  lst_height: list[int] = field(default_factory=lambda: [None,0,0])