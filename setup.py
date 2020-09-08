'''
Created on 16 jun. 2020

@author: isidoro
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
    
setuptools.setup(
    name="pttapi",
    version="0.0.5",
    author="ptt team",
    author_email="pttteam@plug2teams.com",
    description="It's pip... with git.",
    long_description=long_description,
    url="https://github.com/isanlui/public_ptt_api.git",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

