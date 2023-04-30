import sys
import yaml
from functions import ingestion_web_to_landing_zone,get_descriptive_metadata_from_technical_metadata

# sys.path.insert(0,".")

# Récupération variables
with open("DVLP/app_settings.yaml","r") as f:
    config = yaml.safe_load(f)

proj_path = config['proj_path']


# PHASE 1 : Extrait les pages web et les déposes en LANDING_ZONE du Datalake
# + en même temps, génération des metadonnées technique 
# + chargement des ces métadonnées techniques dans CSV en LANDING_ZONE


ingestion_web_to_landing_zone('*AVIS-SOC*',proj_path + "/1_DATALAKE/01_LANDING_ZONE/AVIS")
ingestion_web_to_landing_zone('*EMP*',proj_path + "/1_DATALAKE/01_LANDING_ZONE/EMP")
ingestion_web_to_landing_zone('*INFO-SOC*',proj_path + "/1_DATALAKE/01_LANDING_ZONE/SOC")

# PHASE 2 : Relecture des métadonnées techniques
# + extraction des métadonnées descriptives contenues dans les pages balises HTML
# + nettoyage et standardisations des données (ex : nom entreprise)
# + chargement des ces métadonnées descriptives dans CSV en CURATED_ZONE
get_descriptive_metadata_from_technical_metadata()


# PHASE 3 : Transformaton en modèle décisionnel pour exploitation BI
# -> Voir PowerBI, partie ETL (PowerQuery)

# PHASE 4 : Création datavisualisation
# -> Voir PowerBI, partie dataviz