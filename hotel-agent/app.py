import json


def get_named_parameter(event, name):
    return next(item for item in event["parameters"] if item["name"] == name)["value"]


def find_hotels(location):
    return_list = [
        {
            "name": "Courtyard Mariott",
            "number of reviews": "485",
            "Address": "123 Main St",
            "features": ["free cancellation", "complementary breakfast"],
            "Ratings": 4.5,
            "star": "3 star",
            "Phone": "202-324-2536",
        },
        {
            "providerType": "Sheraton",
            "number of reviews": "989",
            "Address": "423 Corporate Ct",
            "features": ["pool", "complementary breakfast", "free cancellation"],
            "Ratings": 5,
            "star": "4 star",
            "Phone": "243-324-2126",
        },
    ]
    return return_list


def lambda_handler(event, context):
    agent = event["agent"]
    actionGroup = event["actionGroup"]
    function = event["function"]
    parameters = event.get("parameters", [])
    session_id = event["sessionId"]

    responseBody = ""

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    if function in "getHotels":
        city = get_named_parameter(event, "city")
        responseBody = {"TEXT": {"body": json.dumps(find_hotels(city))}}
    elif function in "reserveHotel":
        hotel = get_named_parameter(event, "hotelname")
        ## Call a service to reserve the hotel and get a confirmation number. Return a default confirmation number for now.
        confirmation_number = "ABC123"  # Replace with actual confirmation number
        responseBody = {
            "TEXT": {
                "body": json.dumps(
                    {"success": True, "confirmation_number": confirmation_number}
                )
            }
        }
    else:
        responseBody = {"TEXT": {"body": json.dumps({"success": False})}}

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
