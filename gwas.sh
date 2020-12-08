#!/bin/bash

fname=$1; oname=${fname/.vcf.gz/};
rng=$(for i in {1..99};do printf %.2f"," "$(($i))e-2";done)"1"

plink2 --vcf $fname --fam $oname.fam --geno 0.01 --mind 0.01 --make-bed --out $oname
plink2 --vcf $fname --fam $oname.fam --glm allow-no-covars --adjust --out $oname 
plot_mht.py $oname.PHENO1.glm.logistic.hybrid $2

plink2 --vcf $fname --fam $oname.fam --freq alt1bins=$rng --out ${oname}1
plink2 --vcf $fname --fam $oname.fam --freq alt1bins=0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1 --out ${oname}2

plot_frq.py ${oname}1.afreq.alt1.bins
plot_frq.py ${oname}2.afreq.alt1.bins


plink2 --bfile $oname --maf 0.01 --make-bed --out ${oname}_maf
oname=${oname}_maf
plink2 --bfile $oname --glm allow-no-covars --adjust --out $oname
plot_mht.py $oname.PHENO1.glm.logistic.hybrid $2

plink2 --bfile $oname --hwe 1e-5 --make-bed --out ${oname}_hwe
oname=${oname}_hwe
plink2 --bfile $oname --hardy --out $oname
plink2 --bfile $oname --glm allow-no-covars --adjust --out $oname
plot_mht.py $oname.PHENO1.glm.logistic.hybrid $2

plink2 --bfile $oname --indep-pairwise 1500 150 0.2 --out ${oname}
plink2 --bfile $oname --extract ${oname}.prune.in --make-bed --out ${oname}_ld
oname=${oname}_ld
plink2 --bfile $oname --glm allow-no-covars --adjust --out ${oname}
plot_mht.py $oname.PHENO1.glm.logistic.hybrid $2

plink2 --bfile $oname --freq alt1bins=$rng --out ${oname}1
plink2 --bfile $oname --freq alt1bins=0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1 --out ${oname}2

plot_frq.py ${oname}1.afreq.alt1.bins
plot_frq.py ${oname}2.afreq.alt1.bins

mkdir image
cp *.png image
cp *_SNPs.lst image
