from utils.common_functions import read_yaml
from config.paths_config import *
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining

if __name__=="__main__":
    #data_ingestion = DataIngestion(read_yaml(CONFIG_PATH)) -> This is not needed as we have already ingested the data and stored it in the raw directory. We can directly process the data and train the model.
    #data_ingestion.run()

    data_processor = DataProcessor(ANIMELIST_CSV,PROCESSED_DIR)
    data_processor.run()

    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()