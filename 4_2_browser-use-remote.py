import os
import pprint

import dotenv
from browser_use_sdk import BrowserUse

dotenv.load_dotenv()

client = BrowserUse(api_key=os.environ["BROWSER_USE_API_KEY"])

task = client.tasks.create_task(
    task="Forecast Bitcoin price for the next 6 months?",
    llm="browser-use-llm",
)

for step in task.stream():
    pprint.pprint(f"Step_{step.number}: {step}")
    print("====================")
