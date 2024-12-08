# Input-Output Mapping
The tool initilization goes as:
```
# Command line input
python main.py --name <vulnerability_name> --ip_addr <target_ip>

# Example
python main.py --name "drupal/CVE-2018-7600" --ip_addr "172.19.0.1"
```
The inputs are: the ip address of the target machine, and the name of the vulnerability.

| Model | Success Rat | Avg Runtime | Cost |
| --- | --- | --- | --- |
| GPT-4o mini | 36% | 161.31s | $0.02423 |
| GPT-4o | 26% | 317.31s | $0.03492 |
| GPT-3.5 | 11% | 389.97s | $0.04123 |

# Model Limitations
- gpt4o_mini": "128k tokens"
- gpt4o": "128k tokens"
- gpt35": "16k tokens"

# key_challenges
- Command hallucination
- Context overflow
- Security policy restrictions

# Detection Rate
Better performance on file read vulnerabilities (+3%)
Slightly lower performance on auth bypass (-4%)
