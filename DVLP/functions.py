import sys, os, fnmatch,time
import shutil
import pandas as pd
import yaml
import hashlib

from datetime import datetime
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from functions_b4soup import *


# technical_metadata_path = "C:/Users/429300/Documents/GitHub/TD_DATALAKE/1_DATALAKE/01_LANDING_ZONE"
with open("DVLP/app_settings.yaml","r") as f:
    config = yaml.safe_load(f)

proj_path = config['proj_path']
technical_metadata_file = proj_path + '/1_DATALAKE/01_LANDING_ZONE/technical_metadata.csv'
descriptive_metadata_file = proj_path + '/1_DATALAKE/02_CURATED_ZONE/descriptive_metadata.csv'

# !!! for dev only !!!
# try:
#     os.remove(technical_metadata_file) 
#     os.remove(descriptive_metadata_file) 
# except Exception:
#     pass
# !!! for dev only !!!

# Fonctions pour PHASE 1
def ingestion_web_to_landing_zone(pattern: str, landing_path:str):
    """Based on a text pattern (with *), copy files from the datasource to datalake/Landing zone

    Args:
        pattern (str): string to lookup in file name
        landing_path (str): path of the target folder 
    """
    
    myListOfFile = []
    myListOfFileTmp = []

    source_path = proj_path + "/0_WEB"

    #-- ramène tous les noms des fichiers du répertoire 
    myListOfFileTmp = os.listdir(source_path)

    #-- Filtrer les fichiers concernés 
    myPattern = f'{pattern}.html'  

    for myEntry in myListOfFileTmp :  
        if fnmatch.fnmatch(myEntry, myPattern):
            myListOfFile.append(myEntry)

    i = 0
    
    df_final = pd.DataFrame()
    for myFileName in tqdm(myListOfFile,f"Ingestion des pages web {pattern} ..."): 
        
        # For each fail matching the pattern
        # - Copy it in the corresponding landing zone
        shutil.copy(f'{source_path}/{myFileName}',f'{landing_path}/{myFileName}',)
        # - Extract it's meta technical metadata
        tech_md = get_technical_metadata(i,f'{source_path}',f'{landing_path}/{myFileName}',pattern)
        
        df = pd.DataFrame(columns=['file_identifier', 'key', 'value'])
        
        # Parcoure de chaque élément du dictionnaire et ajoute au dataframe
        for key, value in tech_md.items():
            # Ignorer la colonne file_identifier car elle est utilisée comme index
            if key != 'file_identifier':
                # Ajoutez une nouvelle ligne au dataframe
                df = df.append({
                    'file_identifier': tech_md['file_identifier'],
                    'key': key,
                    'value': value
                }, ignore_index=True)

        # Concaténation avec le fichier précédent pour création du fichier de metadonnée
        df_final = pd.concat([df_final, df])
   
    if not os.path.isfile(technical_metadata_file):
        df_final.to_csv(technical_metadata_file, header='column_names', index=False,sep=';')
    else: # else it exists so append without writing the header
        df_final.to_csv(technical_metadata_file, mode='a', header=False, index=False,sep=';')

def get_technical_metadata(ID,source_path,dest_full_path,pattern):
    file_name = dest_full_path.split("/")[-1]
    file_size_in_octet = os.path.getsize(dest_full_path)
    file_size_in_Ko = "{:.2f}".format(file_size_in_octet/1024)
    
    import_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    technical_metadata= {
                            "file_identifier" : hashlib.md5(file_name.encode()).hexdigest(),
                            "file_size" : f"{file_size_in_Ko} Ko",
                            "file_name" : file_name,
                            "import_date": import_date,
                            "file_source": f'{source_path}/{file_name}',
                            "file_destination": f'{dest_full_path}',
                            "file_pattern": f'{pattern}'
                        }
    return technical_metadata

