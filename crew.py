from crewai import Agent, Task, Crew
from crewai_tools import CodeInterpreterTool
from tools.custom_outputs import ColumnInfo
from data.data_ingest import load_crash_data
import yaml
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

class DataAnalysisCrew:
    def __init__(self):
        self.agents_config = load_config('config/agents.yaml')
        self.tasks_config = load_config('config/tasks.yaml')
        self.setup_agents()
        self.setup_tasks()
        self.setup_crew()

    def setup_agents(self):
        # Create Python Data Analyst agent
        self.coding_agent = Agent(
            role=self.agents_config['python_data_analyst']['role'],
            goal=self.agents_config['python_data_analyst']['goal'],
            backstory=self.agents_config['python_data_analyst']['backstory'],
            tools=[CodeInterpreterTool(unsafe_mode=True)],
            allow_delegation=self.agents_config['python_data_analyst']['allow_delegation'],
            verbose=self.agents_config['python_data_analyst']['verbose']
        )

        # Create Data Interpreter agent
        self.data_writer_agent = Agent(
            role=self.agents_config['data_interpreter']['role'],
            goal=self.agents_config['data_interpreter']['goal'],
            backstory=self.agents_config['data_interpreter']['backstory'],
            allow_delegation=self.agents_config['data_interpreter']['allow_delegation'],
            verbose=self.agents_config['data_interpreter']['verbose']
        )

    def setup_tasks(self):
        # Create data analysis task
        self.data_analysis_task = Task(
            description=self.tasks_config['data_analysis']['description'],
            agent=self.coding_agent,
            expected_output=self.tasks_config['data_analysis']['expected_output'],
            output_json=ColumnInfo,
        )

        # Create data writing task
        self.data_writing_task = Task(
            description=self.tasks_config['data_writing']['description'],
            agent=self.data_writer_agent,
            expected_output=self.tasks_config['data_writing']['expected_output']
        )

    def setup_crew(self):
        self.crew = Crew(
            agents=[self.coding_agent, self.data_writer_agent],
            tasks=[self.data_analysis_task, self.data_writing_task]
        )

    def analyze_data(self, df):
        inputs = {"df": df.to_dict(orient='records')}
        return self.crew.kickoff(inputs=inputs)

# Usage example
if __name__ == "__main__":
    import pandas as pd
    
    # Read the crash data from CSV
    df = load_crash_data()
    
    # Initialize and run the crew
    analysis_crew = DataAnalysisCrew()
    result = analysis_crew.analyze_data(df)
    print(result) 