'''
Created on 12 May 2014

Copyright (c) 2014, Tyler Allen.
License: MIT (see http://opensource.org/licenses/MIT
'''
import psutil
import os
import pyMonitor

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def printStats():
    #---------------CPU---------------
    print "CPU: \t\t" + str(psutil.cpu_percent(interval=0.1)) + "%"
    print "LOAD: \t\t" + str(os.getloadavg()[0])
     
    #---------------MEM---------------
    mem = psutil.virtual_memory()
    print "Avaliable: \t" + str(round(float(mem.available) / 1073741824)) + "GB"
    print "Total: \t\t" + str(round(float(mem.total) / 1073741824)) + "GB"
    print "Free: \t\t" + str(round(float(mem.free) / 1073741824)) + "GB"
    print "Used: \t\t" + str(round(float(mem.used) / 1073741824)) +"GB " +str(mem.percent) + "%"
    
    print "Active: \t" + str(round(float(mem.active) / 1073741824)) +"GB"
    print "Inactive: \t" + str(round(float(mem.inactive) / 1073741824)) +"GB"
    print "Buffers: \t" + str(round(float(mem.buffers) / 1073741824)) +"GB"
    print "Cached: \t" + str(round(float(mem.cached) / 1073741824)) +"GB"

    #---------------DISK---------------
    disk = psutil.disk_usage('/')
    print "Total \t\t" + str(bytes2human(disk.total))
    print "Used \t\t" + str(bytes2human(disk.used))
    print "Free \t\t" + str(bytes2human(disk.free))
    print "Percent \t" +  str(disk.percent) + "%"

    #---------------NET---------------
    net = psutil.net_io_counters()
    print "Sent: \t\t" + str(net.bytes_sent)
    print "Recv: \t\t" + str(net.bytes_recv)

    #---------------APACHE---------------
    #Required apache mod_status is installed and enabled
    #https://pythonhosted.org/pyserverstatus/

if __name__ == '__main__':
    thread = pyMonitor.Monitor()
    thread.start()
    
