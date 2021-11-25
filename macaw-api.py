from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pydantic import BaseModel
import requests
from loguru import logger
import re
import sys
import json

logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
logger.add(sys.stderr, format="{time} {level} {message}", filter="macaw", level="INFO")

# --------------------------> HuggingFace API <--------------------------------------
API_URL = "https://api-inference.huggingface.co/models/allenai/macaw-large"
headers = {"Authorization": "Bearer "}

class Message(BaseModel):
	input: str
	output: str= None

# =============================================================================
# MACAW API ----> 
# =============================================================================

# huggingface hub macaw-large request
def query(payload):
	"""querying macaw model in huggingface hub """
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# regex cleaner
def regex_function(variable):
	""" Regex for cleaning answer """ls
	regex = r"\=(.+?)\;(.*)\$explanation\$(.*)\=(.*)"
	matches = re.findall(regex, variable)
	matches = matches[0]
	matches = [str(i.strip(' ')) for i in matches if matches]
	matches= list(filter(None, matches))
	result = {"answer": matches[0], "explanation": matches[1]}
	return result

# question
@logger.catch
def query_macaw(message: Message):
	print("message.input: ", message)
	msg = message['input']
	msg= f'"$answer$; $explanation$; $question$ = {msg}?"'
	#print("msg", msg)
	try:
		result = query([msg])
		print("result ", result)
	except Exception as e:
		logger.exception("query_macaw: ", e)
	
	if result:
		message['output'] = regex_function(result[0]['generated_text'])
		#return {"output" : message.output}
		return message['output']
	
	
#a = {"input": "Which force pulls objects to the ground", "output": ""}
#print(query_macaw(a))


