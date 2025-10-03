"""
Master Orchestrator Agent
Uses ADK SequentialAgent to orchestrate the complete manufacturing workflow

Following ADK pattern: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/
"""

from google.adk.agents import SequentialAgent, LlmAgent

# Import all sub-agents
from demand_agent.agent import root_agent as demand_agent
from bid_coordinator_agent.agent import root_agent as bid_coordinator_agent
from cornerstone_agent.agent import root_agent as cornerstone_agent
from timeline_agent.agent import root_agent as timeline_agent
from logistics_agent.agent import root_agent as logistics_agent


# Create the Master Orchestrator using SequentialAgent
# This will execute agents in order: Demand → Bid Coordinator → Cornerstone → Timeline → Logistics
root_agent = SequentialAgent(
    name="master_orchestrator",
    sub_agents=[
        demand_agent,
        bid_coordinator_agent,
        cornerstone_agent,
        timeline_agent,
        logistics_agent
    ],
    description=(
        "Master workflow orchestrator for Cornerstone's manufacturing process. "
        "Executes the complete workflow sequentially: demand analysis → bid coordination → "
        "optimization → timeline management → logistics planning."
    )
)
