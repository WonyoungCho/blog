#! /usr/bin/env python3


def make_ann(bedFile,dataFile):
    inbim = dataFile+'.bim'
    inbed = bedFile+'.bed'
    out   = dataFile+'.ann'
    
    afile=open(inbim,'r')
    bfile=open(inbed,'r')
    ofile=open(out,'w')

    bline=bfile.readline()
    blines=bline.split()

    if len(blines[0].split('chr'))==1:
        bchrm=blines[0].split('chr')[0]
    elif len(blines[0].split('chr')) > 1:
        bchrm=blines[0].split('chr')[1]
    bstart=blines[1]
    bend=blines[2]
    bgene=blines[3]

    aline=afile.readline()
    alines=aline.split()

    achrm=alines[0]
    aID  =alines[1]
    apos =alines[3]
    
    while 1:
        if bchrm == 'X':
            bchrm = 23
            
        if int(achrm) == int(bchrm):
            if (int(apos) >= int(bstart)) and (int(apos) <= int(bend)):
                annot=aID+'\t'+bgene+'\n'
                ofile.write(annot)
                
                aline=afile.readline()
                if not aline:break
                alines=aline.split()
                
                achrm=alines[0]
                aID  =alines[1]
                apos =alines[3]

            elif int(apos) < int(bstart):
                aline=afile.readline()
                if not aline:break
                alines=aline.split()
                
                achrm=alines[0]
                aID  =alines[1]
                apos =alines[3]

            elif int(apos) > int(bend):
                bline=bfile.readline()
                if not bline:break
                blines=bline.split()

                if len(blines[0].split('chr'))==1:
                    bchrm=blines[0].split('chr')[0]
                elif len(blines[0].split('chr')) > 1:
                    bchrm=blines[0].split('chr')[1]

                bstart=blines[1]
                bend=blines[2]
                bgene=blines[3]
                
        elif int(achrm) > int(bchrm) :
            bline=bfile.readline()
            if not bline:break
            blines=bline.split()

            if len(blines[0].split('chr'))==1:
                bchrm=blines[0].split('chr')[0]
            elif len(blines[0].split('chr')) > 1:
                bchrm=blines[0].split('chr')[1]
            
            bstart=blines[1]
            bend=blines[2]
            bgene=blines[3]

        elif int(achrm) < int(bchrm) :
            aline=afile.readline()
            if not aline:break
            alines=aline.split()
            
            achrm=alines[0]
            aID  =alines[1]
            apos =alines[3]


    return True
