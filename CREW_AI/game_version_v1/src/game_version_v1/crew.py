from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class GameVersionV1():
    """GameVersionV1 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def game_logic_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['game_logic_agent'],
            model=self.agents_config['game_logic_agent']['model'],
            verbose=True
        )

    @agent
    def ui_ux_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ui_ux_agent"],
            model=self.agents_config["ui_ux_agent"]["model"],
            verbose=True
        )

    @agent
    def user_input_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["user_input_agent"],
            model=self.agents_config["user_input_agent"]["model"],
            verbose=True
        )

    @agent
    def code_integrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["code_integrator_agent"],
            model=self.agents_config["code_integrator_agent"]["model"],
            verbose=True
        )

    @agent
    def tester_debugger_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["tester_debugger_agent"],
            model=self.agents_config["tester_debugger_agent"]["model"],
            verbose=True
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def generate_game_logic(self) -> Task:
      return Task(
          config=self.tasks_config["generate_game_logic"],
      )

    @task
    def design_ui_ux(self) -> Task:
      return Task(
          config=self.tasks_config["design_ui_ux"],
      )
    
    @task
    def handle_input_controls(self) -> Task:
      return Task(
          config=self.tasks_config["handle_input_controls"],
      )

    @task
    def handle_input_controls(self) -> Task:
      return Task(
          config=self.tasks_config["handle_input_controls"],
      )
    
    @task
    def integrate_code_modules(self) -> Task:
      return Task(
          config=self.tasks_config["integrate_code_modules"],
      )
    
    @task
    def test_and_debug_game(self) -> Task:
      return Task(
          config=self.tasks_config["test_and_debug_game"],
      )
    


    @crew
    def crew(self) -> Crew:
        """Creates the GameVersionV1 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
