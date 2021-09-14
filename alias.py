import os

from utils import copy_file
from utils import sta_ifconfig, ap_ifconfig


def ls():
    print(os.listdir())


def cat(f_name):
    try:
        fd = open(f_name, 'r')
        data = fd.read()
        line_no = 1

        lines = data.split('\n')
        max_space = len(str(len(lines))) + 2
        for line in lines:
            print(str(line_no) + ' ' * (max_space - len(str(line_no))) + line)
            line_no += 1
    except:
        print('Open file failed')


def rm(f_name):
    try:
        os.remove(f_name)
    except:
        print('Remove ' + f_name + ' failed')


def cp(raw_path, new_path):
    copy_file(raw_path, new_path)

def mv(raw_path, new_path):
    try:
        os.rename(raw_path, new_path)
        print('Done.')
    except:
        print('Failed.')


def ifconfig():
    sta_ifconfig()


def apconfig():
    ap_ifconfig()
