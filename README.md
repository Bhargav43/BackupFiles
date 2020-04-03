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

## Hidden Modules
* os *[Built-in]*
* time *[Built-in]*
* shutil *[Built-in]*
* functools *[Built-in]*
* re *[Built-in]*
* sys *[Built-in]*
* TraceFuncCalls *[Added Script]*
* ClearScreen *[Added Script]*


### Added Scripts
#### TraceFuncCalls


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
