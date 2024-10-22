from openai import OpenAI
client = OpenAI()

alice = client.beta.assistants.create(
    instructions="You are enthusiastic to propose your movie ideas regarding a bear society in the meeting. You propose a pollitical Thriller, where the bears are trying to overturn a rulling that segregated hibernators from nonhibernators.",
    name="alice",
    model="gpt-3.5-turbo",
)

bob = client.beta.assistants.create(
    instructions="You just arrived to the meeting room late. The meeting is about the bear society movie porject. You want to propose a summer blockbuster war film about factions of bears overturning the oppressive rulling class of the forest. Alice begins talking to you about her ideas for the project.",
    name="Math Tutor",
    model="gpt-3.5-turbo",
)

empty_thread = client.beta.threads.create()

thread_message = client.beta.threads.messages.create(
  empty_thread.id,
  role="user",
  content="You just got into the meeting room, and see bob unpacking their things.",
)

print(thread_message.role+": "+thread_message.content[0].text.value)