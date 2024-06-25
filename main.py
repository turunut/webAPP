import mesop as me
import pandas as pd
import numpy as np

from tab_CT import tab_3
from modEvents import on_prompt_input

from modState import State
  
def tab_1():

  me.textarea(label="Basic input", on_input=on_prompt_input)

  #df = pd.DataFrame(data={"col1": [11, 12, 13, 14, 15, 16],
  #                        "col2": [21, 22, 23, 24, 25, 26],
  #                        "col3": [31, 32, 33, 34, 35, 36],
  #                        "col4": [41, 42, 43, 44, 45, 46],
  #                        "col5": [51, 52, 53, 54, 55, 56],
  #                        "col6": [61, 62, 63, 64, 65, 66]})
  #
  #with me.box(style=me.Style(width=500)):
  #  me.table(df, header=me.TableHeader(sticky=False))

def tab_2():
  me.text("Page 2")

  #src = "file:///C:/Users/fturo/Documents/webAPP/HW.html"
  src = "https://google.github.io/mesop/"
  me.embed(
    src=src,
    style=me.Style(width="100%", height=500),
  )



@me.page(security_policy=me.SecurityPolicy(allowed_iframe_parents=["https://google.github.io"]),path="/",)
def app():

  state = me.state(State)

  with me.box(style=me.Style(width=1200)):

    with me.box(style=me.Style(padding=me.Padding.all(20))):
    
      with me.box(style=me.Style(background="white")):
        me.button("Constitutive Tensor", on_click=on_click_page_1, color=state.lst_colr[0])
        me.button("Laminate Stiffness", on_click=on_click_page_2, color=state.lst_colr[1])
        me.button("but3", on_click=on_click_page_3, color=state.lst_colr[2])
        me.divider()
      
      with me.box(style=me.Style(visibility=state.lst_vsblty[0],height=state.lst_height[0],),):
        tab_1()
      
      with me.box(style=me.Style(visibility=state.lst_vsblty[1],height=state.lst_height[1],),):
        tab_2()
      
      with me.box(style=me.Style(visibility=state.lst_vsblty[2],height=state.lst_height[2],),):
        tab_3()

def on_click_page_1(e: me.ClickEvent):
  state = me.state(State)
  state.lst_colr   = ["primary","accent","accent"]
  state.lst_vsblty = ["visible","hidden","hidden"]
  state.lst_height = [None,0,0]
  
def on_click_page_2(e: me.ClickEvent):
  state = me.state(State)
  state.lst_colr   = ["accent","primary","accent"]
  state.lst_vsblty = ["hidden","visible","hidden"]
  state.lst_height = [0,None,0]
  
def on_click_page_3(e: me.ClickEvent):
  state = me.state(State)
  state.lst_colr   = ["accent","accent","primary"]
  state.lst_vsblty = ["hidden","hidden","visible"]
  state.lst_height = [0,0,None]

