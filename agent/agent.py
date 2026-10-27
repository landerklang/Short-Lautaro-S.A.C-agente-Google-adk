import os
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from agent.tools.tools import detect_language,count_characters,translate_text

root_agent = Agent(
    model=LiteLlm("ollama_chat/gemma4:31b-cloud"),
    name="root_agent",
    description="Agente traductor que traduce textos entre idiomas, detecta el idioma de origen y reporta la cantidad de caracteres.",
    instruction="""
    Eres un asistente que texto del usuario que este te pide y le responde con el texto traducido ademas de la estructura con la que este te enviaron es decir si la traduccion esta dentro de comillas dobles le devuelve la traduccion dentro de comilla doble. al inicio de la respuesta. utiliza la herramienta lenght. si el usuario te dice que no sabe de que idioma es ,utiliza la herramienta detection_Languaje. y para la traduccion utiliza la herramienta traductor.
    """,
    tools=[detect_language,count_characters,translate_text]
)