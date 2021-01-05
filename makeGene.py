#! /usr/bin/env python3.7

import pandas as pd
import subprocess
import sys

pname=sys.argv[1:]

df=pd.read_table(pname+'.ann',sep='\t',header=None)

df.columns=['ID','GENE']
df=df[['GENE','ID']]
df2=df['ID'].str.split(':',expand=True)
df['SNP']=df2[0]+':'+df2[1]+'_'+df2[2]+'/'+df2[3]

df1=df.groupby('GENE')['SNP'].apply(' '.join).reset_index()

df3=df1['SNP'].str.split(' ',expand=True).fillna('')
df2=df1['GENE'].to_frame()
df4=df2.join(df3,how='right')

print(df4)
df4.to_csv(pname+'_groupFile_geneBasedtest.tmp',header=None,index=None,sep='\t')


cmd='awk OFS=\"\\t\" \'{$1=$1}1\' '+pname+'_groupFile_geneBasedtest.tmp > '+pname+'_groupFile_geneBasedtest.txt' \
    +' && rm '+pname+'_groupFile_geneBasedtest.tmp'
subprocess.run(cmd,shell=True)
