import json
import boto3
import os

weather_agentId = os.getenv("WEATHER_AGENT_ID")
hotel_agentId = os.getenv("HOTEL_AGENT_ID")
bedrock_agent_client = boto3.client("bedrock-agent")
bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime")


def get_named_parameter(event, name):
    return next(item for item in event["parameters"] if item["name"] == name)["value"]


def invoke_agent(agentId, alias_id, prompt, sessionId):
    response = bedrock_agent_runtime_client.invoke_agent(
        agentId=agentId,
        agentAliasId=alias_id,
        sessionId=sessionId,
        inputText=prompt,
    )

    completion = ""

    for event in response.get("completion"):
        chunk = event["chunk"]
        completion += chunk["bytes"].decode()

    return completion


def lambda_handler(event, context):
    agent = event["agent"]
    actionGroup = event["actionGroup"]
    function = event["function"]
    print(agent, actionGroup, function)
    parameters = event.get("parameters", [])
    session_id = event["sessionId"]
    print(parameters)

    prompt = get_named_parameter(event, "prompt")

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    if function in "askForWeather":
        response = invoke_agent(weather_agentId, "TSTALIASID", prompt, session_id)
    elif function in "listHotels":
        response = invoke_agent(hotel_agentId, "TSTALIASID", prompt, session_id)
    elif function in "reserveHotel":
        response = invoke_agent(hotel_agentId, "TSTALIASID", prompt, session_id)

    print(response)

    responseBody = {"TEXT": {"body": str(response)}}

    action_response = {
        "actionGroup": actionGroup,
        "function": function,
        "functionResponse": {"responseBody": responseBody},
    }

    function_response = {
        "response": action_response,
        "messageVersion": event["messageVersion"],
    }
    print("Response: {}".format(function_response))

    return function_response
