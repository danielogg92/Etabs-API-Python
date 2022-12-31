# -*- coding: utf-8 -*-

def get_all_db_tables(SapModel):
    """
    gets all database tables
    
    returns all_tables
    
    import types:
        0: not importable
        1: importable but not interactively importable
        2: importable and interactively importable when the model is unlocked
        3: importable and interactively importable when the model is unlocked and locked
    """
    table_data=SapModel.DatabaseTables.GetAllTables();
    all_tables={};
    for i in range(table_data[0]):
        table_key=table_data[1][i];
        table_name=table_data[2][i];
        import_type=table_data[3][i];
        is_empty=table_data[4][i];
        all_tables[table_key]={
            'table_name':table_name,
            'import_type':import_type,
            'is_empty':is_empty};
    return all_tables;

def get_available_db_tables(SapModel):
    """
    gets the available tables from the etabs model. Not all tables will be 
    available for a model.
    
    returns all_tables
    
    import types:
        0: not importable
        1: importable but not interactively importable
        2: importable and interactively importable when the model is unlocked
        3: importable and interactively importable when the model is unlocked and locked
    """
    table_data=SapModel.DatabaseTables.GetAvailableTables();
    available_tables={};
    for i in range(table_data[0]):
        table_key=table_data[1][i];
        table_name=table_data[2][i];
        import_type=table_data[3][i];
        available_tables[table_key]={
            'table_name':table_name,
            'import_type':import_type};
    return available_tables;

#The below function is an example how to get data when using the database 
#tables.

def get_spandrel_design(SapModel):
    """
    returns: spandrels (dict)
    
    spandrels will be given a unique_id as 'Spandrel Name_Story_Location'
    """
    #get the table
    table_key='Shear Wall Spandrel Design Summary - AS 3600-2018';
    #get the database table
    spandrel_db=SapModel.DatabaseTables.GetTableForDisplayArray(table_key,GroupName='');
    GroupName=spandrel_db[0];
    TableVersion=spandrel_db[1];
    FieldsKeysIncluded=spandrel_db[2];
    NosFields=len(FieldsKeysIncluded);
    NumberRecords=spandrel_db[3];
    TableData=spandrel_db[4];
    #initiate the table
    spandrels={};
    #loop thru and assign name for each spandrel
    for i in range(NumberRecords):
        Story=TableData[i*NosFields+0];
        Spandrel=TableData[i*NosFields+1];
        Station=TableData[i*NosFields+2];
        spandrel_key='{}_{}_{}'.format(Spandrel,Story,Station);
        #top design
        TopRebar=int(TableData[i*NosFields+3]);
        TopRebarRat=float(TableData[i*NosFields+4]);
        TopRebarCmb=TableData[i*NosFields+5];
        MuTop=round(float(TableData[i*NosFields+6])*10**-6,1);
        #bottom design
        BotRebar=int(TableData[i*NosFields+7]);
        BotRebarRat=float(TableData[i*NosFields+8]);
        BotRebarCmb=TableData[i*NosFields+9];
        MuBot=round(float(TableData[i*NosFields+10])*10**-6,1);
        #shear design
        AVert=round(float(TableData[i*NosFields+11]),4);
        AHorz=float(TableData[i*NosFields+12]);
        ShearCombo=TableData[i*NosFields+13];
        Vu=round(float(TableData[i*NosFields+14])*10**-3,1);
        #diagonal reinforcement
        ADiag=TableData[i*NosFields+15];
        Mandatory=TableData[i*NosFields+16];
        ShrDiagCmb=TableData[i*NosFields+17];
        VuDiag=round(float(TableData[i*NosFields+18])*10**-3,1);
        #messages
        WarnMsg=TableData[i*NosFields+19];
        ErrMsg=TableData[i*NosFields+20];
        spandrels[spandrel_key]={'Story':Story,'Spandrel':Spandrel,
                                 'Station':Station,
                                 'TopRebar':TopRebar,'TopRebarRat':TopRebarRat,
                                 'TopRebarCmb':TopRebarCmb,'MuTop':MuTop,
                                 'BotRebar':BotRebar,'BotRebarRat':BotRebarRat,
                                 'BotRebarCmb':BotRebarCmb,'MuBot':MuBot,
                                 'AVert':AVert,'AHorz':AHorz,
                                 'ShearCombo':ShearCombo,'Vu':Vu,
                                 'ADiag':ADiag,'Mandatory':Mandatory,
                                 'ShrDiagCmb':ShrDiagCmb,'VuDiag':VuDiag,
                                 'WarnMsg':WarnMsg,'ErrMsg':ErrMsg};
    return spandrels;