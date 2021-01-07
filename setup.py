import setuptools
import json

version = '0.3.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("ringcentral_engage_voice/version", "w") as v:
    v.write(version)

setuptools.setup(
    name="ringcentral_engage_voice",
    version=version,
    author="Drake Zhao @ RingCentral",
    author_email="drake.zhao@ringcentral.com",
    description="RingCentral Engage Voice client Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ringcentral/engage-digital-python",
    packages=setuptools.find_packages(),
    keywords=['RingCentral', 'Engage Digital', 'sdk'],
    install_requires=[i.strip() for i in open('requirements.txt').readlines()],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)