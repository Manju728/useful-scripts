import boto3
import logging
from moto import mock_aws
import os
import pytest
import requests
from unittest.mock import patch

# Sending mocked values to environment values of lambda
PATCHED_ENV = {
    "REGION": "eu-west-1",
    "HELPER_BUCKET": "mock_bucket",
    "URL": "https://www.google.com",
}

logger = logging.getLogger(__name__)
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logger.setLevel(LOG_LEVEL)

with patch.dict("os.environ", PATCHED_ENV):
    import inspect
    import os
    import sys

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(os.path.dirname(currentdir))
    code_path = os.path.join(parentdir, "path_to_code_folder")
    dependencies_path = os.path.join(parentdir, "path_to_extra_dependencies")
    sys.path.insert(1, code_path)
    sys.path.insert(2, dependencies_path)
    # import lambda handler and required functions here


@pytest.fixture(autouse=True)
def create_mock_resource():
    # Create mock aws resource here
    mocked_aws_env = mock_aws()
    mocked_aws_env.start()
    s3_client = boto3.client("s3")
    s3_client.create_bucket(
        Bucket="mock_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )
    yield
    mocked_aws_env.stop()
    # Write code to clean up any unwanted things after test run or failure of test run


def mock_token():
    return "something"


patch_attr = "script.lambdas.lambda_folder.name_of_python_file."
urls = ["https://get-token.net", "https://get-data.net"]


@patch("script.lambdas.lambda_folder.name_of_python_file.get_api_token", mock_token)  # one way of Mocking function
# or variable inside the lambda
@mock_aws
def test_lambda_handler_true(monkeypatch, requests_mock):
    # 2nd way of mocking function or variable inside the lambda(Note: Use any one of the ways nto both)
    monkeypatch.setattr(patch_attr + "get_api_token", mock_token)
    # mocking the HTTP requests
    requests_mock.register_uri(
        "POST", urls[0], json={"access_token": "mock_token", "expires_in": 1}
    )
    requests_mock.register_uri(
        "POST",
        urls[1],
        json={"msg": "Hello! World."},
    )
    requests.post(urls[0], timeout=60)
    requests.post(urls[1], timeout=60)

    # Mock HTTP exception
    requests_mock.register_uri(
        "POST", urls[0], json={"access_token": "mock_token", "expires_in": 7199}
    )
    requests_mock.register_uri("POST", urls[1], exc=requests.exceptions.ConnectionError)
    requests.post(urls[0], timeout=60)
    # event = {
    #     "Records": [
    #         {
    #             "body": json.dumps(payload),
    #             "messageId": response["Messages"][0]["MessageId"],
    #             "receiptHandle": response["Messages"][0]["ReceiptHandle"],
    #         }
    #     ]
    # }
    # lambda_handler(event, {})
