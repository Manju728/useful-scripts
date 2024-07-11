import json
import requests
from boto3 import Session
import sys
import subprocess

args = sys.argv
if len(args) > 1 and args[1]:
    aws_profile = args[1]
else:
    aws_profile = input("Enter AWS profile name: ")
print(f"Generating signed URL for {aws_profile} login.......")
session = Session(profile_name=aws_profile)
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
credentials = {
    'AccessKeyId': current_credentials.access_key,
    'SecretAccessKey': current_credentials.secret_key,
    'SessionToken': current_credentials.token
}
get_signin_token_url = 'https://signin.aws.amazon.com/federation'
aws_details = {
    'Action': 'getSigninToken',
    'Session': json.dumps({
        'sessionId': credentials['AccessKeyId'],
        'sessionKey': credentials['SecretAccessKey'],
        'sessionToken': credentials['SessionToken']
    })
}
response = requests.get(get_signin_token_url, params=aws_details)
signin_token = response.json()['SigninToken']
console_url = 'https://console.aws.amazon.com/'
signin_url = f"{get_signin_token_url}?Action=login&SigninToken={signin_token}&Destination={console_url}"
print(signin_url)


# def open_url_in_container(url):
#     firefox_path = r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"
#     profiles_path = r"C:\\Users\\mareedu\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
#     profile_dir = rf"{profiles_path}\\{aws_profile}"
#     command = [
#         firefox_path,
#         "-profile", profile_dir,
#         url
#     ]
#     subprocess.run(command)


# Example usage
# open_url_in_container(signin_url)
