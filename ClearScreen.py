import os
import time

def cls():
    #Step 1
    clear = lambda: os.system('cls')
    clear()

    #Step 2
    os.system('cls')

def main():
    print('#'*100)
    time.sleep(5)
    cls()
    time.sleep(5)

if __name__ == '__main__':
    main()