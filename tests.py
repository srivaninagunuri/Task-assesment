# tests.py
import sys
import os

# FORCE current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting tests...")

from agent import ReasoningAgent

agent = ReasoningAgent()

tests = [   
    "If a train leaves at 14:30 and arrives at 18:05, how long is the journey?"
]

for q in tests:
    print("\nQUESTION:")
    print(q)

    result = agent.solve(q)

    print("ANSWER:")
    print(result["answer"])

print("\nAll tests completed.")
