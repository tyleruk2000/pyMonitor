'''
Created on 12 May 2014

@author: tyler
'''

import threading
import time
import psutil
import os

rrdCPULocation = "./pyMonitorCPU.rrd"
rrdMEMLocation = "./pyMonitorMEM.rrd"
rrdDISKLocation = "./pyMonitorDISK.rrd"
rrdNETLocation = "./pyMonitorNET.rrd"

cpuIMG = "./cpu_"
loadIMG = "./load_"
memIMG = "./mem_"
diskIMG = "./disk_"
netIMG = "./net_"

#graphHeigh = str(100)
#graphWidth = str(400)


class Monitor(threading.Thread):   
    
    '''
    #######################################################
                        Setup RRD's
    #######################################################
    '''  
    def setupRRD(self):
        if not (os.path.isfile(rrdCPULocation)):
            print "Creating CPU RRD file"
            os.system("rrdtool create " + rrdCPULocation + " \
            --step 60 \
            DS:cpu:GAUGE:120:0:100 \
            DS:load:GAUGE:120:0:U \
            RRA:AVERAGE:0.5:1:10080 \
            RRA:AVERAGE:0.5:5:8765 \
            RRA:AVERAGE:0.5:60:8765")
            #1 min for week
            #5 min for 1 month
            #1 hour for 1 years

        if not (os.path.isfile(rrdMEMLocation)):
            print "Creating MEM RRD file"
            os.system("rrdtool create " + rrdMEMLocation + " \
            --step 60 \
            DS:avaliable:GAUGE:120:U:U \
            DS:total:GAUGE:120:U:U \
            DS:free:GAUGE:120:U:U \
            DS:used:GAUGE:120:U:U \
            DS:active:GAUGE:120:U:U \
            DS:inactive:GAUGE:120:U:U \
            DS:buffers:GAUGE:120:U:U \
            DS:cached:GAUGE:120:U:U \
            RRA:AVERAGE:0.5:1:10080 \
            RRA:AVERAGE:0.5:5:8765 \
	    RRA:AVERAGE:0.5:60:8765")

        if not (os.path.isfile(rrdDISKLocation)):
            print "Creating MEM RRD file"
            os.system("rrdtool create " + rrdDISKLocation + " \
            --step 60 \
            DS:total:GAUGE:120:U:U \
            DS:used:GAUGE:120:U:U \
            DS:free:GAUGE:120:U:U \
            DS:percent:GAUGE:120:0:100 \
            RRA:AVERAGE:0.5:1:10080 \
            RRA:AVERAGE:0.5:5:8765 \
	    RRA:AVERAGE:0.5:60:8765")
        
        if not (os.path.isfile(rrdNETLocation)):
            print "Creating MEM RRD file"
            os.system("rrdtool create " + rrdNETLocation + " \
            --step 60 \
            DS:sent:COUNTER:120:U:U \
            DS:recv:COUNTER:120:U:U \
            RRA:AVERAGE:0.5:1:10080 \
            RRA:AVERAGE:0.5:5:8765 \
	    RRA:AVERAGE:0.5:60:8765")
    
    '''
    #######################################################
                        Update RRD
    #######################################################
    '''  
    def updateRRD(self):
        #---------------CPU---------------
        os.system("rrdtool update " + rrdCPULocation + " N:" + str(psutil.cpu_percent(interval=0.1)) + ":" + str(os.getloadavg()[0]))
        
        #---------------MEM---------------
        mem = psutil.virtual_memory()
        os.system("rrdtool update " + rrdMEMLocation + " N:" + str(float(mem.available)) + ":" + str(float(mem.total)) + ":" + str(float(mem.free)) + ":" + str(float(mem.used)) + ":" + str(float(mem.active)) + ":" + str(float(mem.inactive)) + ":" + str(float(mem.buffers)) + ":" + str(float(mem.cached)))
        
        #---------------DISK---------------
        disk = psutil.disk_usage('/')
        os.system("rrdtool update " + rrdDISKLocation + " N:" + str(disk.total) + ":" + str(disk.used) + ":" + str(disk.free) + ":" + str(disk.percent))

        #---------------NET---------------
        net = psutil.net_io_counters()
        os.system("rrdtool update " + rrdNETLocation + " N:" + str(net.bytes_sent) + ":" + str(net.bytes_recv))
    
    '''
    #######################################################
                        DARW GRAPH
    #######################################################
    '''  
    def drawGraph(self,graphHeigh,graphWidth,postfix,start):
        #---------------CPU---------------
        os.system("rrdtool graph " + cpuIMG + postfix + ".png \
        --title 'CPU %' \
        DEF:cpu=" + rrdCPULocation + ":cpu:AVERAGE \
        AREA:cpu#8FBE00:'CPU %' \
        --start now-" + start + " \
        -w " + graphWidth + " \
        -h " + graphHeigh)
        
        os.system("rrdtool graph " + loadIMG + postfix + ".png \
        --title 'Load AVG' \
        DEF:load=" + rrdCPULocation + ":load:AVERAGE \
        AREA:load#40C0CB:'Load AVG' \
        --start now-" + start + " \
        -w " + graphWidth + " \
        -h " + graphHeigh)
        
        #---------------MEM---------------
        os.system("rrdtool graph " + memIMG + postfix + ".png \
        --title 'Memory Usage' \
        DEF:avaliable=" + rrdMEMLocation + ":avaliable:AVERAGE \
        DEF:total=" + rrdMEMLocation + ":total:AVERAGE \
        DEF:free=" + rrdMEMLocation + ":free:AVERAGE \
        DEF:used=" + rrdMEMLocation + ":used:AVERAGE \
        DEF:active=" + rrdMEMLocation + ":active:AVERAGE \
        DEF:inactive=" + rrdMEMLocation + ":inactive:AVERAGE \
        DEF:buffers=" + rrdMEMLocation + ":buffers:AVERAGE \
        DEF:cached=" + rrdMEMLocation + ":cached:AVERAGE \
        AREA:total#00A8C6:'Total' \
        AREA:used#8FBE00:'Used' \
        AREA:active#AEE239:'Active' \
        AREA:cached#40C0CB:'Cached' \
        --start now-" + start + " \
        -w " + graphWidth + " \
        -h " + graphHeigh)
        
        #---------------DISK---------------
        os.system("rrdtool graph " + diskIMG + postfix + ".png \
        --title 'Disk Usage' \
        DEF:total=" + rrdDISKLocation + ":total:AVERAGE \
        DEF:used=" + rrdDISKLocation + ":used:AVERAGE \
        AREA:total#00A8C6:'Total' \
        AREA:used#AEE239:'used' \
        --lower-limit 0 \
        --start now-" + start + " \
        -w " + graphWidth + " \
        -h " + graphHeigh)
        
        #---------------NET---------------
        os.system("rrdtool graph " + netIMG + postfix + ".png \
        --title 'Network Stats' \
        DEF:sent=" + rrdNETLocation + ":sent:AVERAGE \
        DEF:recv=" + rrdNETLocation + ":recv:AVERAGE \
        LINE:sent#00A8C6:'Sent' \
        LINE:recv#AEE239:'recv' \
        --start now-" + start + " \
        -w " + graphWidth + " \
        -h " + graphHeigh)
    
    
    def __init__(self):
        super(Monitor,self).__init__()
        self.setupRRD()
    
    def run(self):
        #Always draw grap th begining
        self.drawGraph(str(100),str(400),"sml","1d")
        self.drawGraph(str(800),str(1800),"lrg","1d")
        self.drawGraph(str(100),str(400),"30d","30d")
        
        count = 0 #used for 10 min timer
        count1 = 0 #used for 60 min timer
        
        #Begin main loon
        while (True):
            self.updateRRD()
            
            count = count + 1
            count1 = count1 + 1
            if (count > 9):
                #every 5 mins re-draw graph
                self.drawGraph(str(100),str(400),"sml","1d")
                count = 0
            if (count1 > 60):
                #every 60 mins darw large and 1 month graph
                self.drawGraph(str(800),str(1800),"lrg","1d")
                self.drawGraph(str(100),str(400),"30d","30d")
                count1 = 0
                
            time.sleep(30)
