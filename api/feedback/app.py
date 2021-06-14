import json
from db.story import Story
from db.termsboard import Termsboard

def save_handler(event, context):
    eventData = json.loads(event['body']) if type(event) == str else event
    result = {}
    processor = None
    if 'feedback_type' in eventData.keys():
        if (eventData['feedback_type'] == 'story'):
            processor = Story()
        elif (eventData['feedback_type'] == 'termsboard'):
            processor = Termsboard()
    
    
    if (processor):
        result = processor.save(eventData)
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Request-Method': '*',
            'Access-Control-Request-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        "body": json.dumps({
            "result": result
        })
    }
