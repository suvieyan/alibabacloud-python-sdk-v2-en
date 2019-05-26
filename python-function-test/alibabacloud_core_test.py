# Copyright 2019 Alibaba Cloud Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from alibabacloud.client import ClientConfig, AlibabaCloudClient
from alibabacloud.credentials import AccessKeyCredentials
from alibabacloud.credentials.provider import RamRoleCredentialsProvider
from alibabacloud.exceptions import ServerException, InvalidRegionIDException
from alibabacloud.request import APIRequest
from base import SDKTestBase

from alibabacloud.clients.ecs_20140526 import EcsClient


class ROSClient(AlibabaCloudClient):

    def __init__(self, client_config, credentials_provider=None):
        AlibabaCloudClient.__init__(self, client_config, credentials_provider)
        self.product_code = 'ROS'
        self.product_version = '2015-09-01'
        self.location_service_code = 'ros'
        self.location_endpoint_type = 'openAPI'

    def describe_resource_types(self, support_status=None):
        api_request = APIRequest('DescribeResourceTypes', 'GET', 'http', 'ROA', 'query')
        api_request.uri_pattern = '/resource_types'
        api_request._params = {"SupportStatus": support_status}
        return self._handle_request(api_request).result


class CloudLevelTest(SDKTestBase):

    def init_config(self):
        client_config = ClientConfig(access_key_id=self.access_key_id,
                                     access_key_secret=self.access_key_secret,
                                     region_id=self.region_id)
        return client_config

    def test_rpc_with_regions_request(self):
        client_config = self.init_config()
        ecs_client = EcsClient(client_config)
        response = ecs_client.describe_regions()
        self.assertTrue(response.get("Regions"))
        self.assertTrue(response.get("RequestId"))

    def test_roa_with_resource_types_request(self):
        client_config = self.init_config()
        ros_client = ROSClient(client_config)
        response = ros_client.describe_resource_types()
        self.assertTrue(response.get("ResourceTypes"))

    def test_rpc_assume_role_request_with_sts_token(self):
        self._create_default_ram_user()
        # self._attach_default_policy()
        self._create_access_key()
        self._create_default_ram_role()

        acs_client = ClientConfig(region_id=self.region_id)
        ram_role_arn_credential = RamRoleCredentialsProvider(
            acs_client,
            AccessKeyCredentials(self.ram_user_access_key_id,
                                 self.ram_user_access_key_secret),
            self.ram_role_arn,
            "alice_test")
        client = AlibabaCloudClient(acs_client, ram_role_arn_credential)
        client.product_code = "Ecs"
        client.product_version = "2014-05-26"
        client.location_service_code = 'ecs'
        client.location_endpoint_type = "openAPI"
        api_request = APIRequest('DescribeRegions', 'GET', 'https', 'RPC')
        response = client._handle_request(api_request)

        response_credentials = response.http_request.credentials
        self.assertTrue(response_credentials.access_key_id.startswith("STS."))

        response = response.http_response.content
        ret = self.get_dict_response(response)
        self.assertTrue(ret.get("Regions"))
        self.assertTrue(ret.get("RequestId"))

    def test_roa_assume_role_request_with_sts_token(self):
        self._create_default_ram_user()
        # self._attach_default_policy()
        self._create_access_key()
        self._create_default_ram_role()

        roa_client = ClientConfig(region_id=self.region_id)
        ram_role_arn_credential = RamRoleCredentialsProvider(
            roa_client,
            AccessKeyCredentials(self.ram_user_access_key_id,
                                 self.ram_user_access_key_secret),
            self.ram_role_arn,
            "alice_test")
        client = AlibabaCloudClient(roa_client, ram_role_arn_credential)
        client.product_code = "ROS"
        client.product_version = "2015-09-01"
        client.location_service_code = 'ros'
        client.location_endpoint_type = "openAPI"
        api_request = APIRequest('DescribeResourceTypes', 'GET', 'https', 'ROA')
        api_request.uri_pattern = '/resource_types'
        api_request.path_params = None
        response = client._handle_request(api_request)

        response_credentials = response.http_request.credentials
        self.assertTrue(response_credentials.access_key_id.startswith("STS."))

        response = response.http_response.content
        ret = self.get_dict_response(response)
        self.assertTrue(ret.get("ResourceTypes"))

    def test_rpc_regions_request_with_error(self):
        client_config = ClientConfig(access_key_id=self.access_key_id,
                                     access_key_secret=self.access_key_secret,
                                     region_id="abc")
        client = AlibabaCloudClient(client_config, None)
        client.product_code = "Ecs"
        client.product_version = "2014-05-26"
        client.location_service_code = 'ecs'
        client.location_endpoint_type = "openAPI"
        api_request = APIRequest('DescribeRegions', 'GET', 'https', 'RPC')
        with self.assertRaises(InvalidRegionIDException) as e:
            client._handle_request(api_request)
        self.assertEqual(e.exception.error_message, "No such region 'abc'."
                                                    " Please check your region ID.")

    def test_rpc_regions_request_with_unicode(self):
        client_config = ClientConfig(access_key_id=self.access_key_id,
                                     access_key_secret=self.access_key_secret,
                                     region_id="cn-hangzhou")
        client = AlibabaCloudClient(client_config, None)
        client.product_code = "Ecs"
        client.product_version = "2014-05-26"
        client.location_service_code = 'ecs'
        client.location_endpoint_type = "openAPI"
        api_request = APIRequest('DescribeRegions', 'GET', 'https', 'RPC')
        api_request._params = {'OwnerAccount': "&#111;&#119;&#110;&#101;"
                                               "&#114;&#95;&#97;&#99;&#99;"
                                               "&#111;&#117;&#110;&#116;", }
        with self.assertRaises(ServerException) as e:
            client._handle_request(api_request)
        self.assertEqual(e.exception.error_code, "InvalidParameter.OwnerAccount")
        self.assertEqual(e.exception.error_message, "OwnerAccount is Invalid.")

    def test_roa_regions_types_request_with_unicode(self):
        client_config = self.init_config()
        ros_client = ROSClient(client_config)
        # with self.assertRaises(ServerException) as e:
        try:
            ros_client.describe_resource_types(support_status='&#114;&#101;')
        except Exception as e:
            self.assertEqual(e.exception.error_code, "SignatureDoesNotMatch")
            self.assertTrue(e.exception.error_message)

    def test_rpc_regions_request_with_query(self):
        client_config = ClientConfig(access_key_id=self.access_key_id,
                                     access_key_secret=self.access_key_secret,
                                     region_id="cn-hangzhou")
        client = AlibabaCloudClient(client_config, None)
        client.product_code = "Ecs"
        client.product_version = "2014-05-26"
        client.location_service_code = 'ecs'
        client.location_endpoint_type = "openAPI"
        api_request = APIRequest('DescribeRegions', 'GET', 'http', 'RPC')
        api_request._params = {'OwnerAccount': "owner&account"}
        with self.assertRaises(ServerException) as e:
            client._handle_request(api_request)
        self.assertEqual(e.exception.error_code, "InvalidParameter.OwnerAccount")
        self.assertEqual(e.exception.error_message, "OwnerAccount is Invalid.")

    def test_roa_regions_types_request_with_query(self):
        client_config = self.init_config()
        ros_client = ROSClient(client_config)
        # with self.assertRaises(ServerException) as e:
        #     ros_client.describe_resource_types(support_status='resource&types;')
        try:

            ros_client.describe_resource_types(support_status='resource&types;')

        except Exception as e:
            self.assertEqual(e.exception.error_code, "ResourceTypeNotFound")
            self.assertEqual(e.exception.error_message,
                             "The Resource Type (resource&types;) could not be found.")
