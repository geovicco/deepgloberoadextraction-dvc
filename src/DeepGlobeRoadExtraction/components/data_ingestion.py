from DeepGlobeRoadExtraction.configuration import DataIngestionConfig
import os
import subprocess
import json
from DeepGlobeRoadExtraction import logger
from kaggle.api.kaggle_api_extended import KaggleApi

class DataIngestionComponent:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config
    
    # Initialise Kaggle API
    def kaggle_init(self):
        logger.info(f'---------- Initialising Kaggle Account ----------')
        KAGGLE_CONFIG_DIR = os.path.join(os.path.expandvars('$HOME'), '.kaggle')
        KAGGLE_CONFIG_FILE = os.path.join(KAGGLE_CONFIG_DIR, 'kaggle.json')
        
        # Check if the kaggle.json file already exists and is not empty
        if os.path.exists(KAGGLE_CONFIG_FILE) and os.path.getsize(KAGGLE_CONFIG_FILE) > 0:
            logger.warning(f'---> Kaggle Account Credentials Found! {KAGGLE_CONFIG_FILE}. Remove this file and re-initialise if API token is invalid or has expired.')
            return

        os.makedirs(KAGGLE_CONFIG_DIR, exist_ok = True)
        try:
            username = self.config.username
            api_key = self.config.token
            api_dict = {"username":username, "key":api_key}
            with open(KAGGLE_CONFIG_FILE, "w", encoding='utf-8') as f:
                json.dump(api_dict, f)
            cmd = f"chmod 600 {KAGGLE_CONFIG_FILE}"
            output = subprocess.check_output(cmd.split(" "))
            output = output.decode(encoding='UTF-8')
        except Exception as e:
            logger.error(f'Failed to Initialise Kaggle Account!')
            raise e
        
    # Download Kaggle Dataset
    def download_dataset(self) -> None:
        logger.info(f'---------- Downloading Kaggle Dataset: {self.config.kaggle_dataset_id} ----------')
        try:
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(
                dataset=self.config.kaggle_dataset_id,
                path=self.config.root_dir, 
                unzip=True,
                force=False
            )
            logger.info(f'---> Kaggle dataset saved to {self.config.root_dir}')
        except  Exception as e:
            logger.error('Kaggle dataset download failed!')
            raise e
