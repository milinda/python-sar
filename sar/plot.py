#!/usr/bin/env python
'''
:mod:`sar.plot` is a module containing class for plotting processed SAR output files.
'''

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.ticker as ticker
import matplotlib as mpl


class Plot(object):
    def __init__(self, sar_info):
        if not isinstance(sar_info, dict):
            raise 'Invalid sar info'
        self.sar_info = sar_info

    def plot(self, out_pdf, config={}):
        mpl.rc('font',family='Source Code Pro')
        fig = plt.figure()
        fig.set_figheight(21)
        plt.clf()
        plt.subplots_adjust(wspace=1,hspace=1)

        cpu_usage = self.sar_info['cpu']

        # Get sorted time points and x axis
        time_points = cpu_usage.keys()
        time_points.sort()

        print 'Start:', time_points[0]
        print 'End:', time_points[len(time_points)- 1]

        x = range(len(time_points))
        if len(time_points) > 1000:
            stepsize = 200
        elif len(time_points) > 200:
            stepsize = 50
        else:
            stepsize = 10

        xticks = np.arange(0, len(time_points), stepsize)
        xticklabels = [time_points[i] for i in xticks]
        
        ax = plt.subplot(711)
        usr = [cpu_usage[t]['all']['usr'] for t in time_points]
        sys = [cpu_usage[t]['all']['sys'] for t in time_points]
        # plt.plot(time_points, usr, 'm^', time_points, sys, 'm-')
        
        plt.xticks(xticks, xticklabels, rotation='vertical')
        plt.plot(x, usr, label='usr')
        plt.plot(x, sys, label='sys')
        plt.xlabel('time')
        plt.ylabel('%')
        plt.title('CPU Usage')
        lg = plt.legend(frameon=False)
        lg.get_frame().set_alpha(0.5)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)

        ax = plt.subplot(712)
        paging = self.sar_info['paging']
        fault = [paging[t]['fault'] for t in time_points]
        majfault = [paging[t]['majflt'] for t in time_points]
        pageins = [paging[t]['pgpgin'] for t in time_points]
        pageouts = [paging[t]['pgpgout'] for t in time_points]
        plt.xticks(xticks, xticklabels, rotation='vertical')
        plt.plot(x, fault, label='fault')
        plt.plot(x, majfault, label='majfault')
        plt.xlabel('time')
        plt.ylabel('faults/s')
        plt.title('Page Faults')
        lg = plt.legend(frameon=False)
        lg.get_frame().set_alpha(0.5)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)

        ax = plt.subplot(713)
        plt.xticks(xticks, xticklabels, rotation='vertical')
        plt.plot(x, pageins, label='page-ins')
        plt.plot(x, pageouts, label='page-outs')
        plt.xlabel('time')
        plt.ylabel('KB/s')
        plt.title('Page Ins and Outs')
        lg = plt.legend(frameon=False)
        lg.get_frame().set_alpha(0.5)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)


        ax = plt.subplot(714)
        mem = self.sar_info['mem']
        memusage = [mem[t]['memusedpercent'] for t in time_points]
        kbmemused = [(mem[t]['memused'] - (mem[t]['membuffer'] + mem[t]['memcache']))/ 1024 for t in time_points]
        kbmembuffer = [mem[t]['membuffer']/ 1024 for t in time_points]
        kbmemcached = [mem[t]['memcache']/ 1024 for t in time_points]
        plt.xticks(xticks, xticklabels, rotation='vertical')
        plt.plot(x, memusage, label='% memused')
        plt.xlabel('time')
        plt.ylabel('% memused')
        plt.title('Percentage of Mmemory Used')
        lg = plt.legend(frameon=False)
        lg.get_frame().set_alpha(0.5)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)

        ax = plt.subplot(715)
        plt.xticks(xticks, xticklabels, rotation='vertical')
        plt.stackplot(x, kbmembuffer, kbmemcached, kbmemused)
        plt.xlabel('time')
        plt.ylabel('Memory Usage (MB)')
        plt.title('Memory Usage')
        #lg = plt.legend()
        #lg.get_frame().set_alpha(0.5)

        ax = plt.subplot(716)
        net = self.sar_info['net']
        netusage_rx = {}
        netusage_tx = {}
        for t in time_points:
            p = net[t]
            for iface in p.keys():
                if iface not in netusage_rx:
                    netusage_rx[iface] = [p[iface]['rxkB']/1024]
                else:
                    netusage_rx[iface].append(p[iface]['rxkB']/1024)

                if iface not in netusage_tx:
                    netusage_tx[iface] = [p[iface]['txkB']/1024]
                else:
                    netusage_tx[iface].append(p[iface]['txkB']/1024)

        plt.xticks(xticks, xticklabels, rotation='vertical')
        
        for iface in netusage_rx.keys():
            plt.plot(x, netusage_rx[iface], label='{}-rx'.format(iface))

        for iface in netusage_tx.keys():
            plt.plot(x, netusage_tx[iface], label='{}-tx'.format(iface))

        plt.xlabel('time')
        plt.ylabel('Network Usage (MB)')
        plt.title('Network Usage')
        lg = plt.legend(loc=1,
           ncol=len(netusage_tx.keys()),frameon=False)
        lg.get_frame().set_alpha(0)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)

        ax = plt.subplot(717)
        io = self.sar_info['io']
        bread = [io[t]['bread'] for t in time_points]
        bwrite = [io[t]['bwrite'] for t in time_points]
        plt.xticks(xticks, xticklabels, rotation='vertical')
        plt.plot(x, bread, label='reads')
        plt.plot(x, bwrite, label='writes')
        plt.xlabel('time')
        plt.ylabel('blocks')
        plt.title('Disk IO')
        lg = plt.legend(frameon=False)
        lg.get_frame().set_alpha(0.5)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)

        fig.tight_layout()
        pp = PdfPages(out_pdf)
        pp.savefig()
        pp.close()
