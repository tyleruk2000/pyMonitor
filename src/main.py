'''
Created on 12 May 2014

Copyright (c) 2014, Tyler Allen.
License: MIT (see http://opensource.org/licenses/MIT)
'''
import psutil
import os
import pyMonitor
import datetime
import logging

thread = pyMonitor.Monitor()

from bottle import route, run, static_file,request
@route('/')
def hello():
    logging.info(' ' + str(datetime.datetime.now()) + ' Root Loaded By ' + request.remote_addr)
    return static_file("monitor.html",root='./')

@route('/img/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root=thread.pngLocation, mimetype='image/png')

if __name__ == '__main__':
    logging.basicConfig(filename=thread.logLocation + 'pyMonitor.log',level=logging.INFO)

    logging.info(' ' + str(datetime.datetime.now()) + ' Starting Thread')    
    thread.start()
    
    logging.info(' ' + str(datetime.datetime.now()) + ' Starting Bottle')
    run(host=thread.host, port=thread.portNo, debug=True)
    
