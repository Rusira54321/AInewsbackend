from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool,ScrapeWebsiteTool, FileWriterTool
from dotenv import load_dotenv
from .tools.custom_tool import PDFWriterTool
load_dotenv()

search_tool = SerperDevTool()
scraper_tool = ScrapeWebsiteTool()
file_writer = PDFWriterTool()
@CrewBase
class AiProject1():
    """AiProject1 crew"""

    agents_config: 'config/agents.yaml'
    tasks_config: 'config/tasks.yaml'

    @agent
    def search_news(self) -> Agent:
        return Agent(
            config=self.agents_config['search_news'],
            tools=[search_tool], # type: ignore[index]
            verbose=True
        )

    @agent
    def scraper_news(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper_news'],
            tools=[scraper_tool], # type: ignore[index]
            verbose=True
        )
    @agent
    def ai_news_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_news_writer'],
            tools=[], # type: ignore[index]
            verbose=True
        )

    @agent
    def file_Writer(self) -> Agent:
        return Agent(
            config=self.agents_config['file_Writer'],
            tools=[file_writer], # type: ignore[index]
            verbose=True
        )
    
    @task
    def search_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_news_task'], # type: ignore[index]
        )

    @task
    def scraper_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraper_task'], # type: ignore[index]
        )

    @task
    def ai_newsWriter_task(self) -> Task:
        return Task(
            config=self.tasks_config['ai_newsWriter_task'], # type: ignore[index]
        )

    @task
    def file_write_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_write_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiProject1 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
