import os

from aliyunsdkcore.client import AcsClient

github_token = os.getenv('GITHUB_TOKEN')

client = AcsClient(os.getenv("ALI_ID"), os.getenv('ALI_KEY'), 'cn-hangzhou')
