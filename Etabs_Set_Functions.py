# -*- coding: utf-8 -*-
from Etabs_Get_Functions import *;

def add_australia_conc_materials(SapModel,delete_existing=False):
    """
    This will set all the concrete grades with material properties to AS3600,
    20,25,32,40,50,60,65,70,80,100. The materials will have the designation
    'Conc-40' etc
    
    Parameters
    SapModel : Pointer (refer to function connect_to_etabs)
    delete_existing : Boolean. If True will delete all existing concrete 
                      materials
    
    Returns None
    """
    conc_mat_to_del=[];
    #Get existing concrete materials to be deleted
    if(delete_existing==True):
        all_materials=get_all_materials(SapModel);
        for mat in all_materials:
            if(all_materials[mat]['mat_type']=='Concrete'):
                conc_mat_to_del+=[mat];
    conc_grade=[25,32,40,50,65,80,100];
    #Delete materials
    for mat in conc_mat_to_del:
        prop_del=SapModel.PropMaterial.Delete(mat);
        if(prop_del==1):
            print('Deleting material {} unsuccessful'.format(mat));
    for grade in conc_grade:
        conc_nm="CONC-"+str(grade);
        new_prop=SapModel.PropMaterial.AddMaterial(conc_nm,2,"User","AS3600",
                                                   str(grade)+'MPa',
                                                   UserName=conc_nm);
        isLightweight=False;
        fcsFact=0.0;
        SSType=2;
        SSHysType=4;
        strainAtFc=0.003;
        strainAtUlt=0.0035;
        SapModel.PropMaterial.SetOConcrete(conc_nm,grade,isLightweight,fcsFact,
                                           SSType,SSHysType,strainAtFc,
                                           strainAtUlt)
        conc_E={25:26700,
                32:30100,
                40:32800,
                50:34800,
                65:37400,
                80:39600,
                100:42200};
        concU=0.2
        concA=10*10**-6
        SapModel.PropMaterial.SetMPIsotropic(conc_nm,conc_E[grade],concU,concA);
        SapModel.PropMaterial.SetWeightAndMass(conc_nm,1,24.6*10**-6)
    return None;