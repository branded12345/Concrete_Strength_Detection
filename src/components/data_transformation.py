import sys,os
sys.path.append("E:/ML_end_to_end/Cement_Strength_Detection")

from sklearn.impute import SimpleImputer ## HAndling Missing Values
from sklearn.preprocessing import StandardScaler # HAndling Feature Scaling

## pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from dataclasses import dataclass
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

## Data Transformation config

@dataclass
class DataTransformationconfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

## Data Ingestionconfig class

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationconfig()

    def get_data_transformation_object(self):

        try:
            logging.info('Data Transformation initiated')
            logging.info('Pipeline Initiated')

            num_cols= ['cement', 'blast_furnace_slag', 'fly_ash', 'water', 'superplasticizer',
                'coarse_aggregate', 'fine_aggregate', 'age']
            
            # Pipeline
            pipeline= Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            preprocessor= ColumnTransformer([
                ('pipeline', pipeline, num_cols)
            ])
            logging.info('Pipeline Completed')
            return preprocessor
    
        except Exception as e:
            
            logging.info("Error in Data Transformation")
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'concrete_compressive_strength'
            drop_columns = [target_column_name,'id']

            ## features into independent and dependent features

            input_feature_train_df = train_df.drop(drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            
             ## apply the transformation

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            logging.info('Processsor pickle in created and saved')

            return(
                train_arr,
                test_arr
            )
        
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise CustomException(e,sys)
