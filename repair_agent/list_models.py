from groq import Groq

from repair_agent.config import GROQ_API_KEY, check_config

check_config()
client = Groq(api_key=GROQ_API_KEY)

for model in sorted(client.models.list().data, key=lambda m: m.id):
    print(model.id)