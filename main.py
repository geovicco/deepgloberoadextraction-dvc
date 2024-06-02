from DeepGlobeRoadExtraction import logger
from DeepGlobeRoadExtraction.pipeline import DataIngestionPipeline

def execute_pipeline(stage_name, pipeline_class):
    try:
        logger.info(f">>>>>> Processing Stage: {stage_name} <<<<<<")
        pipeline = pipeline_class()
        pipeline.main()
        logger.info(f">>>>>> Finished Stage: {stage_name} <<<<<<\n\nx==========x\n\n")
    except Exception as e:
        logger.exception(e)
        raise e

if __name__ == '__main__':
    execute_pipeline("Data Ingestion", DataIngestionPipeline)