# :metal::sunglasses::metal: BackupFiles 1.1.0 :metal::sunglasses::metal: 

## Purpose :bulb:
Takes the backup of files (small to large) and folders as well, in the local system. This doesn't have the limitation on type of files to backup. This is more or less similar to the version-control feature in Git, except, it is manual and local.
The transfer rate is as high as 16 MBPS. Also, it appends a local machine's timestamp to the file/folder name in order to avoid overwriting and keeping a track.

The _Prime Intention_ is to develop a code to reduce my manual work of opening a new file and copying all the existing content onto it every time before starting reconstruction or performing the trials for enhancements. The [executable](https://github.com/Bhargav43/BackupFiles/blob/master/BackupFiles.exe) works perfectly to my daily usage.

## Base System's Configurations :wrench:
**Sno.** | **Name** | **Version/Config.**
-------: | :------: | :------------------
1 | Operating System | Windows 10 x64 bit
2 | Python | Version 3.7.0 x64 bit
3 | PyInstaller | Version 3.6
4 | IDE | Pyzo 4.10.2 x64 bit

_Recommendation: Try using [`executable`](https://github.com/Bhargav43/BackupFiles/blob/master/BackupFiles.exe) directly as it doesn't require Python and other dependencies to be present in your Windows PC. Executable is mostly made stand-alone._ 

## Imported Modules :package:
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


### Added Scripts :page_facing_up:
#### [TraceFuncCalls](https://github.com/Bhargav43/BackupFiles/blob/master/TraceFuncCalls.py) :mag:
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

#### [ClearScreen](https://github.com/Bhargav43/BackupFiles/blob/master/ClearScreen.py) :scissors:
_Compared with the remaining, this is a simple 2 line script used for clearing-up the console screen. Not heavy, but handy to import rather than checking either types, everytime. `ClearScreen` is used in `BackupFiles1.1.0` to clear the screen just before displaying summery of the execution. As follows:_
```python
def cls():
    #Type 1
    clear = lambda: os.system('cls')
    clear()

    #Type 2
    os.system('cls')
```


## BackupFiles 1.1.0.py :computer:

```python
import os
import time
import shutil
import functools
import re
import sys
import TraceFuncCalls as trc
import ClearScreen

'''
#Checking a Specific Function is Being Called.
sys.setprofile(trc.tracefunc)
trc.keyword = 'copyfile, copytree, memoryview'
'''

def gen_call_counter(func):
    def helper(*args, **kwargs):
        helper.calls += 1
        printable = format_time(helper.calls)
        sys.stdout.write('\r'+ ' '*50)
        sys.stdout.write('\rGeneral Backup Time Count: '+printable)
        return func(*args, **kwargs)

    helper.calls = 0
    helper.__name__ = func.__name__
    return helper

@gen_call_counter
def gen_callback(val):
    pass


def st_call_counter(func):
    def helper2(*args, **kwargs):
        helper2.calls += 1
        printable = format_time(helper2.calls)
        sys.stdout.write('\r'+ ' '*50)
        sys.stdout.write('\rStandard Backup Time Count: '+printable)
        return func(*args, **kwargs)

    helper2.calls = 0
    helper2.__name__ = func.__name__
    return helper2

@st_call_counter
def st_callback(val):
    pass

def _copyfileobj_patched(fsrc, fdst, length=16 * 1024 * 1024):
    """Patches shutil method to improve copy speed to 16 MBPS"""
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        copied += len(buf)

        if bool(re.search('_STANDARD_BACKUP', str(fdst.name))):
            st_callback(copied)
        else:
            gen_callback(copied)


shutil.copyfileobj = _copyfileobj_patched


class Backup:
    def __init__(self, path):
        if path.endswith('\\\\'):
            self.fullpath = path[:-2]
        elif path.endswith('\\'):
            self.fullpath = path[:-1]
        else:
            self.fullpath = path
        self.path, self.leaf = os.path.split(self.fullpath)

        self.standard = f'C:\\Users\\{os.getlogin()}\\Desktop\\Standard Backups'

    def __repr__(self):
        return {'fullpath':self.fullpath, 'path':self.path, 'file': self.leaf}

    def __str__(self):
        return ('fullpath = '+self.fullpath+'\npath = '+self.path+'\nfile or folder = '+self.leaf)

    def timestamp(self, today):
        newname = dict()
        i = 1
        while True:
            if os.path.isfile(self.fullpath):
                newname['Gen'] = os.path.splitext(self.leaf)[0] + '_' + today + '_BACKUP_' + str(i) + os.path.splitext(self.leaf)[1]
                newname['St'] = os.path.splitext(self.leaf)[0] + '_' + today + '_STANDARD_BACKUP_' + str(i) + os.path.splitext(self.leaf)[1]
            elif os.path.isdir(self.fullpath):
                newname['Gen'] = self.leaf + ' ' + today + '_BACKUP' + str(i)
                newname['St'] = self.leaf + ' ' + today + '_STANDARD_BACKUP' + str(i)
            if not os.path.exists(os.path.join(self.path, newname['Gen'])):
                break
            i+=1

        if os.path.exists(os.path.join(self.standard, newname['St'])):
            if os.path.isdir(os.path.join(self.standard, newname['St'])):
                shutil.rmtree(os.path.join(self.standard, newname['St']))
            elif os.path.isfile(os.path.join(self.standard, newname['St'])):
                os.remove(os.path.join(self.standard, newname['St']))
        return newname

    def backup(self, general = False, standard = False):
        output = []
        today = time.strftime('%d%b%y%H%M').upper()
        newFilename = self.timestamp(today)
        #print(newFilename)
        if os.path.isfile(self.fullpath):
            if general:
                print('\n')
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Backup Started-- (Please Wait)')
                time.sleep(2)
                shutil.copyfile(os.path.join(self.path, self.leaf), os.path.join(self.path, newFilename['Gen']))
                output.append(f'Backup File:\t{self.path}\\{newFilename["Gen"]}')
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Backup Done--(Please Wait)')
                time.sleep(2)
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'Backup Successful!!!')

            if standard:
                if not os.path.exists(self.standard):
                    os.mkdir(self.standard)
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Standard Backup Started--(Please Wait)')
                time.sleep(2)
                shutil.copyfile(os.path.join(self.path, self.leaf), os.path.join(self.standard, newFilename['St']))
                output.append(f'Backup File:\t{self.standard}\\{newFilename["St"]}')
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Standard Backup Done--(Please Wait)')
                time.sleep(2)
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'Backup Successful!!!')

        elif os.path.isdir(self.fullpath):
            if general:
                print('\n')
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Backup Started--(Please Wait)')
                time.sleep(2)
                shutil.copytree(os.path.join(self.path, self.leaf), os.path.join(self.path, newFilename['Gen']))
                output.append(f'Backup File:\t{self.path}\\{newFilename["Gen"]}')
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Backup Done--(Please Wait)')
                time.sleep(2)
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'Backup Successful!!!')

            if standard:
                if not os.path.exists(self.standard):
                    os.mkdir(self.standard)
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Standard Backup Started--(Please Wait)')
                time.sleep(2)
                shutil.copytree(os.path.join(self.path, self.leaf), os.path.join(self.standard, newFilename['St']))
                output.append(f'Backup File:\t{self.standard}\\{newFilename["St"]}')
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'--Standard Backup Done--(Please Wait)')
                time.sleep(2)
                sys.stdout.write('\r'+ ' '*50)
                sys.stdout.write('\r'+'Backup Successful!!!')

        ClearScreen.cls()
        print("Final Report:\n")
        print(f'\nFile(s) has been backed-up successfully with a high-speed of 16 MBPS!\n\nPlease find the backup(s) at following location(s),\n\nBackup:\t\t\t{os.path.join(self.path, newFilename["Gen"])}')
        if len(newFilename) == 2:
            print(f'Standard Backup:\t{os.path.join(self.path, newFilename["St"])}')

        return output

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'Kilo', 2: 'Mega', 3: 'Giga', 4: 'Tera'}
    while size > power:
        size /= power
        n += 1
    return f'{size:.2f} {power_labels[n]}bytes'

def format_time(seconds):
    mins, hours, n = 0, 0, 0
    units = {0 : 'Seconds', 1 : 'Minutes', 2 : 'Hours'}
    while seconds >= 60:
        seconds -= 60
        mins += 1
        n = 1
    while mins >= 60:
        mins -= 60
        hours += 1
        n = 2
    if n == 2:
        return f'{hours}:{mins:02d}:{seconds:02d} {units[n]}'
    elif n == 1:
        return f'{mins:2d}:{seconds:02d} {units[n]}'
    else:
        return f'{seconds:.2f} {units[n]}'


def LOF(path):
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    return listOfFiles

def Analyze(path, Standard):
    flags = {'Gen_W': False, 'Gen_C': False, 'St_W': False, 'St_C': False}
    local_drive = 'C:'
    nonlocal_drive = path[:2]
    ctotal, cused, cfree = shutil.disk_usage(local_drive)
    xtotal, xused, xfree = shutil.disk_usage(nonlocal_drive)
    leaf_size = 0
    if os.path.isdir(path):
        leaf_size = functools.reduce(lambda x, y : x + y, [os.stat(os.path.join(path, file)).st_size for file in LOF(path)])
        print('\nTotal Disk Occupied by Directory = ', format_bytes(leaf_size))
    else:
        leaf_size = os.stat(path).st_size
        print('\nTotal Disk Occupied by File = ', format_bytes(leaf_size))


    if local_drive == nonlocal_drive:
        if Standard:
            if cfree <= 2*leaf_size:
                flags['Gen_C'], flags['St_C'] = True, True
            elif int((ctotal - cused - 2*leaf_size)/ctotal) < 10:
                flags['Gen_W'], flags['St_W'] = True, True
        else:
            if xfree <= leaf_size:
                flags['Gen_C'] = True
            elif int((xtotal - xused - leaf_size)/xtotal) < 10:
                flags['Gen_W'] = True

    else:
        if xfree <= leaf_size:
            flags['Gen_C'] = True
        elif int((xtotal - xused - leaf_size)/xtotal) < 10:
            flags['Gen_W'] = True

        if Standard:
            if cfree <= leaf_size:
                flags['St_C'] = True
            elif int((ctotal - cused - leaf_size)/ctotal) < 10:
                flags['St_W'] = True

    print(f'Estimated ETA on Transfer =\t{format_time(int(leaf_size / (16*1024*1024))+10)} (Approx.)')

    return leaf_size, flags

def Warn(sf, path, st, obj):
    gen =True
    if path.endswith('\\'):
        path = path[:len(path)-1]

    warnings = {'Gen_C':f'\nCRITICAL: Disk Space is Terribly Low or Will Be Low After Taking the Backup of File/Folder \'{os.path.split(path)[1]}\' of Size {format_bytes(sf[0])}, at The Same Directory {os.path.split(path)[0]}. Process Aborted!!!',
    'St_C':f'\nCRITICAL: Disk Space is Terribly Low or Will Be Low After Taking the Standard Backup of File/Folder \'{os.path.split(path)[1]}\' of Size {format_bytes(sf[0])}, at The Standard Directory C:\\Users\\{os.getlogin()}\\Desktop\\Standard Backups. Process Aborted!!!',
    'Gen_W':f'\nWARNING: Disk Space is 90% Full or Will Be, After Taking the Backup of File/Folder \'{os.path.split(path)[1]}\' of Size {format_bytes(sf[0])}, at The Same Directory {os.path.split(path)[0]}. Yet, We Can Proceed With This Process!!!',
    'St_W':f'\nWARNING: Disk Space is 90% Full or Will Be, After Taking the Standard Backup of File/Folder \'{os.path.split(path)[1]}\' of Size {format_bytes(sf[0])}, at The Standard Directory C:\\Users\\{os.getlogin()}\\Desktop\\Standard Backups. Yet, We Can Proceed With This Process!!!'}

    if sf[1]['Gen_C']:
        if path[0] in ('C', 'c'):
            if st:
                print(warnings['Gen_C'], '\n', warnings['St_C'])
                gen, st = False, False
            else:
                print(warnings['Gen_C'])
                gen = False
        else:
            print(warnings['Gen_C'])
            gen = False
            if sf[1]['St_C']:
                print(warnings['St_C'])
                st = False

    elif sf[1]['Gen_W']:
        if path[0] in ('C', 'c'):
            if st:
                print(warnings['Gen_W'], '\n', warnings['St_W'])
            else:
                print(warnings['Gen_W'])
        else:
            print(warnings['Gen_W'])
            if sf[1]['St_W']:
                print(warnings['St_W'])

    if (not sf[1]['Gen_C']) and sf[1]['St_C']:
        print(warnings['St_C'])
        gen, st = True, False
    elif (not sf[1]['St_W']) and sf[1]['St_W']:
        print(warnings['St_W'])

    obj.backup(gen, st)


def main():
    st, ba = True, True
    print('\n','\\'*30, '/'*30, '\n', '----------|   BackupFiles 1.1.0   |----------'.center(60),'\n', '/'*30, '\\'*30, '\n')

    while True:
        path = str(input('Please enter full path (Path + File/Folder Name) to backup:\n'))
        if os.path.exists(path):
            break
        else:
            print('Invaild Path. Please re-enter.')

    #Backup of Self
    #path = os.path.join(os.getcwd(), __file__)
    print('\nBackups will be as follows,\n\nGeneral/Normal Backup: Will be at the location of original file with a timestamp appended to the original filename.\nStandard Backup: It is secondary at standard location (Desktop\Standard Backups) which is optional.')
    while True:
        Standard = str(input('\nWant a standard backup?[Y/N]\t')).upper()
        if Standard in ('Y', 'N'):
            break
        print('Invalid Input. Retry.')
    Standard = True if Standard== 'Y' else False

    BackupObj = Backup(path)

    Warn(Analyze(path, Standard), path, Standard, BackupObj)

    input('\nEnter any key to exit the console.')

if __name__ == '__main__':
    main()
```

Haven't added any comments for understanding. You can go thru, and let me know on mails in case if this is useful for you and require clarification/assistance.


#### Some Terms Used :pencil:
###### Warnings :warning:
1. Critical Condition
    - Triggers when the disk space already at max, or will be, after copying the file.
1. Warning Condtion
    - Triggers when the disk space already at 90% occupancy, or will be, after copying the file.

###### Types of Backups :v:
1. [General] Backup
    - The backup at the location of original file, with a timestamp for avoiding overwriting.
2. Standard Backup
    - The backup at a standard location, say Desktop\Standard Directory, for secondary backup or track of backups.

### Sample Output :bar_chart:
**Screen 1**
```

 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ //////////////////////////////
        ----------|   BackupFiles 1.1.0   |----------
 ////////////////////////////// \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Please enter full path (Path + File/Folder Name) to backup:
H:\Projects\Python Related Stuff\Projects with Git\BackupFiles 1.1.0

Backups will be as follows,

General/Normal Backup: Will be at the location of original file with a timestamp appended to the original filename.
Standard Backup: It is secondary at standard location (Desktop\Standard Backups) which is optional.

Want a standard backup?[Y/N]    y

Total Disk Occupied by Directory =  14.70 Megabytes
Estimated ETA on Transfer =     10.00 Seconds (Approx.)

WARNING: Disk Space is 90% Full or Will Be, After Taking the Backup of File/Folder 'BackupFiles 1.1.0' of Size 14.70 Megabytes, at The Same Directory H:\Projects\Python Related Stuff\Projects with Git. Yet, We Can Proceed With This Process!!!

WARNING: Disk Space is 90% Full or Will Be, After Taking the Standard Backup of File/Folder 'BackupFiles 1.1.0' of Size 14.70 Megabytes, at The Standard Directory C:\Users\BHARGAV-PC\Desktop\Standard Backups. Yet, We Can Proceed With This Process!!!


General Backup Time Count: 20.00 Seconds
```

**Screen 2**
```
Final Report:


File(s) has been backed-up successfully with a high-speed of 16 MBPS!

Please find the backup(s) at following location(s),

Backup:                 H:\Projects\Python Related Stuff\Projects with Git\BackupFiles 1.1.0 04APR200119_BACKUP1
Standard Backup:        H:\Projects\Python Related Stuff\Projects with Git\BackupFiles 1.1.0 04APR200119_STANDARD_BACKUP1

Enter any key to exit the console.
```

### [Executable File](https://github.com/Bhargav43/BackupFiles/blob/master/BackupFiles.exe) :floppy_disk:
_Executable (also called freezing) for using in change of confguration of base system or in absence of python. The file be used for distribution with ease and without dependencies. Following is the commands I used for the same. [Click here](https://github.com/Bhargav43/BackupFiles/blob/master/Freezing%20Logs.txt) for logs related to it._

#### Creating Specifications file :page_facing_up:

```
H:\Projects\Python Related Stuff\Pyzo Projects\BackupFiles 1.1.0>pyi-makespec --onefile --hidden-import=os --hidden-import=time --hidden-import=shutil --hidden-import=functools --hidden-import=re --hidden-import=sys --hidden-import=TraceFuncCalls --hidden-import=ClearScreen  --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\BackupFiles 1.1.0" BackupFiles.py
```

This has created [BacupFiles.spec](https://github.com/Bhargav43/BackupFiles/blob/master/BackupFiles.spec) as follows,
```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['BackupFiles.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\BackupFiles 1.1.0'],
             binaries=[],
             datas=[],
             hiddenimports=['os', 'time', 'shutil', 'functools', 're', 'sys', 'TraceFuncCalls', 'ClearScreen'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BackupFiles',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
```

#### Creating Executable :arrow_forward:

PyPI `Pyinstaller 3.6` was used for creating the executable in PIP environment. Command as follows,
```
H:\Projects\Python Related Stuff\Pyzo Projects\BackupFiles 1.1.0>pyinstaller --onefile --hidden-import=os --hidden-import=time --hidden-import=shutil --hidden-import=functools --hidden-import=re --hidden-import=sys --hidden-import=TraceFuncCalls --hidden-import=ClearScreen  --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\BackupFiles 1.1.0" BackupFiles.py
```

### Finally, the Working Model :metal:

Click for accessing [BackupFile 1.1.0.exe](https://github.com/Bhargav43/BackupFiles/blob/master/BackupFiles.exe)

# Farewell! :tada::tada:
