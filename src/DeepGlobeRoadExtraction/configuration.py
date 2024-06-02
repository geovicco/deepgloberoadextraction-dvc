from dataclasses import dataclass
from pathlib import Path 

@dataclass(frozen=True)
class DataIngestionConfig:
    # Kaggle Credentials saved in secrets.yaml
    username: str
    token: str
    # Config.yaml
    root_dir: Path
    kaggle_dataset_id: str
    
from DeepGlobeRoadExtraction import CONFIG_FILE_PATH, SECRETS_FILE_PATH
from DeepGlobeRoadExtraction.utils.common import read_yaml, create_directories

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, secrets_filepath=SECRETS_FILE_PATH) -> None:
        self.config = read_yaml(config_filepath)
        self.secrets = read_yaml(secrets_filepath)
        create_directories([self.config.data_ingestion.root_dir])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        secrets = self.secrets.kaggle
        cfg = DataIngestionConfig(
            username=secrets.username,
            token=secrets.token,
            root_dir=Path(config.root_dir),
            kaggle_dataset_id=config.kaggle_dataset_id
        )
        return cfg