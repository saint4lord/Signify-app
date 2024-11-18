import time
import os
import sys

def type_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def main():
    
    ascii_art = r"""
  ______    ______     __         
 /      \  /      \  _/  |        
/$$$$$$  |/$$$$$$  |/ $$ |        
$$ \__$$/ $$$  \$$ |$$$$ | ______ 
$$      \ $$$$  $$ |  $$ |/      |
$$$$$$$  |$$ $$ $$ |  $$ |$$$$$$/ 
$$ \__$$ |$$ \$$$$ | _$$ |_       
$$    $$/ $$   $$$/ / $$   |      
 $$$$$$/   $$$$$$/  $$$$$$/    
    """

    # clean cmd
    os.system("cls" if os.name == "nt" else "clear")
    print("\nWelcome to Signify Gesture Recognition!")
    time.sleep(1)

    # run effect
    type_effect(ascii_art, delay=0.01)  # delay between sybmols

    # other effects
    type_effect("\nSystem Initializing...", delay=0.04)
    time.sleep(0.5)
    type_effect("Loading Modules...", delay=0.04)
    time.sleep(0.5)
    type_effect("Starting Camera...", delay=0.06)
    time.sleep(1)

if __name__ == "__main__":
    main()
