# Copyright 2018 Alibaba Cloud Inc. All rights reserved.
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


from setuptools import setup, find_packages

PACKAGE = "alibabacloud"
VERSION = __import__(PACKAGE).__version__

requires = [
    'jmespath>=0.9.3,<1.0.0',
    'mock>=2.0.0',
]

setup(
    name=PACKAGE,
    version=VERSION,
    description='Alibaba Cloud Python SDK 2.0',
    author='Alibaba Cloud',
    author_email='alibaba-cloud-sdk-dev-team@list.alibaba-inc.com',
    url='https://github.com/aliyun/alibabacloud-python-sdk-v2',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
