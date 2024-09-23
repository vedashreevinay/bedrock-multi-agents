import json


def return_weather(city):
    return {"max temperature": 90, "min temperature": 79, "rainfall": 80}


def get_named_parameter(event, name):
    return next(item for item in event["parameters"] if item["name"] == name)["value"]


def lambda_handler(event, context):
    agent = event["agent"]
    actionGroup = event["actionGroup"]
    function = event["function"]
    parameters = event.get("parameters", [])
    session_id = event["sessionId"]

    city = get_named_parameter(event, "city")

    weather = return_weather(city)
    print(weather)

    # weather= invoke_weather_agent(weather_agent_id, weather_agent_alias, prompt, sessionId )

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html

    responseBody = {"TEXT": {"body": json.dumps(weather)}}

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
