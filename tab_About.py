import mesop as me
from modEvents import on_prompt_input

def tab_About():
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