import kagglehub
import shutil
from src.logger import get_logger
from src.custom_exception import CustomException
from config.data_ingestion_config import * # Calls DATASET_NAME , TARGET_DIR
import zipfile
import json
import os

# Initial Setup: Ensure kagglehub is updated for optimal API performance
logger = get_logger(__name__)

class DataIngestion:
    """
    Focused DataIngestion class for the retrieval and extraction of the 
    Anime Recommendation Database 2020.
    """

    def __init__(self, dataset_name: str, target_dir: str):
        self.dataset_name = dataset_name
        self.target_dir = target_dir

        # Manifest of files to be extracted to the project raw directory
        self.required_files = [
            "anime.csv",
            "anime_with_synopsis.csv",
            "animelist.csv",
            "rating_complete.csv",
            "watching_status.csv"
        ]

    def create_raw_dir(self) -> str:
        """Initializes the raw data storage path within the project structure."""
        raw_dir = os.path.join(self.target_dir, "raw")
        if not os.path.exists(raw_dir):
            try:
                os.makedirs(raw_dir)
                logger.info(f"Initialized raw directory at: {raw_dir}")
            except Exception as e:
                logger.error("Failed to create raw directory structure.")
                raise CustomException("Directory creation error", e)
        return raw_dir

    def handle_extraction(self, path: str) -> str:
        """
        Decouples the extraction logic. Handles both direct folder 
        returns from kagglehub and zip file archives.
        """
        if os.path.isdir(path):
            logger.info(f"Source is a directory. Extraction skipped: {path}")
            return path

        if path.endswith(".zip"):
            logger.info(f"Processing zip archive: {path}")
            extract_dir = path.replace(".zip", "")
            try:
                with zipfile.ZipFile(path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
                logger.info(f"Archive extracted to: {extract_dir}")
                return extract_dir
            except Exception as e:
                logger.error("Fault detected during zip extraction.")
                raise CustomException("Zip extraction failed", e)
        
        raise CustomException("Unsupported file format provided by kagglehub.")

    def transfer_raw_files(self, dataset_root: str, raw_dir: str) -> None:
        """
        Selectively moves required CSV files from the Kaggle cache 
        to the project's local 'raw' directory.
        """
        try:
            for file_name in self.required_files:
                src_path = os.path.join(dataset_root, file_name)
                dst_path = os.path.join(raw_dir, file_name)

                if os.path.exists(src_path):
                    shutil.copy(src_path, dst_path)
                    logger.info(f"Successfully staged: {file_name}")
                else:
                    logger.warning(f"Manifest file missing from source: {file_name}")
        except Exception as e:
            logger.error("Critical error during file transfer.")
            raise CustomException("File staging failed", e)

    def download_data(self) -> None:
        """
        Orchestrates the download, extraction, and staging of the dataset.
        """
        try:
            raw_dir = self.create_raw_dir()
            
            logger.info(f"Initiating kagglehub download for: {self.dataset_name}")
            # Downloads to default kagglehub cache (~/.cache/kagglehub)
            download_path = kagglehub.dataset_download(self.dataset_name)
            logger.info(f"Download complete. Local cache: {download_path}")

            # Extract if necessary and move to project target
            dataset_root = self.handle_extraction(download_path)
            self.transfer_raw_files(dataset_root, raw_dir)
            
            logger.info("Data Ingestion: Raw files staged successfully.")
            
        except Exception as e:
            logger.error("Data Ingestion Pipeline encountered a fatal error.")
            raise CustomException("Ingestion process failed", e)

if __name__ == "__main__":
    # Ensure DATASET_NAME in config is: 'hernan4444/anime-recommendation-database-2020'
    ingestion_service = DataIngestion(
        dataset_name=DATASET_NAME,
        target_dir=TARGET_DIR
    )
    ingestion_service.download_data()