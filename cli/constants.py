"""
Responsible for loading all of the environmental variables.
"""
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from cidc_utils.caching import CredentialCache

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

DOMAIN = env.get('DOMAIN')
AUDIENCE = env.get('AUDIENCE')
CLIENT_ID = env.get('CLIENT_ID')
REDIRECT_URI = env.get('REDIRECT_URI')
SCOPE = env.get('SCOPE')
EVE_URL = env.get('EVE_URL')
IDP = env.get('IDP')

USER_CACHE = CredentialCache(100, 600)
FILE_EXTENSION_DICT = {
    "fa": "FASTQ",
    "fa.gz": "FASTQ",
    "fq.gz": "FASTQ"
}

BANNER = '''
##################██████╗██╗██████╗##██████╗##########################
##################██╔════╝██║██╔══██╗██╔════╝#########################
##################██║#####██║██║##██║██║##############################
##################██║#####██║██║##██║██║##############################
##################╚██████╗██║██████╔╝╚██████╗#########################
###################╚═════╝╚═╝╚═════╝##╚═════╝#########################
######################################################################
###██████╗#██████╗#███╗###███╗███╗###███╗#█████╗#███╗###██╗██████╗####
##██╔════╝██╔═══██╗████╗#████║████╗#████║██╔══██╗████╗##██║██╔══██╗###
##██║#####██║###██║██╔████╔██║██╔████╔██║███████║██╔██╗#██║██║##██║###
##██║#####██║###██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║##██║###
##╚██████╗╚██████╔╝██║#╚═╝#██║██║#╚═╝#██║██║##██║██║#╚████║██████╔╝###
###╚═════╝#╚═════╝#╚═╝#####╚═╝╚═╝#####╚═╝╚═╝##╚═╝╚═╝##╚═══╝╚═════╝####
######################################################################
#██╗#####██╗███╗###██╗███████╗####████████╗#██████╗##██████╗#██╗######
#██║#####██║████╗##██║██╔════╝####╚══██╔══╝██╔═══██╗██╔═══██╗██║######
#██║#####██║██╔██╗#██║█████╗#########██║###██║###██║██║###██║██║######
#██║#####██║██║╚██╗██║██╔══╝#########██║###██║###██║██║###██║██║######
#███████╗██║██║#╚████║███████╗#######██║###╚██████╔╝╚██████╔╝███████╗#
#╚══════╝╚═╝╚═╝##╚═══╝╚══════╝#######╚═╝####╚═════╝##╚═════╝#╚══════╝#
######################################################################'''
