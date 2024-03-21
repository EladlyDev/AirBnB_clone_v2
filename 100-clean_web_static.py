#!/usr/bin/python3
""" deletes out-of-date archives, using the function do_clean """
from os import listdir
from os import remove
from fabric.api import *
env.hosts = ['34.232.68.194', '54.173.210.20']


def do_clean(number=0):
    """ deletes out-of-date archives, using the function do_clean """
    number = 1 if int(number) == 0 else int(number)

    flist = sorted(listdir("versions"))
    for b in range(number):
        flist.pop()
    for a in flist:
        local("rm ./versions/{}".format(a))

    with cd("/data/web_static/releases"):
        tlist = run("ls -tr").split()
        flist = []
        for a in tlist:
            if "test" != a:
                flist.append(a)
        for i in range(number):
            flist.pop()
        for a in flist:
            run("rm -rf ./{}".format(a))
