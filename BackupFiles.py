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