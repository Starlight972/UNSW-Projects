import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math
import re

studentid = os.path.basename(sys.modules[__name__].__file__)


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


def question_1(exposure, countries):
    """
    :param exposure: the path for the exposure.csv file
    :param countries: the path for the Countries.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    data_1 = pd.read_csv(exposure, sep = ';', low_memory=False)
    data_1.dropna(subset=['country'],inplace=True)
    data_1 = data_1.replace({'country':
                             {'Brunei Darussalam': 'Brunei', 
                              'Cabo Verde': 'Cape Verde', 
                              'Congo': 'Republic of the Congo', 
                              'Congo DR': 'Democratic Republic of the Congo', 
                              "C�te d'Ivoire": 'Ivory Coast', 
                              'Eswatini': 'Swaziland', 
                              'Korea DPR': 'North Korea', 
                              'Korea Republic of': 'South Korea', 
                              'Lao PDR': 'Laos',
                              'Moldova Republic of': 'Moldova', 
                              'North Macedonia': 'Macedonia', 
                              'Palestine': 'Palestinian Territory', 
                              'Russian Federation': 'Russia', 
                              'United States of America': 'United States', 
                              'Viet Nam': 'Vietnam'}
                            })
    data_1.sort_values(by='country',axis=0,ascending=True,inplace=True)
    #data_1['country'].to_csv('output1.csv', index=False)
    data_2 = pd.read_csv(countries)
    #data_2['Country'].to_csv('output2.csv', index=False)
    df1 = pd.merge(data_2, data_1, left_on='Country', right_on='country')
    df1.drop(columns=['country'],inplace=True)
    df1.set_index('Country',inplace=True)
    df1.sort_values(by='Country',axis=0,ascending=True,inplace=True)
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    basic =[]
    def help(list):
        list=re.split(r"[|]", list)
        for x in list:
            if x != '':
                basic.append(json.loads(x))            
        return basic

    df2=df1.copy(True)
    df2['Cities'].apply(help)
    df=pd.DataFrame(basic)
    df.drop_duplicates(subset=['Country','Latitude','Longitude'], keep='first', inplace=True)
    df=df.reset_index(drop=True)
    temp=df[['Latitude','Longitude']].groupby(df['Country']).mean()
    df2=pd.merge(df2,temp,left_on='Country',right_on='Country')
    df2.rename(columns={'Latitude':'avg_latitude', 'Longitude':'avg_longitude'}, inplace = True)
    #################################################

    log("QUESTION 2", output_df=df2[["avg_latitude", "avg_longitude"]], other=df2.shape)
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    def rad(d):
        return d * math.pi / 180.0

    def getDistance(lat1, lng1, lat2, lng2):
        EARTH_REDIUS = 6373
        radLat1 = rad(lat1)
        radLat2 = rad(lat2)
        a = radLat1 - radLat2
        b = rad(lng1) - rad(lng2)
        s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
        s = s * EARTH_REDIUS
        return s

    df3=df2.copy(True)
    df3['distance_to_Wuhan'] = df3.apply(lambda x: getDistance(30.5928, 114.3055, x['avg_latitude'], x['avg_longitude']), axis=1)
    df3.sort_values(by='distance_to_Wuhan',axis=0,ascending=True,inplace=True)
    #################################################

    log("QUESTION 3", output_df=df3[['distance_to_Wuhan']], other=df3.shape)
    return df3


def question_4(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    data_3 = pd.read_csv(continents)
    data_3 = data_3.replace({'Country':
                             {'Burkina': 'Burkina Faso', 
                              'Burma (Myanmar)': 'Myanmar',
                              'CZ': 'Czech Republic',
                              'Congo': 'Republic of the Congo', 
                              'Congo, Democratic Republic of': 'Democratic Republic of the Congo', 
                              'Korea, North': 'North Korea', 
                              'Korea, South': 'South Korea',
                              'Russian Federation': 'Russia', 
                              'US': 'United States', }
                            })
    temp = pd.merge(df2, data_3, left_on='Country', right_on='Country')
    def shift_comma(x):
        if x == 'No data' or x == 'x':
            x = ''
        else:
            x=re.split(r"[,]", x)
            x='.'.join(x)
        return x

    temp['Covid_19_Economic_exposure_index']=temp['Covid_19_Economic_exposure_index'].apply(shift_comma)
    temp['Covid_19_Economic_exposure_index'] = pd.to_numeric(temp['Covid_19_Economic_exposure_index'],errors='coerce')

    avg=temp['Covid_19_Economic_exposure_index'].groupby(temp['Continent']).mean()
    df4=pd.merge(data_3['Continent'], avg, left_on='Continent',right_on='Continent')
    df4.drop_duplicates(subset=None, keep='first', inplace=True)

    df4.rename(columns={'Covid_19_Economic_exposure_index':'average_covid_19_Economic_exposure_index'}, inplace = True)
    df4.set_index('Continent',inplace=True)
    df4.sort_values(by='average_covid_19_Economic_exposure_index',axis=0,ascending=True,inplace=True)
    #################################################

    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


def question_5(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df5
            Data Type: dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
    def shift_value(x):
        if x == 'No data' or x == 'x':
            x = ''
        else:
            x=re.split(r"[,]", x)
            x='.'.join(x)
        return x

    temp=df2.copy(True)
    temp['Foreign direct investment']=temp['Foreign direct investment'].apply(shift_value)
    temp['Foreign direct investment']= pd.to_numeric(temp['Foreign direct investment'],errors='coerce')
    temp['Net_ODA_received_perc_of_GNI']=temp['Net_ODA_received_perc_of_GNI'].apply(shift_value)
    temp['Net_ODA_received_perc_of_GNI']= pd.to_numeric(temp['Net_ODA_received_perc_of_GNI'],errors='coerce')
    avg_Foreign=temp['Foreign direct investment'].groupby(temp['Income classification according to WB']).mean()
    avg_Net=temp['Net_ODA_received_perc_of_GNI'].groupby(temp['Income classification according to WB']).mean()
    df5=pd.merge(temp['Income classification according to WB'], avg_Foreign, left_on='Income classification according to WB',right_on='Income classification according to WB')
    df5=pd.merge(df5, avg_Net, left_on='Income classification according to WB',right_on='Income classification according to WB')
    df5.drop_duplicates(subset=None, keep='first', inplace=True)
    df5.rename(columns={'Income classification according to WB': 'Income Class', 'Foreign direct investment': 'Avg Foreign direct investment', 'Net_ODA_received_perc_of_GNI': 'Avg_ Net_ODA_received_perc_of_GNI'}, inplace = True)
    df5.set_index('Income Class',inplace=True)
    #################################################

    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5


def question_6(df2):
    """
    :param df2: the dataframe created in question 2
    :return: cities_lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    cities_lst = []
    #################################################
    # Your code goes here ...
    basic =[]
    def help(list):
        list=re.split(r"[|]", list)
        for x in list:
            if x != '':
                basic.append(json.loads(x))            
        return basic

    temp=df2.copy(True)
    temp=temp.loc[temp['Income classification according to WB']=='LIC']
    temp['Cities'].apply(help)
    df=pd.DataFrame(basic)
    df.set_index('Population',inplace=True)
    df.sort_values(by='Population',axis=0,ascending=False,inplace=True)
    df.drop_duplicates(subset=['Country','Latitude','Longitude'], keep='first', inplace=True)
    df=df.head(5)
    cities_lst=df['City'].values.tolist()
    #################################################

    log("QUESTION 6", output_df=None, other=cities_lst)
    return cities_lst


