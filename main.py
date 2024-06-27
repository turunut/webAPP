import mesop as me

#import debugpy

from tab_About import tab_About
from tab_CT    import tab_CT
from tab_ABD   import tab_ABD

from modState import State

#debugpy.listen(5678)

# @me.page(path="/multi_page_nav/page_2")
@me.page(security_policy=me.SecurityPolicy(allowed_iframe_parents=["https://google.github.io"]),path="/",)
def app():

  state = me.state(State)

  with me.box(style=me.Style(width=1200)):

    with me.box(style=me.Style(padding=me.Padding.all(20))):
    
      with me.box(style=me.Style(background="white")):
        me.button("About",               on_click=on_click_page_1, color=state.lst_colr[0])
        me.button("Constitutive Tensor", on_click=on_click_page_2, color=state.lst_colr[1])
        me.button("Laminate Stiffness",  on_click=on_click_page_3, color=state.lst_colr[2])
        me.divider()
      
      with me.box(style=me.Style(visibility=state.lst_vsblty[0],height=state.lst_height[0],),):
        #me.text("1")
        tab_About()
      
      with me.box(style=me.Style(visibility=state.lst_vsblty[1],height=state.lst_height[1],),):
        #me.text("2")
        tab_CT()
      
      with me.box(style=me.Style(visibility=state.lst_vsblty[2],height=state.lst_height[2],),):
        #me.text("3")
        tab_ABD()

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

