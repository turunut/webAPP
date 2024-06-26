import mesop as me

def tab_ABD():
  me.text("Page 2")

  #src = "file:///C:/Users/fturo/Documents/webAPP/HW.html"
  src = "https://google.github.io/mesop/"
  me.embed(
    src=src,
    style=me.Style(width="100%", height=500),
  )