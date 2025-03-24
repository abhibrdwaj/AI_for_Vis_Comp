from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class GameVersionV1():
    """GameVersionV1 crew for HTML game development and testing"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def game_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['game_developer'],
            verbose=True
        )

    @agent
    def game_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['game_tester'],
            verbose=True
        )

    @task
    def game_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['game_creation_task'],
        )

    @task
    def game_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['game_testing_task'],
        )
    
    @agent
    def asset_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['asset_creator'],
            verbose=True
        )

    @agent
    def asset_integrator(self) -> Agent:
        return Agent(
        config=self.agents_config['asset_integrator'],
        verbose=True
        )

    @task
    def asset_creation_task(self) -> Task:
        return Task(
        config=self.tasks_config['asset_creation_task'],
        )

    @task
    def asset_integration_task(self) -> Task:
        return Task(
        config=self.tasks_config['asset_integration_task'],
    )


    @crew
    def crew(self) -> Crew:
        """Creates the GameVersionV1 crew with game dev and testing only"""
        return Crew(
            agents=[
                self.game_developer(),
                self.game_tester(),
                self.asset_creator(),
                self.asset_integrator()
                ],
            tasks=[
                self.game_creation_task(),
                self.asset_creation_task(),
                self.asset_integration_task(),
                self.game_testing_task()
                ],

            process=Process.sequential,
            verbose=True,
        )
