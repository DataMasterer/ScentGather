import datetime
import time
import os.path
import shutil

logfilename='logfile.log'

def log(msg,errmsg=None,dump=None,listelem=None,elemparent=None,pathname=None,depth=None):
    global logfilename
    ts=time.time()
    logstring=[]
    logstring=logstring+[datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')]
    logstring=logstring+[msg,';',errmsg]
    if elemparent is list and listelem in elemparent:
        logstring=logstring+[elemparent.index(listelem)/len(elemparent)]
    else:
        logstring=logstring+[None]
    logstring=logstring+[pathname,depth,dump]
    print logstring
    with open(logfilename,'a') as f:
        f.write('\t'.join(map(str,logstring))+'\n')

def archivelog():
    global logfilename
    ts=time.time()
    if os.path.exists(logfilename):
                os.rename(logfilename,logfilename+'.'+datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S'))
        #shutil.copy(logfilename,logfilename+'.'+datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S'))
    with open(logfilename,'w') as f:
        f.write('')

class ScentTimer(object):
    def __init__(self):
        self.clear()
        self.beginTime=self.now()

    def start(self):
        if not self.running:
            self.startTime=self.now()
            self.running=True

    def stop(self):
        if self.running:
            self.endTime=self.now()
            self.running=False
            self.lastTimeDiff=self.endTime-self.startTime

            if self.countTick==0:
                self.avgTime=self.lastTimeDiff
                self.totalTime=self.lastTimeDiff
            else:
                self.avgTime=(self.avgTime*self.countTick+self.lastTimeDiff)/(self.countTick+1)
                self.totalTime+=self.lastTimeDiff
            self.countTick+=1

    def grandTotalElapsed(self):
        gte=self.now()-self.beginTime
        return self.fInterval(gte)

    def ETA(self,remainingTicks):
        eta=self.now()+self.avgTime*remainingTicks
        return eta.strftime('%c')

    def remainingUntil(self,remainingTicks):
        eta=self.avgTime*remainingTicks
        return self.fInterval(eta)

    def clear(self):
        self.running = False
        self.beginTime = None
        self.startTime = None
        self.endTime = None
        self.lastTimeDiff = None
        self.avgTime = None
        self.totalTime = None
        self.countTick = 0

    @classmethod
    def now(cls):
        return datetime.datetime.now()

    @classmethod
    def fInterval(cls,timedelta):
        days, remainder = divmod(timedelta.total_seconds(), 24*60*60)
        hours, remainder = divmod(remainder, 60*60)
        mins, seconds = divmod(remainder, 60)
        form=str(int(days))+' day'+('s' if days!=1 else '')
        form+=' '+str(int(hours))+' hour'+('s' if hours!=1 else '')
        form+=' '+str(int(mins))+' minute'+('s' if mins!=1 else '')
        form+=' '+str(seconds)+' second'+('s' if seconds!=1 else '')
        return form
