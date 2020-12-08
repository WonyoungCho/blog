#! /usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def plot_freq(x,y,y1,title):
    fig,ax=plt.subplots(1,1)

    psize=12
    fsize=10
    tsize=8
    lw=0.3

    #fig.suptitle(data)
    ax.stem(x,y,linefmt='dodgerblue', markerfmt='.',use_line_collection=True, bottom=0)#,label='maf<0.01 ~ '+str(round(y1,2)))
    ax.set_xlim(-0.01,1.01)
    ax.set_xticks(np.arange(0,1.1,0.1))

    if y1>0.8:
        ax.set_ylim(-0.001,0.051)
        ax.set_yticks(np.arange(0,0.051,0.01))
    else:
        ax.set_ylim(-0.01,0.36)
        ax.set_yticks(np.arange(0,0.36,0.05))

    ax.tick_params(labelsize=tsize)
    ax.set_xlabel('Allele Frequency',fontsize=fsize)
    ax.set_ylabel('Ratio',fontsize=fsize)

    #ax.legend(fontsize=fsize,loc=2)

    ax.grid(color='gray',alpha=0.3,linewidth=0.3)
    plt.title(title)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig(title+'_frq',dpi=300)


def main(fname):
    title=fname.split('.')[0]
    
    df=pd.read_csv(fname,sep='\s+')

    df['ratio']=df['OBS_CT']/df['OBS_CT'].sum(axis=0)

    df1=df.drop(index=0)

    x=df1['#BIN_START']
    y=df1['ratio']
    y1=df.loc[0,'ratio']

    plot_freq(x,y,y1,title)

    
if __name__=='__main__':
    fname=sys.argv[1]

    main(fname)
