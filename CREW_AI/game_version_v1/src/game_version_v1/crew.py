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

    @crew
    def crew(self) -> Crew:
        """Creates the GameVersionV1 crew with game dev and testing only"""
        return Crew(
            agents=[
                self.game_developer(),
                self.game_tester()
            ],
            tasks=[
                self.game_creation_task(),
                self.game_testing_task()
            ],
            process=Process.sequential,
            verbose=True,
        )
