import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DataValidator")

class DataValidator:
    """
    Validates clinical appointment data for the prediction pipeline.
    Ensures that required columns exist and data types are correct.
    """
    REQUIRED_COLUMNS = [
        "PatientId", "AppointmentID", "Gender", "ScheduledDay", 
        "AppointmentDay", "Age", "Neighbourhood", "Scholarship", 
        "Hipertension", "Diabetes", "Alcoholism", "Handcap", "SMS_received"
    ]

    @staticmethod
    def validate_schema(df: pd.DataFrame):
        missing = [col for col in DataValidator.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            logger.error(f"Missing required columns: {missing}")
            return False, missing
        logger.info("Schema validation passed.")
        return True, []

    @staticmethod
    def check_data_quality(df: pd.DataFrame):
        issues = []
        
        # Check for nulls
        null_counts = df.isnull().sum()
        if null_counts.any():
            issues.append(f"Found null values in: {null_counts[null_counts > 0].index.tolist()}")
            
        # Check Age range
        if (df['Age'] < 0).any() or (df['Age'] > 120).any():
            issues.append("Found invalid patient ages outside 0-120 range.")
            
        # Check categorical consistency
        if 'Gender' in df.columns:
            invalid_gender = [g for g in df['Gender'].unique() if g not in ['M', 'F']]
            if invalid_gender:
                issues.append(f"Invalid gender values found: {invalid_gender}")
                
        if issues:
            for issue in issues:
                logger.warning(issue)
        else:
            logger.info("Data quality check passed.")
            
        return issues

def run_pre_check(file_path: str):
    try:
        df = pd.read_csv(file_path)
        valid_schema, missing = DataValidator.validate_schema(df)
        if not valid_schema:
            return False
        
        quality_issues = DataValidator.check_data_quality(df)
        return len(quality_issues) == 0
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        return False
