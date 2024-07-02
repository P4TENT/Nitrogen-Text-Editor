import JSON
def ExtensionRunner():
    Info = JSON.JsonGetInfo("Info.json")
    ExtensionInfo = Info["EXTENSION-PACK"]
    del Info
    with open("ExecExtensions.py", 'w') as file:
        file.write("")
    
    with open("ExecExtensions.py", 'a') as file:   
        for key in ExtensionInfo:
            file.write(f"from EXTENSIONS.{key} import *\n")
        
        file.write("def EXECUTE_EXTENSION():\n")
        for key in ExtensionInfo:
            file.write(f"  {key}()\n")
    
    import ExecExtensions
    ExecExtensions.EXECUTE_EXTENSION()