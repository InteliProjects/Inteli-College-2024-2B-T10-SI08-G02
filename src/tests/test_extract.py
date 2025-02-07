#import os
#import pandas as pd
#from io import BytesIO
#import pytest
#from moto import mock_aws
#import boto3
#from unittest.mock import patch
#from dataapp.etl.etl_bronze.extract import S3DataExtractor
#
## Arrange
#@pytest.fixture
#def s3_bucket_setup():
#    bucket_name = "test-bucket"
#    data = {
#        "test1.parquet": pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]}),
#        "test2.parquet": pd.DataFrame({"col1": [4, 5, 6], "col2": ["d", "e", "f"]}),
#    }
#
#    with mock_aws():
#        s3 = boto3.client("s3", region_name="us-east-1")
#        s3.create_bucket(Bucket=bucket_name)
#
#        for file_name, df in data.items():
#            buffer = BytesIO()
#            df.to_parquet(buffer, engine="pyarrow", index=False)
#            buffer.seek(0)
#            s3.upload_fileobj(buffer, bucket_name, file_name)
#
#        yield s3, bucket_name, data
#
## Act and Assert
#def test_extract_data_from_s3(s3_bucket_setup):
#    # Arrange
#    s3, bucket_name, expected_data = s3_bucket_setup
#    extractor = S3DataExtractor(bucket_name)
#
#    with patch("os.getenv", return_value=bucket_name), patch("config.connections.s3_client", return_value=s3):
#        # Act
#        results = list(extractor.extract_data_from_s3())
#
#    # Assert
#    assert len(results) == len(expected_data)
#
#    for (actual_df, actual_name), (expected_name, expected_df) in zip(results, expected_data.items()):
#        assert actual_name == expected_name.replace(".parquet", "")
#        pd.testing.assert_frame_equal(actual_df, expected_df)
