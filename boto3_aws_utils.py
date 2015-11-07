#!/usr/bin/env python


def setup_profile(module):
  region, ec2_url, aws_connect_params = get_aws_connection_info(module)
  if 'profile_name' in aws_connect_params and aws_connect_params['profile_name'].strip():
    boto3.setup_default_session(profile_name=aws_connect_params['profile_name'])

  if 'profile_name' in aws_connect_params:
    del aws_connect_params['profile_name']

  del aws_connect_params['validate_certs']
  del aws_connect_params['security_token']

  return region,ec2_url, aws_connect_params