# Fonctions pour PHASE 2
def get_descriptive_metadata_from_technical_metadata():
    # Read technical metadata file
    tech_metadata = pd.read_csv(technical_metadata_file,delimiter=';')

    # Get path of each file in the LANDING_ZONE by filtering on 'file_destination' and droping duplicate
    df_path = tech_metadata.query("key == 'file_destination'").drop_duplicates() 
    
    # For each file unique file_identifier or AVIS, extract descriptive metadata
    
    list_file = df_path[['file_identifier','value']].values.tolist()
    # print(list_file)
    df = pd.DataFrame(columns=['file_identifier', 'key', 'value'])
    df_final = pd.DataFrame()
    for row in tqdm(list_file,f"Recupération métadonnées descriptives ..."):
        # print(row[0])
        # print(df)
        
        if fnmatch.fnmatch(row[1], "*AVIS-SOC*"):
            descr_md = get_descr_md_avis(row[0],row[1])
                       
        elif fnmatch.fnmatch(row[1], "*EMP*"):
            descr_md = get_descr_md_emp(row[0],row[1])
            
        elif fnmatch.fnmatch(row[1], "*INFO-SOC*"):
            descr_md = get_descr_md_soc(row[0],row[1])

        for key, value in descr_md.items():
            # Ignorer la colonne file_identifier car elle est utilisée comme index
            if key != 'file_identifier':
                # Ajoutez une nouvelle ligne au dataframe
                df = df.append({
                    'file_identifier': descr_md['file_identifier'],
                    'key': key,
                    'value': value
                }, ignore_index=True)

        # Concaténation avec le fichier précédent pour création du fichier de metadonnée
        df_final = pd.concat([df_final, df])

    if not os.path.isfile(descriptive_metadata_file):
        df_final.to_csv(descriptive_metadata_file, header='column_names', index=False,sep=';')
    else: # else it exists so append without writing the header
        df_final.to_csv(descriptive_metadata_file, mode='a', header=False, index=False,sep=';')

def get_descr_md_avis(identifier,path):
    Nom_CompanyG_value = Nom_CompanyG(path)
    Nombre_Avis_value = Nombre_AvisG(path)
    Rating_value = RatingG(path)
    Perc_recommandation_value = Perc_recommandationG(path)
    
    descriptive_metadata = {
                            "file_identifier": identifier,
                            "company_name": Nom_CompanyG_value,
                            "nombre_avis": Nombre_Avis_value,
                            "rating":Rating_value,
                            "perc_recommandation": Perc_recommandation_value
                            }
    return descriptive_metadata

def get_descr_md_soc(identifier,path):
    Nom_CompanyG_value = Nom_CompanyG_soc(path)
    soc_infos = soc_infosG(path)
    siege_socialG_value = siege_socialG(soc_infos)
    soc_tailleG_value = soc_tailleG(soc_infos)
    soc_fonde_leG_value = soc_fonde_leG(soc_infos) 
    soc_typeG_value = soc_typeG(soc_infos)
    soc_secteurG_value = soc_secteurG(soc_infos) 
    soc_revenuG_value = soc_revenuG(soc_infos) 
    
    
    descriptive_metadata = {
                            "file_identifier": identifier,
                            "company_name": Nom_CompanyG_value,
                            "siege_social": siege_socialG_value,
                            "taille":soc_tailleG_value,
                            "fonde_le":soc_fonde_leG_value,
                            "type":soc_typeG_value,
                            "secteur":soc_secteurG_value,
                            "revenu":soc_revenuG_value
                            }
    return descriptive_metadata

def get_descr_md_emp(identifier,path):
    Nom_OffreL_value = Nom_OffreL(path)
    Nom_EntL_value = Nom_EntL(path)
    Nom_VilleL_value = Nom_VilleL(path)
    DatePublicL_value = DatePublicL(path)
    NBCandidatsL_value = NBCandidatsL(path)
    nivHL_value = Get_nivHL(path)
    TypeEmploiL_value = Get_TypeEmploiL(path)
    FonctionL_value = Get_FonctionL(path)
    
    descriptive_metadata = {
                            "file_identifier": identifier,
                            "nom_offre": Nom_OffreL_value,
                            "nom_entreprise" : Nom_EntL_value ,
                            "nom_ville": Nom_VilleL_value,
                            "offre_date" : DatePublicL_value,
                            "offre_candidats" : NBCandidatsL_value,
                            "niveau_hierarchique" : nivHL_value,
                            "type_emploi":TypeEmploiL_value,
                            "fonction":FonctionL_value
                            }
    return descriptive_metadata