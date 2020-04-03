# BackupFiles 1.1.0 2-Apr-2020

## Purpose
For taking the backups of (small to large) files and folders in the local system, much like the version-control in Git. There isn't limitation of type of file. The transfer rate is as high as 16 MBPS. The backup file or folder will have a local system's timestamp appended so as to not to disturb the original.

## Base System's Configurations
**Sno.** | **Name** | **Version/Config.**
-------: | :------: | :------------------
1 | Operating System | Windows 10 x64 bit
2 | Python | Version 3.7.0 x64 bit
3 | PyInstaller | Version 3.6
4 | IDE | Pyzo 4.10.2 x64 bit

## Imported Modules
Sn | **Module** | **Type**
-: | :--------: | :-------
1 | os | *Built-in*
2 | time | *Built-in*
3 | shutil | *Built-in*
4 | functools | *Built-in*
5 | re | *Built-in*
6 | sys | *Built-in*
7 | TraceFuncCalls | *Added Script*
8 | ClearScreen | *Added Script*


### Added Scripts
#### [TraceFuncCalls](https://github.com/Bhargav43/BackupFiles/blob/master/TraceFuncCalls.py)
_This is for tracing the all in-built and user-defined functions called throughout the execution of the program. `TraceFunCalls` had no effect on `BackUpFile1.1.0` 's  output, but was used for developement purpose. Logic is as follows:_

```python
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
```

#### [ClearScreen](https://github.com/Bhargav43/BackupFiles/blob/master/ClearScreen.py)
_Compared to remaining, this is a simple 2 line script used for clearing-up the console screen. Not heavy, but handy to import rather than checking either types, everytime. `ClearScreen` is used in `BackupFiles1.1.0` to clear the screen just before displaying summery of the execution. As follows:_
```python
def cls():
    #Step 1
    clear = lambda: os.system('cls')
    clear()

    #Step 2
    os.system('cls')
```
