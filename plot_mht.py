#! /usr/bin/env python3

import formatData as FD

import matplotlib.pyplot as plt
import sys
import os
import subprocess


def GenerateManhattan(data_object, title = None, significance = 6, colors = ['#E24E42', '#008F95'], refSNP = False):
    f=open(title+'_SNPs.tmp','w')
    f.write('#CHROM\tPOS\tID\tOR\tZ_STAT\tP\n')
    
    data = data_object[0]
    data_grouped = data_object[1]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x_labels = []
    x_labels_pos = []
    for num, (name, group) in enumerate(data_grouped):
        group.plot(kind='scatter', x='ind', y='-log10(p_value)', color=colors[num % len(colors)], ax=ax, s= 10000/len(data))
        x_labels.append(name)
        x_labels_pos.append((group['ind'].iloc[-1] - (group['ind'].iloc[-1] - group['ind'].iloc[0]) / 2))

    ax.set_xticks(x_labels_pos)
    ax.set_xticklabels(x_labels)
    ax.set_xlim([0, len(data)])
    #ax.set_ylim([0, data['-log10(p_value)'].max() + 1])
    ax.set_ylim([0, 10])
    ax.set_xlabel('Chromosome',fontsize=8)
    ax.set_ylabel('-log10(p_value)',fontsize=8)
    plt.title(title)
    plt.axhline(y=significance, color='gray', linestyle='-', linewidth = 0.5)
    plt.xticks(fontsize=6)#, rotation=60)
    plt.yticks(fontsize=6)
    plt.tight_layout()
    
    if refSNP:
        for index, row in data.iterrows():
            if row['-log10(p_value)'] >= significance and row['OR'] > 1:
                ax.annotate(str(row[refSNP])+'\nOR:'+str(round(row['OR'],2)), xy = (index, row['-log10(p_value)']),fontsize=6)
                f.write(str(row['#CHROM'])+'\t'+str(row['POS'])+'\t'+str(row['ID'])+'\t'+str(format(row['OR'],'.6g'))+'\t'+str(format(row['Z_STAT'],'.6g'))+'\t'+str(format(row['P'],'.6g'))+'\n')

    f.close()
    if title:
        plt.savefig(title+'_mht',dpi=300)

    cmd='sort -k6 -g '+title+'_SNPs.tmp > '+title+'_SNPs.lst && rm '+title+'_SNPs.tmp'
    subprocess.run(cmd,shell=True)
    #plt.show()


if __name__=="__main__":
    fname=sys.argv[1]
    try:
        sig=int(sys.argv[2])
    except:
        sig=5
        
    fname=fname.split('.')[0]
    if not os.path.isfile(fname+'.PHENO1.glm.logistic.hybrid'):
        cmd='plink2 --vcf '+fname+'.vcf.gz --fam '+fname+'.fam --glm allow-no-covars --adjust --out '+fname
        subprocess.run(cmd,shell=True)
        
    data_object=FD.FormatData(fname+'.PHENO1.glm.logistic.hybrid', sep = '\s+', chromosome = '#CHROM', p_value = 'P')


    GenerateManhattan(data_object, title = fname, significance = sig, colors = ['#E24E42', '#008F95'], refSNP = 'ID')

