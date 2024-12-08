# R3_Reproducing

This repository contains an temporarly implementation of the paper "AutoPT: How Far Are We from the End2End Automated Web Penetration Testing?" from arXiv. AutoPT is an automated penetration testing framework powered by large language models that aims to automate the entire penetration testing process.

# Overview
AutoPT uses a state machine architecture to manage different phases of penetration testing:

* Scanning state for vulnerability discovery
* Selection state for vulnerability prioritization
* Reconnaissance state for information gathering
* Exploitation state for vulnerability exploitation
* Check state for verification

The system leverages LLMs (GPT-4o, GPT-4o mini, GPT-3.5) to drive the testing process and make intelligent decisions at each stage.


## Prerequisites

Software Requirements

- Python 3.9+
- Docker
- Kali Linux (recommended) or Ubuntu 22.04

Key Python Libraries:

* langchain==0.2.15
* langchain_community==0.2.15
* langchain_core==0.2.37
* langchain_nvidia_ai_endpoints==0.2.2
* langchain_openai==0.1.23
* langgraph==0.2.16
* beautifulsoup4==4.12.3
* jsonlines==4.0.0
* PyYAML==6.0.1
* Requests==2.32.3
* termcolor==2.4.0

## Hardware Requirements

* CPU: 4+ cores recommended
* RAM: Minimum 8GB
* Storage: 10GB+ free space
* GPU: Not required but recommended for improved performance

## Installation Instructions

### 1. Clone the repository
```
git clone https://github.com/Azziz-77/R3_Reproducing
cd R3_Reproducing
```
### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure settings
* Add your OpenAI API key in config.yaml
* Modify the settings within config.yaml for debug if desired
* Choose the desired model {GPT4o, GPT4omini, GPT3.5turbo}

### 4. Install Docker for vulnerability environment
```
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

## Execution Steps:
To run the tool, first, the vulnerability environment needs to be run in order to test against. navigate to the desired vulnerability, say Broken Access Control, specifically drupal/CVE-2018-7600. and run the following: 
```
sudo docker-compose up -d
```
To verfy the docker image is up and to check the IP address, run the following:
```
sudo docker ps
sudo docker inspect <name>
```

Once the image is up, verify the connectivity using the browser and navigate to the IP address. 
To run the tool against this specific vulnerability, use the main.py file as the following:
```
python main.py --name "drupal/CVE-2018-7600" --ip_addr "the ip address of the image"
```
