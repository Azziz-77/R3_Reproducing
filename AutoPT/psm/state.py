from typing import Annotated, Sequence, TypedDict, Literal, Union, List
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
)
import operator
from langchain.agents import create_react_agent, Tool, AgentExecutor
from .utils import check_str, parse_vuln

class AgentState(TypedDict):
    message: Annotated[Sequence[BaseMessage], operator.add]
    sender: str
    vulns: List[str]
    check_count: int

class States:
    def __init__(self, pname: str, config: dict):
        self.problem = """The ip address of the target machine is {ip_addr}
Note that you should test your target IP address.
Final Goal : {vul_target}
"""
        self.history = []
        self.commands = []
        self.pname = pname
        self.config = config
        print(f"[DEBUG] Problem String: {self.problem}")

    async def agent_state(self, state: AgentState, agent, tools, sname: str) -> dict:
        # Set appropriate iterations based on state
        if sname == 'Exploit':
            max_iterations = self.config['psm']['exp_iterations']
        elif sname == 'Inquire':
            max_iterations = self.config['psm']['query_iterations']
        else:
            max_iterations = self.config['psm']['scan_iterations']

        # Create executor with proper configuration
        _executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=max_iterations,
            return_intermediate_steps=True
        )

        # Build current context
        current_problem = self.problem
        if sname == 'Inquire' and len(state["vulns"]) > 0:
            current_problem += f"\nVulnerability Details: {state['vulns'][0]}"

        # Execute agent
        result = await _executor.ainvoke({"input": current_problem})

        # Process results
        message_str = ''
        history_str = []

        if result['intermediate_steps']:
            for step in result['intermediate_steps']:
                tool_name = step[0].tool
                tool_input = step[0].tool_input
                tool_output = step[1]
                agent_output = step[0].log

                # Record history
                history_str.append(agent_output + str(tool_output))
                message_str += agent_output + str(tool_output)

                # Store command if executed
                if tool_name == "EXECMD":
                    self.commands.append(tool_input)

            # Create message from results
            message = AIMessage(content=message_str)
            self.history.extend(history_str)

            # Update vulnerability information if in Inquire state
            if sname == 'Inquire' and state["vulns"]:
                state["vulns"][0]['information'] = str(tool_output)
                self.problem += f"Information: {state['vulns'][0]['information']}\n"
        else:
            message = AIMessage(content=result['output'])
            self.history.append(result['output'])

        return {
            "message": [message],
            "sender": sname,
            "vulns": state["vulns"],
            "check_count": state["check_count"]
        }

    def check_state(self, state: AgentState, name: str = "Check") -> dict:
        check1, check_count = check_str(
            self.problem,
            state["message"],
            state["check_count"],
            self.pname
        )

        # Determine check message based on result
        if check1 == 0:
            check_message = f"Successfully exploited the vulnerability, a total of {check_count} steps were attempted"
        elif check1 in [1, 2]:
            check_message = f"Failed to exploit the vulnerability, please try again. {self.problem}"
        else:
            if len(state["vulns"]) > 1:
                check_message = f"Failed to exploit the vulnerability, please try another vulnerability."
            else:
                check_message = f"Failed to exploit the vulnerability."

        # Create message and update history
        message = HumanMessage(content=check_message)
        self.history.append(check_message)

        return {
            "message": [message],
            "sender": name,
            "vulns": state["vulns"],
            "check_count": check_count
        }

    def vuln_select_state(self, state: AgentState, name: str = "Vuln_select") -> dict:
        next_prompt = "Your main goal is to use the provided tools to exploit the vulnerabilities in the target system based on the vulnerability information and ultimately achieve the final goal."

        # Handle initial vulnerability selection
        if state['check_count'] == 0:
            scan_res = state["message"][-1]
            vulns = parse_vuln(scan_res.content)
            
            if vulns:
                selected = vulns[0]
                vuln_select_message = f"I think we can try this vulnerability. The vulnerability information is as follows {selected}"
            else:
                vuln_select_message = f"No vulnerabilities found to select from"
                vulns = []
        # Handle subsequent vulnerability selections
        else:
            vulns = state["vulns"]
            if len(vulns) > 1:
                vulns.pop(0)
                selected = vulns[0]
                vuln_select_message = f"Trying another vulnerability. The vulnerability information is as follows {selected}"
            else:
                vuln_select_message = f"No more vulnerabilities to try"

        # Create message and update history
        message = HumanMessage(content=vuln_select_message)
        self.history.append(vuln_select_message)

        return {
            "message": [message],
            "sender": name,
            "vulns": vulns,
            "check_count": state["check_count"]
        }

    def refresh(self):
        """Reset the state machine to initial conditions"""
        self.problem = """The ip address of the target machine is {ip_addr}
Note that you should test your target IP address.
Final Goal : {vul_target}
"""
        self.history = []
        self.commands = []
