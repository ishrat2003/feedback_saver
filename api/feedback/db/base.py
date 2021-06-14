import os, re
import boto3
import uuid
from datetime import datetime
import socket
import json
from botocore.exceptions import ClientError

class Base:

    def __init__(self):
        self.endPointUrl = os.environ['DYNAMODB_ENDPOINT']
        if os.environ['ENVIRONMENT_NAME'] == 'local':
            self.endPointUrl = os.environ['DEFAULT_DYNAMODB_ENDPOINT']

        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endPointUrl)
        self.errors = []
        self.commonArrtibutes = [
            'id',
            'created',
            'environment',
            'key',
            'condition',
            'user_code',
            'gender',
            'age_group',
            'experiment_date_datepicker',
            'agreed',
            'level',
            'department',
            'disability',
            'open_timestamp',
            'open_date_time',
            'close_timestamp',
            'close_date_time',
            'time_taken_in_seconds',
            'summary',
            'ease'
        ]
        return
    
    def save(self, data):
        validData = self.getBind(data)
        print(validData)
        if len(self.errors):
            return { 'errors': '<br>'.join(self.errors) }
            
        if self.get(data):
            return self.update(validData)
        
        return self.create(validData)

    def get(self, data):
        response = {}
        table = self.dynamodb.Table(self.tableName)
        
        for key in self.keyAttributes:
            if key not in data.keys():
                return None

        try:
            query = {}
            expression = ''
            joiner = ''
            for key in self.keyAttributes:
                expression += joiner + key + ' = :' + key
                joiner = ' and '
                query[':' + key] = data[key]
            response = table.scan(
                FilterExpression = expression,
                ExpressionAttributeValues = query
            )
            if response['Items'] and len(response['Items']):
                return response['Items'][0]['id']
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
          
        return None
        
    def create(self, data): 
        table = self.dynamodb.Table(self.tableName)
        response = {}
        try:
            response = table.put_item(Item = data)
        except ClientError as e:
            return {'errors': 'Failed to CREATE details.' + e.response['Error']['Message']}
    
        return {'message': 'Record saved successfully.'}

    def update(self, validData):
        table = self.dynamodb.Table(self.tableName)
        keys = {}
        for key in self.keyAttributes:
            keys[key] = validData[key]
            del validData[key]
        
        expression = 'SET ';
        expressionAttributes = {}
        divider = '';
        for key in validData.keys():
            expressionAttributes[':' + key] = validData[key]
            expression += divider + key + ' = :' + key
            divider = ', '
        try:
            response = table.update_item(
                Key = keys,
                UpdateExpression = expression,
                ExpressionAttributeValues = expressionAttributes,
                ReturnValues = 'ALL_NEW'
            )
            print(response)
            if response: 
                return {'message': 'Record UPDATED successfully.'}
        except Exception as e:
            print(e)
            print(e.response['Error']['Message'])
            return {'errors': e.response['Error']['Message']}
          
        return {'errors': 'Failed to UPDATE details.'}
        
    def clean(self, text):
        text = re.sub(r"'", '', text)
        return text
    
    def getBind(self, data = {}):
        self.errors = []
        validData = {}
        now = datetime.now()
        validData['id'] = str(uuid.uuid4())
        validData['created'] = str(now.strftime("%d/%m/%Y %H:%M:%S"))
        validData['environment'] = str(os.environ['ENVIRONMENT_NAME'])
        
        for attribute in self.attributes:
            if (attribute in ['id', 'created', 'environment']):
                continue
            
            if (attribute not in data.keys()) or not data[attribute]:
                self._checkError(attribute, data)
            else:
                print(attribute, '--', data[attribute], "\n")
                if attribute in self.keyAttributes:
                    validData[attribute] = str(data[attribute])
                else:
                    keyAttribute = 'task_' + attribute  if attribute in ['key', 'condition', 'level'] else attribute
                    validData[keyAttribute] = str(data[attribute])

        return validData
    
    def _checkError(self, attribute, data):
        return
        
