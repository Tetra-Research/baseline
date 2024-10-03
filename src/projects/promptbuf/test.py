import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from baseline import Data, Evaluation, Evaluator, Outcome
from projects.promptbuf.lib_cpy import decode

load_dotenv()


introductions = [
    "My name is Sarah Martinez, and I'm 28 years old. By day, I work as a Marketing Manager, handling everything from campaign strategies to content creation. By night, I’m working towards my MBA, hoping it’ll open more doors for leadership roles in my company. Honestly, balancing work and school can be tough, but I enjoy staying busy. When I have downtime, I love painting—mostly landscapes—and hiking with my dog, Luna. It’s my way of recharging after long workdays.",
    "Hey, I’m David Chen, and I’m 32. I’m a Software Engineer and spend most of my time solving complex problems for my company’s backend systems. I’m doing a Master’s in Data Science because I want to dive deeper into machine learning and AI. Outside of work and class, I’m really into photography. On weekends, you’ll usually find me out in nature, trying to capture the perfect shot at sunrise. It’s my creative outlet, especially when coding starts to get a bit too technical.",
    "Hi, I’m Amelia Johnson, 26, and I’m currently a stay at home mom. My goal is to complete my Master’s in Communication so I can eventually move into a leadership role, maybe even start my own PR agency one day. I’m really into fitness, so when I’m not in class, I’m usually hitting the gym or doing Pilates. I also love cooking, and I’m always trying new recipes—I’m kind of obsessed with Italian food right now.",
    "I’m Marcus O’Neill, and I’m 35. By day, I work as a Project Manager in the tech industry, and by night, I’m a graduate student pursuing my Master’s in Organizational Leadership. I’m hoping it’ll give me the skills to move into a director-level role soon. Outside of all the hustle, I’m a huge sports fan. I play in a local soccer league, and watching games—especially Premier League—is how I unwind. I also dabble in woodworking, believe it or not, and I find it super relaxing.",
    "Hey, I’m Jasmine Patel, 29, and I work as a Financial Analyst during the day. I’m getting my Master’s in Finance because I want to specialize in investment strategies and maybe even start my own advisory firm someday. Outside of work and school, I’m an avid reader—thrillers and mysteries are my favorite genres. I also enjoy traveling, and I try to take at least one big trip each year. Exploring new cultures and food is a huge passion of mine, and it helps me recharge between semesters.",
]


class ValidJSON(Evaluator):
    property = "valid_json"

    def eval(self, outcome: Outcome):
        try:
            json.loads(json.dumps(outcome.value))
            outcome.properties.append(self.property)
        except Exception as e:
            print("exception", e)
            return


def prompt(content: str) -> str:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                Below is a user written summary.  
                
                Extract the following details:
                - name, in quotes
                - age, integer
                - isEmployed, boolean, as 1 or 0

                In this space-delimited, minified JSON format: 
                {name age isEmployed}
                """,
            },
            {"role": "user", "content": content},
        ],
        model="gpt-4o",
    )

    return decode(
        v=chat_completion.choices[0].message.content,
        s={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "isEmployed": {"type": "boolean"},
            },
        },
    )


def run():
    dataset = [Data(value=intro, properties=["easy"]) for intro in introductions]

    evaluators = [ValidJSON()]

    evaluation = Evaluation(
        dataset=dataset, callback=prompt, evaluators=evaluators, num_simulation_runs=1
    )

    evaluation.run()

    for result in evaluation.results:
        print("valid_json" in result.outcome.properties)
