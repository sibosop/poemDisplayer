#!/usr/bin/env python
import os
import sys
os.environ['DISPLAY']=":0.0"
os.chdir(os.path.dirname(sys.argv[0]))
pname = sys.argv[0]
home = os.environ['HOME']
sys.path.append("sibcommon")
defaultSpecPath = "%s/%s"%("speclib","raspmus.json")
import datetime
import time
import argparse
import json
import subprocess
import traceback
import signal
import pygame
import random
import glob

from asoundConfig import setVolume
from debug import Debug
from specs import Specs
from shutdown import Shutdown
from watchdog import Watchdog
from display import Display
from singleton import Singleton


class Poem(object):
  __metaclass__ = Singleton
  def __init__(self):
    self.name = "Poem"
    random.seed()
    poemDir = 'POEMDATA'
    self.minLineTime = Specs().s['minLineTime']
    self.candidates = []
    self.candidates = glob.glob(poemDir+"/*/*/*.txt")

  def show(self):
    f = random.choice(self.candidates)
    dirPath = os.path.dirname(f)
    Debug().p("%s choice: %s path %s"%(self.name,f,dirPath))
    poemFile = open(f,"r")
    jsonStr = poemFile.read()
    poem = json.loads(jsonStr)
    for e in poem:
      Debug().p("text: %s"%e['text'])
      if  e['text'] == '+++++':
        time.sleep(2)
      else:
        t = random.random() + self.minLineTime 
        Display().text(e['text'])
        Debug().p("next line in: %f"%(t))
        time.sleep(t)


  
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

def service_shutdown(signum, frame):
    Debug().p('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == '__main__':
  try:
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    print("%s at %s"%(pname,datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.init()
    parser = argparse.ArgumentParser() 
    parser.add_argument('-c','--config',nargs=1,type=str,default=[defaultSpecPath],help='specify different config file')
    args = parser.parse_args()
    Debug(['specs',"__main__"])
    Debug().p("config path %s"%args.config[0])
    specs = Specs(args.config[0]).s
    Debug().enable(specs['debug'])
    while True:
      Poem().show()
      time.sleep(Specs().s['nextTime'])

  except ServiceExit:
    print("%s got signal"%pname)
    gardenExit = 5
  except Exception as e:
    print("%s"%e)
    traceback.print_exc()
    gardenExit = 5

  print("%s exiting"%pname)
  exit(gardenExit)

