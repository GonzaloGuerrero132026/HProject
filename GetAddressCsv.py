import pandas as pd 
import requests
from faker import Faker

def GetInfoAddress():
    df = pd.read_csv('postcodes.csv')
    df=df[df['In Use?']=='Yes']
    df=df[df['County'].notnull()].reset_index(drop=True)
    df=df[["Postcode","In Use?","County","District","Ward","Country","Population","Rural/urban","Region","Postcode area","Postcode district"]]
    df=df[df['Population'].notnull()].reset_index(drop=True)
    df=df[df['District'].notnull()].reset_index(drop=True)
    df=df[df['Ward'].notnull()].reset_index(drop=True)
    df=df[df['Country'].notnull()].reset_index(drop=True)
    groupby_County = df.groupby('County')
    counties_df=pd.DataFrame(groupby_County["County"].first())
    counties_list = counties_df["County"].values.tolist()
    dict_postcodes_bycounty = {}
    for element in counties_list:
        dict_postcodes_bycounty[element] = groupby_County.get_group(element).reset_index(drop=True)
    return counties_list,dict_postcodes_bycounty 

def generate_fake_uk_address():
    # use faker to generate a fake street address based on the postcode
    fake = Faker('en_GB')
    street_name = fake.street_name()
    street_number = fake.building_number()
    full_address = f"{street_number} {street_name}"
    return full_address  

def AddAddress(Dictionary):
    for Key in Dictionary:
        list_of_Addresses = []
        for row in range(len(Dictionary[Key].index)):
            address = generate_fake_uk_address()
            list_of_Addresses.append(address)
        Dictionary[Key].insert(loc=0, column="Address", value=list_of_Addresses)
    return Dictionary

def MergeDct(Dictionary):
    df = pd.DataFrame()
    count = 0
    for key in Dictionary:
        if count == 0:
            df = Dictionary[key]
        else:
            df = df.append(Dictionary[key]).reset_index(drop=True)
        count = count + 1
    return df

def CreateFileAddress():
    List_Prueba,Dict_Prueba = GetInfoAddress()
    dct = AddAddress(Dict_Prueba).copy()
    df_to_export = MergeDct(dct)
    df_to_export.to_csv('AddressInfo.csv')
    return 0 