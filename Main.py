import comtypes.client

def connect_to_etabs():
    """
    Return Values:
    SapModel (type cOAPI pointer)
    EtabsObject (type cOAPI pointer)
    """
    #attach to a running instance of ETABS
    try:
        #get the active ETABS object
        EtabsObject=comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    except (OSError,comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    #create SapModel object
    SapModel=EtabsObject.SapModel
    #setEtabsUnits()
    return SapModel,EtabsObject;

def get_story_data(SapModel):
    """
    returns:
    storyData (list)
    """
    #Get the data using API
    story_in=SapModel.Story.GetStories()
    #Separate the data to lists
    nos_stories=story[0];
    story_nms=story[1];
    story_eles=story[2];
    story_hgts=story[3];
    is_master_story=story[4];
    similar_to_story=story[5];
    splice_above=story[6];
    splice_height=story[7];
    #Combine data into one list called story_data
    story_data=[];
    for i in range(len(story_nms)):
        j=-1-i;
        story_data.append([story_nms[j],
                           round(story_hgts[j],3),
                           round(story_eles[j],3),
                           is_master_story[j][3],
                           similar_to_story[j],
                           splice_above[j],
                           splice_height[j]]);
    return story_data;

def set_etabs_units(SapModel,length="mm",force="N"):
    """
    length can be either "m" or "mm"
    force can be either "N" or "kN"
    """
    if(length=="mm" and force=="N"):
        SapModel.SetPresentUnits(9);
    elif(length=="mm" and force=="kN"):
        SapModel.SetPresentUnits(5);
    elif(length=="m" and force=="N"):
        SapModel.SetPresentUnits(10);
    elif(length=="m" and force=="kN"):
        SapModel.SetPresentUnits(6);
    return None;
