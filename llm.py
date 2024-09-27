import json
import ollama
import asyncio
import winsound

# Simulates an API call to get flight times
# In a real application, this would fetch data from a live database or API

def Beep(duration: int = 100) -> str:
    """Plays a sound"""
    winsound.Beep(2500, duration)
    return "The beep was played"

async def run(model: str):
  client = ollama.AsyncClient()
  # Initialize conversation with a user query
  messages = [{'role': 'user', 'content': 'Can you make 4 beeps of increaing duration from 100 milliseconds to 2 seconds'}]

  # First API call: Send the query and function description to the model
  response = await client.chat(
    model=model,
    messages=messages,
    tools=[
      {
        'type': 'function',
        'function': {
          'name': 'Beep',
          'description': 'Make a beep sound.',
          'parameters': {
            'type': 'object',
            'properties': {
              'duration': {
                'type': 'int',
                'description': 'Duration of the beep in milliseconds',
              },
            },
            'required': [],
          },
        },
      },
    ],
  )

  # Add the model's response to the conversation history
  messages.append(response['message'])

  # Check if the model decided to use the provided function
  if not response['message'].get('tool_calls'):
    print("The model didn't use the function. Its response was:")
    print(response['message']['content'])
    return

  # Process function calls made by the model
  if response['message'].get('tool_calls'):
    available_functions = {
      'Beep': Beep,
    }
    for tool in response['message']['tool_calls']:
      function_to_call = available_functions[tool['function']['name']]
      function_response = function_to_call(tool['function']['arguments']['duration'])
      # Add function response to the conversation
      messages.append(
        {
          'role': 'tool',
          'content': function_response,
        }
      )

  # Second API call: Get final response from the model
  final_response = await client.chat(model=model, messages=messages)
  print(final_response['message']['content'])


# Run the async function
asyncio.run(run('mistral'))