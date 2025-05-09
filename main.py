
import asyncio
import time
import warnings

from weather_agent import *
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.agents.run_config import RunConfig
from google.adk.artifacts import InMemoryArtifactService
from google.adk.cli.utils import logs
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.genai import types
import streamlit as st


load_dotenv()

warnings.filterwarnings('ignore', category=UserWarning)
logs.log_to_tmp_folder()


def main_sync():
  app_name = 'my_app'
  user_id_1 = 'user1'
  session_service = InMemorySessionService()
  artifact_service = InMemoryArtifactService()
  runner = Runner(
      app_name=app_name,
      agent=root_agent,
      artifact_service=artifact_service,
      session_service=session_service,
  )
  session_11 = session_service.create_session(
      app_name=app_name, user_id=user_id_1
  )

  def run_prompt(session: Session, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', content.model_dump(exclude_none=True))
    for event in runner.run(
        user_id=user_id_1,
        session_id=session.id,
        new_message=content,
    ):
      if event.content.parts and event.content.parts[0].text:
        print(f'** {event.author}: {event.content.parts[0].text}')
        return event.content.parts[0].text
    
    return "Something went wrong."
    
  st.title("Chat App")
  st.write("Interact with the chat agent below:")
  st.write("This is a weather AI agent by Google ADK. You can try with an sample question like 'What is the weather in New York?' or 'What is the current time in New York?'")

  user_input = st.text_input("You:", placeholder="Type your message here...")
  if st.button("Send"):
      if user_input.strip():
          response = run_prompt(session_11, user_input)
          st.write(f"Agent: {response}")
      else:
          st.warning("Please enter a message before sending.")


if __name__ == '__main__':
  print('--------------SYNC--------------------')
  main_sync()