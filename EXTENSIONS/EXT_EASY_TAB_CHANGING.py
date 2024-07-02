"""
    ! EASY TAB CHANGING ! 
    *   This is NOT a custom made extension, it comes with the editor but you can decide if you use it or not
    *   This extension can be enabled and disabled in the editor
"""

import SHARED_STATE
root = SHARED_STATE.SHARED_root
ChangeTabs = SHARED_STATE.SHARED_ChangeTabs

def _change_tab1(event):
    ChangeTabs(1)
def _change_tab2(event):
    ChangeTabs(2)
def _change_tab3(event):
    ChangeTabs(3)
def _change_tab4(event):
    ChangeTabs(4)
    
def EXT_EASY_TAB_CHANGING():
    print("|-[+]-| EASY TAB CHANGING |-[+]-|")
    root.bind('<Alt-KeyPress-1>', _change_tab1)
    root.bind('<Alt-KeyPress-2>', _change_tab2)
    root.bind('<Alt-KeyPress-3>', _change_tab3)
    root.bind('<Alt-KeyPress-4>', _change_tab4)