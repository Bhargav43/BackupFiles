# BackupFiles 1.1.0 2-Apr-2020

## Purpose
Takes the backup of files (small to large) and folders as well, in the local system. This doesn't have the limitation on type of files to backup. This is more or less similar to the version-control feature in Git, except, it is manual and local.
The transfer rate is as high as 16 MBPS. Also, it appends a local machine's timestamp to the file/folder name in order to avoid overwriting and keeping a track.

The _Prime Intention_ was to develop a code to reduce my manual work of opening a new file and copying all the existing content onto it every time before starting reconstruction or performing the trials for enhancements. The [executable](https://github.com/Bhargav43/BackupFiles/blob/master/BackupFiles.exe) works perfectly to my daily usage.

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
