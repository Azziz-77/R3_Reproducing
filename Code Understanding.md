# Core Components
The system consists of three main Python files that form the backbone:
## main.py (Entry Point):
This python file contains the argument parser to accept vulnerability name and IP address. It then initializes the configuration from config.yml, creates States and AutoPT instances
and orchestrates the testing process across different models
```
 def main():
    # Parse arguments for vulnerability name and IP
    # Load config
    # Initialize states
    # Run tests across different models (GPT-3.5, GPT-4o etc)
    # Generate results
```

## autopt.py (Core Logic):
This python file implements the AutoPT class. This class handles the model initialization (whether it is GPT-3.5, GPT-4o or GPT-4omini), State machine setup, test execution, and result logging
```
class AutoPT:
    def llm_init() # Initialize LLM models
    def state_machine_init() # Setup FSM states
    def state_machine_run() # Execute the testing
    def log() # Log results
```
## psm/ folder (State Machine):
This folder contains state management logic as the following:
* state.py: Defines states (Scan, Select, Exploit etc)
* trans.py: Handles state transitions
* utils.py: Helper functions

# State Machine Implementation
## State Definitions
The system implements a Finite State Machine with five primary states:
- Scanning State
- Vulnerability Selection State
- Reconnaissance State
- Exploitation State
- Check State

![image](https://github.com/user-attachments/assets/4f38506c-d0bb-4866-9422-ab35a1da557d)


Each state has specific responsibilities:
- Scan: Use xray to scan target
- Vuln_select: Choose vulnerability to test
- Inquire: Gather vulnerability info
- Exploit: Attempt exploitation
- Check: Verify results


# Optimization Opportunities
## Memory Optimization
The system can be optimised through implementing state data compression
in addition, adding cleanup routines for completed states to further optimize history storage

## Performance Improvements
Although seems hard, the system can be further optimise the performance through adding parallel vulnerability testing

## Accuracy Enhancements
The accuracy of the tool can be further enhanced by implement result verification and implement enhanced error handling


# Testing Workflow
the system workflow is as the following: 

## Initialization
- Load configuration
- Setup state machine
- Initialize tools

## Scanning Phase
- Execute vulnerability scan
- Process results
- Generate vulnerability list

## Selection Phase
- Analyze vulnerabilities
- Prioritize targets
- Select vulnerability

## Reconnaissance Phase
- Gather vulnerability information
- Analyze exploitation methods
- Prepare attack strategy

## Exploitation Phase
- Execute exploit attempts

## Verification Phase
- Check exploitation success
- Determine next steps
- Log results
