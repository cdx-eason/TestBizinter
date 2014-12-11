from Config import ConfigBinzinter

import subprocess
import time
import random


class BizinterClass():
    def __init__(self):
        self.mastertraceon = list()
        self.traceon = list()
        self.xrext = list()
        self.probetype = self.getlistfromconfig('probetype')
        self.mktnbr = self.getlistfromconfig('market')
        self.ctrynbr = self.getlistfromconfig('country')
        self.regionnbr = self.getlistfromconfig('region')
        self.statenbr = self.getlistfromconfig('state')
        self.asnnbr = self.getlistfromconfig('asn')

        # print self.probetype
        self.totalhits = int(ConfigBinzinter.getconfig('total_hits'))
        self.batches = int(ConfigBinzinter.getconfig('batches'))
        self.threads = int(ConfigBinzinter.getconfig('threads'))
        self.interval = int(ConfigBinzinter.getconfig('interval_sec'))

    # def getprobetype(self):
    #     probetype = ConfigBinzinter.getconfig('probetype').split(",")
    #     return probetype

    def getlistfromconfig(self, param):
        list = ConfigBinzinter.getconfig(param).split(",")
        return list

    def hitbizinter(self):
        print 'batch 1'
        self.hitudp()

        if self.batches > 1:
            for i in range(1, self.batches):
                time.sleep(self.interval)
                print '\nbatch %s' % (str(i + 1))
                self.hitudp()

    def hitudp(self):
        self.createdata()
        cmd = "cat zinterdata | sudo nc -w 30 -U /var/run/cdx-newzinter/interconnect.skt"
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() is not None:
                break

    def createdata(self):
        self.traceon = list()
        self.xrext = list()

        for i in range(0, self.totalhits):
            mkt_nbr = random.choice(self.mktnbr)
            ctry_nbr = random.choice(self.ctrynbr)
            region_nbr = random.choice(self.regionnbr)
            state_nbr = random.choice(self.statenbr)
            asn_nbr = random.choice(self.asnnbr)
            zone_nbr = 1
            cust_nbr = 1
            p_type = 0
            # p_type = random.choice(self.probetype)
            p_zone = 1
            p_cust = 1
            p_prov = 1
            cnt_nbr = 1
            tot_nbr = 1

            trace_on = 'trace.on %s %s %s %s %s %s' % (p_prov, p_type, mkt_nbr, ctry_nbr, region_nbr, asn_nbr)
            xr_ext = 'xr_ext %s %s %s %s %s %s %s %s %s %s %s %s %s' % (
            mkt_nbr, ctry_nbr, region_nbr, state_nbr, asn_nbr, zone_nbr, cust_nbr, p_type, p_zone, p_cust, p_prov,
            cnt_nbr, tot_nbr)

            if trace_on not in self.mastertraceon:
                if trace_on not in self.traceon:
                    self.mastertraceon.append(trace_on)
                    self.traceon.append(trace_on)
            self.xrext.append(xr_ext)
        self.createdatafile()

    def createdatafile(self):
        open('zinterdata', 'w').close()
        with open('zinterdata', 'a') as zdata:
            for item in self.traceon:
                # print item
                zdata.write(item + '\n')
            for item in self.xrext:
                print item
                zdata.write(item + '\n')