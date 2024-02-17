from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import regionToolset
#import time

def P_C_function(
kw_name=None,
kw_faces=None,
kw_set_point=None,
kw_coupling=None,
kw_coupling_type=None,
kw_set_coupling=None,
kw_x=None,
kw_x_value=None,
kw_y=None,
kw_y_value=None,
kw_z=None,
kw_z_value=None,):


    #print '\n\n----control output----'
    #print kw_name
    #print kw_faces
    #print kw_set_point
    #print kw_coupling
    #print kw_coupling_type
    #print kw_set_coupling
    #print kw_x
    #print kw_x_value    
    #print kw_y
    #print kw_y_value    
    #print kw_z
    #print kw_z_value            
    #print '---------------------------\n\n'

##########################################################################################
    # check if selection is valid
   
    if kw_faces == None:
        #print '\nError: Select face(s) and confirm selection before pressing Apply or OK'
        getWarningReply(message='Select face(s) and confirm selection before pressing Apply or OK!', buttons=(CANCEL,))
        return

################################################################################################################
#   initial settings

    vpName = session.currentViewportName
    modelName = session.sessionState[vpName]['modelName']
    
    ass = mdb.models[modelName].rootAssembly
    r1 = ass.referencePoints
    

#########################################################################
## Check existing names and define new one
    
    if (kw_coupling == False) and (kw_name=='Coupling-'):
        kw_name = 'RP-'
    
    if kw_name[-1] != '-':
        kw_name = kw_name + '-'

        
    featurenames = ass.features.keys()
    
    i = 0
    x = 0
    while x==0:
        x = 1
        i = i+1
        cntnname = kw_name+str(i)
        for name in featurenames:
            if name.find(cntnname) != -1:
                x = 0
    
    #cntnname = currname    
    
    if kw_coupling == True:
        rpname_a = cntnname+'_RP'
    else:
        rpname_a = cntnname

    coupname_a = cntnname
    surfname_a = cntnname+'_faces'
    
    
####################################################################
## Region and center coords

    facetuple = kw_faces
    
    
    facetemp = ass.instances[facetuple[0].instanceName].faces[0:0]
    for x in facetuple:
        i = x.index
        j = x.instanceName
        facetemp = facetemp + ass.instances[j].faces[i:i+1]
    
    faceregion = regionToolset.Region(faces=facetemp,)
    massprop = ass.getMassProperties(regions=faceregion, relativeAccuracy=HIGH, miAboutCenterOfMass=False)
    center = massprop['areaCentroid']

####################################################################
## Round center coords    
    
    nb_digits = 6
    
    centerlist = []
    for i in center:
        centerlist.append(round(i,nb_digits))

####################################################################
## Enforce coord values    

    if kw_x:
        centerlist[0] = float(kw_x_value)
    if kw_y:
        centerlist[1] = float(kw_y_value)
    if kw_z:
        centerlist[2] = float(kw_z_value)


####################################################################
## Create RP
    
    center=tuple(centerlist)

    try:
        rp = ass.ReferencePoint(point=center)
        ass.features.changeKey(fromName=rp.name, 
        toName=rpname_a)
        print('\nUsed center coords: '+str(center))
    except:
        print('\nError: Failed to create RP with center coords')
        print(str(center))
        return
    
    rp_a = r1[rp.id]
    refPoints1=(r1[rp.id], )
    
    if kw_set_point == True:
        ass.Set(referencePoints=refPoints1, name=rpname_a)
        region1=ass.sets[rpname_a]
        
    else:    
        region1=regionToolset.Region(referencePoints=refPoints1)
    
##############################################################################################    
## Create Coupling        
        
    if kw_set_coupling == True:
        ass.Surface(side1Faces=facetemp, name=surfname_a)
        region2=ass.surfaces[surfname_a]
        
    else:    
        region2=regionToolset.Region(side1Faces=facetemp)

    
    if kw_coupling == True and kw_coupling_type == 'Distributing':
    
        mdb.models[modelName].Coupling(name=coupname_a, controlPoint=region1, 
            surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=DISTRIBUTING, 
            weightingMethod=UNIFORM, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
            ur2=ON, ur3=ON)

    elif kw_coupling == True and kw_coupling_type == 'Kinematic':
    
        mdb.models[modelName].Coupling(name=coupname_a, controlPoint=region1,
            surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
            localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)


    ass.regenerate()