#!/usr/bin/env python
'''
:mod:`sar.plot` is a module containing class for plotting processed SAR output files.
'''

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.ticker as ticker


class Plot(object):
    def __init__(self, sar_info):
        if not isinstance(sar_info, dict):
            raise 'Invalid sar info'
        self.sar_info = sar_info

    def plot(self, out_pdf, config={}):
        fig = plt.figure()
        fig.set_figheight(10)
        plt.clf()
        plt.subplots_adjust(wspace=1,hspace=1)
        ax = plt.subplot(311)
        cpu_usage = self.sar_info['cpu']
        time_points = cpu_usage.keys()

        usr = [cpu_usage[t]['all']['usr'] for t in time_points]
        sys = [cpu_usage[t]['all']['sys'] for t in time_points]
        # plt.plot(time_points, usr, 'm^', time_points, sys, 'm-')
        if len(time_points) > 1000:
            stepsize = 200
        elif len(time_points) > 200:
            stepsize = 50
        else:
            stepsize = 5
        x = range(len(time_points))
        plt.xticks(x, time_points, rotation='vertical')
        plt.plot(x, usr, label='usr')
        plt.plot(x, sys, label='sys')
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, stepsize))
        plt.xlabel('time')
        plt.ylabel('%')
        plt.title('CPU Usage')
        lg = plt.legend()
        lg.get_frame().set_alpha(0.5)

        ax = plt.subplot(312)
        paging = self.sar_info['paging']
        time_points = paging.keys()
        fault = [paging[t]['fault'] for t in time_points]
        majfault = [paging[t]['majflt'] for t in time_points]
        pageins = [paging[t]['pgpgin'] for t in time_points]
        pageouts = [paging[t]['pgpgout'] for t in time_points]
        # plt.plot(time_points, fault, 'r^', time_points, majfault, 'r-')
        if len(time_points) > 1000:
            stepsize = 200
        elif len(time_points) > 200:
            stepsize = 50
        else:
            stepsize = 5
        x = range(len(time_points))
        plt.xticks(x, time_points, rotation='vertical')
        plt.plot(x, fault, label='fault')
        plt.plot(x, majfault, label='majfault')
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, stepsize))
        plt.xlabel('time')
        plt.ylabel('faults/s')
        plt.title('Page Faults')
        lg = plt.legend()
        lg.get_frame().set_alpha(0.5)

        ax = plt.subplot(313)
        plt.xticks(x, time_points, rotation='vertical')
        plt.plot(x, pageins, label='page-ins')
        plt.plot(x, pageouts, label='page-outs')
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, stepsize))
        plt.xlabel('time')
        plt.ylabel('KB/s')
        plt.title('Page Ins and Outs')
        lg = plt.legend()
        lg.get_frame().set_alpha(0.5)

        fig.tight_layout()
        pp = PdfPages(out_pdf)
        pp.savefig()
        pp.close()
