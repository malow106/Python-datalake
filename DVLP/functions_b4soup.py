from bs4 import BeautifulSoup
import os, time, json, unicodedata

import re

def bs4_parser(HTMLPathFileName):
    HTMLFile = open(HTMLPathFileName, "r", encoding="utf8")
    index = HTMLFile.read()
    S = BeautifulSoup(index, 'lxml')
    return S

def Nom_CompanyG (HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)
    company_name = S.find("span", {"id": "DivisionsDropdownComponent"})\
                  .text
    return clean_result(company_name)

def clean_result(text_string):
    return unicodedata.normalize("NFKD",text_string)

def Nombre_AvisG (HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)
    Nombre_Avis = S.find("div",{"id":"EIProductHeaders"})\
                   .select("span")[3]\
                   .text\
                   .replace(" ","")
    return clean_result(Nombre_Avis)

def RatingG (HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)
    Rating = S.find_all("div",
                        {"class": 
                         "v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large"})[0]\
              .text
    return clean_result(Rating)

def Perc_recommandationG(HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)
    try:
        Perc_recommandation = S.find("div",{"id":"EmpStats_Recommend"}).select("tspan")[0].text
    except:
        Perc_recommandation = ''
    return clean_result(Perc_recommandation)

def Nom_OffreL(HTMLPathFileName) : 
    S = bs4_parser(HTMLPathFileName)
    
    nom_offre = S.find_all("div", {"class": "topcard__content-left"})[0]\
                     .select("h1")[0]\
                     .text    
    return clean_result(nom_offre) 

def Nom_EntL(HTMLPathFileName) :
    
    S = bs4_parser(HTMLPathFileName)
    
    try:
        nom_societe = S.find_all("div", {"class": "topcard__content-left"})[0]\
                           .select("h3")[0]\
                           .select("span")[0]\
                           .text
    except Exception:
            nom_societe = ''
            
    return clean_result(nom_societe)

def Nom_VilleL(HTMLPathFileName) :
    
    S = bs4_parser(HTMLPathFileName)
    
    nom_ville = S.find_all("div", {"class": "topcard__content-left"})[0]\
                     .select("h3")[0]\
                     .select("span")[-1].text
    return clean_result(nom_ville) 

def DatePublicL(HTMLPathFileName) : 
    
    S = bs4_parser(HTMLPathFileName)
    
    offre_date = S.find_all("div", {"class": "topcard__content-left"})[0]\
                     .select("h3")[1]\
                     .select("span")[0].text
  
    return clean_result(offre_date)

def NBCandidatsL(HTMLPathFileName) : 
    S = bs4_parser(HTMLPathFileName)
    

    try:
            offre_candidats =  S.find_all("div", {"class": "topcard__content-left"})[0]\
                                .select("h3")[1]\
                                .select("figure")[0].text
    except:
            offre_candidats = ''
    return  clean_result(offre_candidats)

def Get_nivHL(HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)
    
    myTest = str(S.find_all('li', attrs = {'class':"job-criteria__item"})[0].contents[1])
    myTxtTmp = str(myTest)
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTxtTmp1 = re.sub('<span class="job-criteria__text job-criteria__text--criteria">','', myTxtTmp)
        myTxtTmp2 = re.sub('</span>','', myTxtTmp1)
        Result =   myTxtTmp2
    return Result

def Get_TypeEmploiL(HTMLPathFileName):
    
    S = bs4_parser(HTMLPathFileName)
    
    myTest = str(S.find_all('li', attrs = {'class':"job-criteria__item"})[1].contents[1])
    myTxtTmp = str(myTest)
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTxtTmp1 = re.sub('<span class="job-criteria__text job-criteria__text--criteria">','', myTxtTmp)
        myTxtTmp2 = re.sub('</span>','', myTxtTmp1)
        Result =   myTxtTmp2
    return Result

def Get_FonctionL(HTMLPathFileName):

    S = bs4_parser(HTMLPathFileName)
    myTest = str(S.find_all('li', attrs = {'class':"job-criteria__item"})[2].contents[1])
    myTxtTmp = str(myTest)
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTxtTmp1 = re.sub('<span class="job-criteria__text job-criteria__text--criteria">','', myTxtTmp)
        myTxtTmp2 = re.sub('</span>','', myTxtTmp1)
        Result =   myTxtTmp2
    return Result

def Nom_CompanyG_soc(HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)
    Nom_Company = S.find("span", {"id": "DivisionsDropdownComponent"})\
                   .text
    return clean_result(Nom_Company)

def soc_infosG(HTMLPathFileName):
    S = bs4_parser(HTMLPathFileName)

    labels = S.find("div", {"id": "EmpBasicInfo"}).select("label")
    labels_list = [elem.text for elem in labels ]
    values = S.find("div", {"id": "EmpBasicInfo"}).select("span")
    values_list = [elem.text for elem in values ]
    soc_infos={}
    for idx,label in enumerate(labels_list):
        soc_infos.update({label:values_list[idx]})
    return soc_infos
    
def siege_socialG(soc_infos):
    try:    
        siege_social = soc_infos["Siège social"]
    except:
        siege_social = ''
    return clean_result(siege_social)

def soc_tailleG(soc_infos):
    soc_taille = soc_infos["Taille"]
    return clean_result(soc_taille)

def soc_fonde_leG(soc_infos):
    soc_fonde_le = soc_infos["Fondé en"]
    return clean_result(soc_fonde_le)

def soc_typeG(soc_infos):
    soc_type = soc_infos["Type"]
    return clean_result(soc_type)

def soc_secteurG(soc_infos):
    soc_secteur = soc_infos["Secteur"]
    return clean_result(soc_secteur)

def soc_revenuG(soc_infos):
    soc_revenu =  soc_infos["Revenu"]
    return clean_result(soc_revenu)
