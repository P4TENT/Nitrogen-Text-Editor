import SHARED_STATE
def _easter_egg(event):
    SHARED_STATE.SHARED_root.configure(fg_color="#B9D9EB")
    SHARED_STATE.SHARED_text_area.configure(fg_color="#FF91AF")
    SHARED_STATE.SHARED_LineCount_label.configure(text_color="#FF91AF")
            
def EXT_NITROGEN_EASTER_EGG():
    print("|-[+]-| NITROGEN EASTER EGG |-[+]-|")
    SHARED_STATE.SHARED_root.bind('<Alt-n>', _easter_egg)