#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
import sys
sys.path.append("..")
from src import domain_control
from src import disk_control
from src import script
import os
import signal
import atexit
"""
usage: start: python server.py start
       stop : python server.py stop
       status: python server.py status
       reboot: python server.py restart

"""

def domainCheck():
    while True:
	#print(1)
        # start domain check
        domain_control.domain_control_refer(num='all')
        # start domain run info check
	#print(2)
        domain_control.domain_control_monitor(num='all')
        # start cluster storage info check
	#print(4)
        domain_control.storageUpdate()
        # start cluster disk info check
	#print(5)
        disk_control.diskUseCheck()
        # start vnc check
	#print(6)
        script.nodeVncPort()
        # start vnc file check
	#print(7)
        script.vncConfig()
        #print(8)
	time.sleep(30)

if __name__ == '__main__':
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    os.chdir("/git_csdn/kvm/src/")
    os.setsid()
    os.umask(022)
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    si = file("/git_csdn/kvm/src/log/server.log",'a+')
    so = file("/git_csdn/kvm/src/log/server.log","a+")
    se = file("/git_csdn/kvm/src/log/error.log","a+",0)
    os.dup2(sys.stdin.fileno(),si.fileno())
    os.dup2(sys.stdout.fileno(),so.fileno())
    os.dup2(sys.stderr.fileno(),se.fileno())
    domainCheck()
