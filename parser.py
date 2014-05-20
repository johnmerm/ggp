'''
Created on May 20, 2014

@author: grmsjac6
'''

import re


kifFile = open('8puzzle.kif')
kifString = ''.join(list(kifFile))

literals = ['role','base','input','init','legal','goal','terminal','next','does','<=']
operators = ['true','distinct','or','and','not']

def propositions(kifString = kifString):
    propsReg =re.compile('\(([^\)|\(]+)\)') #anything that is enclosed in ()
    nestedPropsReg = re.compile('_p([0-9]+)')
    
    noc =kifString # re.sub(commentsReg, '', kifString)
    props = re.findall(propsReg,noc)
    cnt = 0
    allProps = []
    idx = {}
    rev_idx = {}
    lit_dict = {a:[] for a in literals}
    while len(props) >0:
        for p in props:
            pp = re.sub(r'\s+',' ',p)
            allProps.append(pp)
            noc = noc.replace('('+p+')','_p'+str(cnt))
            nps = re.findall(nestedPropsReg, p)
            if len(nps)>0:
                idx[cnt] = [int(n) for n in nps]
                for np in nps:
                    if not int(np) in rev_idx:
                        rev_idx[int(np)] = [cnt]
                    else:
                        rev_idx[int(np)].append(cnt)
            
            words = pp.split(' ')
            
            if len(words)>0 and words[0] in literals:
                lit_dict[words[0]].append(cnt)
                    
            cnt +=1
        props = re.findall(propsReg,noc)
    return allProps,idx,rev_idx,lit_dict
    
def assignments(allProps,idx,rev_idx,lit_dict):
    assigs = lit_dict['<=']
    allAssigs = {}
    for assig in assigs:
        pAssig = allProps[assig]
        tokens = pAssig.split(' ')
        left = tokens[1]
        right = tokens[2:]
        if not left in allAssigs:
            allAssigs[left] = [right]
        else:
            allAssigs[left].append(right)
    return allAssigs


allProps,idx,rev_idx,lit_dict = propositions(kifString)
print allProps
print idx
print rev_idx
print lit_dict

allAssigs = assignments(allProps, idx, rev_idx, lit_dict)
print (allAssigs)
