#Reference: https://stackoverflow.com/a/8315566/9207580

import sys
keyword = ' '


def tracefunc(frame, event, arg, indent=[0]):
    keywords = [i.strip() for i in keyword.split(',')]
    for key in keywords:
        if frame.f_code.co_name.startswith(key):
            if event == "call":
                indent[0] += 2
                print("-" * indent[0] + "> call function", frame.f_code.co_name)
            elif event == "return":
                print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
                indent[0] -= 2
    return tracefunc

def test():
    pass

def main():
    sys.setprofile(tracefunc)
    test()
    print('Module: ', __file__)
    print('Function: ', __name__)
    print(keyword)


if __name__ == '__main__':
    main()


#Sample for Importing In Another File#
'''import sys
import TraceFuncCalls as trc

def functionName():
    pass

def AnotherfunctionName():
    pass

def FunctionNotCalled():
    #Defined but not called
    pass

sys.setprofile(trc.tracefunc)
trc.keyword = 'functionName, AnotherfunctionName, InvalidFunName, FunctionNotCalled'

functionName()
AnotherfunctionName()
'''