def question_7(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    def help(list):
        list=re.split(r"[|]",list)
        for x in list:
            if x != '':
                basic.append(json.loads(x))           
        return basic

    temp=df2.copy(True)
    basic =[]
    temp['Cities'].apply(help)
    df=pd.DataFrame(basic)
    # cause a city in a country has multiple names
    # sometimes one of city's name in A country is same in B country
    # if drop duplicates by a Latitude and Longitude and keep first or last in a country
    # it will lose some results
    # thus, in here I do not do de-duplication
    df=df[['Country','City']]
    df.drop_duplicates(subset=None, keep='first', inplace=True) 
    a=df.groupby('City',as_index=False).count()    
    a.drop(index = (a.loc[a['Country'] == 1].index),inplace=True)    
    temp=pd.merge(df, a, left_on='City', right_on='City')
    temp.drop(columns=['Country_y'],inplace=True)
    temp.rename(columns={'Country_x': 'countries', 'City': 'city'}, inplace = True)
    #temp=temp.groupby('City')['Country_x'].apply(lambda x: x.str.cat(sep=',')).reset_index()
    temp=temp.groupby('city')['countries'].apply(lambda x: x.tolist()).reset_index()
    temp.set_index('city',inplace=True)
    df7=temp.copy(True)
    #################################################

    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7


def question_8(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    data_3 = pd.read_csv(continents)
    data_3 = data_3.replace({'Country':
                             {'Burkina': 'Burkina Faso', 
                              'Burma (Myanmar)': 'Myanmar',
                              'CZ': 'Czech Republic',
                              'Congo': 'Republic of the Congo', 
                              'Congo, Democratic Republic of': 'Democratic Republic of the Congo', 
                              'Korea, North': 'North Korea', 
                              'Korea, South': 'South Korea',
                              'Russian Federation': 'Russia', 
                              'US': 'United States', }
                            })
    temp = pd.merge(df2, data_3, left_on='Country', right_on='Country')
    temp=temp.loc[temp['Continent']=='South America']

    def sum_population(data):
        basic = []
        data=re.split(r"[|]", data)
        for x in data:
            if x != '':
                basic.append(json.loads(x))
        df=pd.DataFrame(basic)
        # bacause some cities in one country has same Latitude and Longitude
        # the population of them would be different
        # so in here, subset is None
        df.drop_duplicates(subset=None, keep='first', inplace=True)
        df=df.reset_index(drop=True)
        temp=df['Population'].groupby(df['Country']).sum()
        for i in temp:
            return i

    def percentage(data):
        output = (data/world_population) * 100
        return output

    def plt_text(data):
        for a, b in zip(x, y):
            plt.text(a-0.3, b+0.05, '%.2f%%' % b,fontsize=20)

    temp2=pd.merge(df2, data_3, left_on='Country', right_on='Country')
    temp2['Population']=temp2['Cities'].apply(sum_population)
    world_population=temp2['Population'].sum()

    temp['Population']=temp['Cities'].apply(sum_population)
    temp['percentage of the world population']=temp['Population'].apply(percentage)
    temp = temp[['Country', 'percentage of the world population']]
    temp=temp.reset_index(drop=True)
    label=temp['Country'].tolist()
    temp.set_index('Country',inplace=True)
    x = np.arange(len(temp))
    y=temp['percentage of the world population'].tolist()
    plt.figure(figsize=(20,10))
    plt.title('Percentage of the world population is living in each South American country',fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=20)
    temp['percentage of the world population'].apply(plt_text)
    plt.bar(x, height=y, tick_label=label)
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_9(df2):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    def shift_value(x):
        if x == 'No data' or x == 'x':
            x = ''
        else:
            x=re.split(r"[,]", x)
            x='.'.join(x)
        return x

    def get_dict(x):
        for i in range(len(list2)): 
            dit={list1[i]:list2[i]}
            dict.update(dit)
        return dict

    temp=df2.copy(True)

    temp['Foreign direct investment']=temp['Foreign direct investment'].apply(shift_value)
    temp['Foreign direct investment']= pd.to_numeric(temp['Foreign direct investment'],errors='coerce')

    temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import']=temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'].apply(shift_value)
    temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import']= pd.to_numeric(temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'],errors='coerce')

    temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI']=temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'].apply(shift_value)
    temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI']= pd.to_numeric(temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'],errors='coerce')

    temp['Foreign direct investment, net inflows percent of GDP']=temp['Foreign direct investment, net inflows percent of GDP'].apply(shift_value)
    temp['Foreign direct investment, net inflows percent of GDP']= pd.to_numeric(temp['Foreign direct investment, net inflows percent of GDP'],errors='coerce')

    sum_Foreign=temp['Foreign direct investment'].groupby(temp['Income classification according to WB']).sum()
    sum_with_food=temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'].groupby(temp['Income classification according to WB']).sum()
    sum_no_food=temp['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'].groupby(temp['Income classification according to WB']).sum()
    sum_net_GDP=temp['Foreign direct investment, net inflows percent of GDP'].groupby(temp['Income classification according to WB']).sum()


    df=pd.merge(temp['Income classification according to WB'], sum_no_food, left_on='Income classification according to WB',right_on='Income classification according to WB')
    df=pd.merge(df, sum_with_food, left_on='Income classification according to WB',right_on='Income classification according to WB')
    df=pd.merge(df, sum_net_GDP, left_on='Income classification according to WB',right_on='Income classification according to WB')
    df=pd.merge(df, sum_Foreign, left_on='Income classification according to WB',right_on='Income classification according to WB')

    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df.set_index('Income classification according to WB',inplace=True)

    dict={}
    list1=df.index.tolist()
    list2=df.values.tolist()
    list3=df.columns.tolist()
    df.apply(get_dict)
    df9=pd.DataFrame(dict)
    df9['Metrics']=list3
    df9.set_index('Metrics',inplace=True)
    df9.plot(kind='bar', title='Compare the Low Middle and High income level countries based on 4 metrics', fontsize=10,figsize=(25,10),rot=0)

    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_10(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    :param continents: the path for the Countries-Continents.csv file
    """

    #################################################
    # Your code goes here ...
    def sum_population(data):
        basic = []
        data=re.split(r"[|]", data)
        for x in data:
            if x != '':
                basic.append(json.loads(x))
        df=pd.DataFrame(basic)
        # bacause some cities in one country has same Latitude and Longitude
        # the population of them would be different
        # so in here, subset is None
        df.drop_duplicates(subset=None, keep='first', inplace=True)
        df=df.reset_index(drop=True)
        temp=df['Population'].groupby(df['Country']).sum()
        for i in temp:
            return i

    data_3 = pd.read_csv(continents)
    data_3 = data_3.replace({'Country':
                             {'Burkina': 'Burkina Faso', 
                              'Burma (Myanmar)': 'Myanmar',
                              'CZ': 'Czech Republic',
                              'Congo': 'Republic of the Congo', 
                              'Congo, Democratic Republic of': 'Democratic Republic of the Congo', 
                              'Korea, North': 'North Korea', 
                              'Korea, South': 'South Korea',
                              'Russian Federation': 'Russia', 
                              'US': 'United States', }
                            })
    temp = pd.merge(df2, data_3, left_on='Country', right_on='Country')
    temp['Population']=temp['Cities'].apply(sum_population)
    Asia_df=temp.loc[temp['Continent']=='Asia']
    Europe_df=temp.loc[temp['Continent']=='Europe']
    Africa_df=temp.loc[temp['Continent']=='Africa']
    NA_df=temp.loc[temp['Continent']=='North America']
    SA_df=temp.loc[temp['Continent']=='South America']
    Oceania_df=temp.loc[temp['Continent']=='Oceania']
    plt.figure(figsize=(20,10))
    plt.title('Points representing countries in different continents, in the world',fontsize=20)
    plt.xlabel('avg_longitude')
    plt.ylabel('avg_latitude')
    plt.scatter(x=Asia_df['avg_longitude'],y=Asia_df['avg_latitude'],s=Asia_df['Population']/5000,alpha=0.5,c='r',label='Asia',marker='.')
    plt.scatter(x=Europe_df['avg_longitude'],y=Europe_df['avg_latitude'],s=Europe_df['Population']/5000,alpha=0.5,c='g',label='Europe',marker='.')
    plt.scatter(x=Africa_df['avg_longitude'],y=Africa_df['avg_latitude'],s=Africa_df['Population']/5000,alpha=0.5,c='y',label='Africa',marker='.')
    plt.scatter(x=NA_df['avg_longitude'],y=NA_df['avg_latitude'],s=NA_df['Population']/5000,alpha=0.5,c='b',label='North America',marker='.')
    plt.scatter(x=SA_df['avg_longitude'],y=SA_df['avg_latitude'],s=SA_df['Population']/5000,alpha=0.5,c='m',label='South America',marker='.')
    plt.scatter(x=Oceania_df['avg_longitude'],y=Oceania_df['avg_latitude'],s=Oceania_df['Population']/5000,alpha=0.5,c='c',label='Oceania',marker='.')
    plt.legend(markerscale=0.2,fontsize=10)
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("exposure.csv", "Countries.csv")
    df2 = question_2(df1.copy(True))
    df3 = question_3(df2.copy(True))
    df4 = question_4(df2.copy(True), "Countries-Continents.csv")
    df5 = question_5(df2.copy(True))
    lst = question_6(df2.copy(True))
    df7 = question_7(df2.copy(True))
    question_8(df2.copy(True), "Countries-Continents.csv")
    question_9(df2.copy(True))
    question_10(df2.copy(True), "Countries-Continents.csv")