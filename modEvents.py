import mesop as me

from modState import State

def on_prompt_input(e: me.InputEvent):
  state = me.state(State)
  state.inputCT = e.value