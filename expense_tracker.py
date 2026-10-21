import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM


load_dotenv()


groq_llm = LLM(
    model="openai/openai/gpt-oss-120b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    custom_openai=True
)



parser = Agent(
    role="Expense Parser",
    goal="Extract amount and description from free text",
    backstory="You are meticulous about numbers.",
    verbose=True,
    llm=groq_llm
)

categorizer = Agent(
    role="Expense Categorizer",
    goal="Assign one category per item",
    backstory="Only use these categories: Food, Transport, Shopping, Bills, Other.",
    verbose=True,
    llm=groq_llm
)

reporter = Agent(
    role="Spending Reporter",
    goal="Summarize totals by category",
    backstory="You write short, clear summaries.",
    verbose=True,
    llm=groq_llm
)

parse_task = Task(
    description="Parse this input into items with amount and description: 'I spent 45 on lunch and 120 on groceries today'. Return only a JSON list.",
    expected_output="A JSON list of items, each with 'amount' and 'description'.",
    agent=parser,
)

categorize_task = Task(
    description="Take the parsed items from the previous task and assign each one a category. Return only JSON.",
    expected_output="A JSON list of items with 'amount', 'description', and 'category'.",
    agent=categorizer,
)

report_task = Task(
    description="Take the categorized items from the previous task and write a short spending summary.",
    expected_output="A short text summary with totals per category.",
    agent=reporter,
)

crew = Crew(
    agents=[parser, categorizer, reporter],
    tasks=[parse_task, categorize_task, report_task],
    verbose=True,
)

result = crew.kickoff()
print(result)