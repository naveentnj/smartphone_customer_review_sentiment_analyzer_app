from textSentimentAnalyser.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textSentimentAnalyser.pipeline.stage_02_data_transform import data_transform
from textSentimentAnalyser.logging import logger


STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e
