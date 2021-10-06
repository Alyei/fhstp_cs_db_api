import sys
import boto3
import os
import simplejson
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('Items')

def getAllItems():
    try:
        result = table.scan()
    except Exception as e:
        print(e)
        return str(e)

    return simplejson.dumps(result["Items"])

def getItemsByID(itemids):
    result = []
    for item in itemids:
        try:
            row = table.query(KeyConditionExpression=Key('item').eq(item))
            result.append(row["Items"])
        except Exception as e:
            print(e)
            return str(e)

    return simplejson.dumps(result)

    
def getAmountOfItem(itemid):
    try:
        result = table.query(KeyConditionExpression=Key('item').eq(itemid))
    except Exception as e:
        print(e)
        return str(e)

    return simplejson.dumps(result['Items'])

def removeItems(itemsToRemove):
    responses=[]

    for itemid in itemsToRemove.keys():
        amount = int(itemsToRemove[itemid])

        try:
            res = table.update_item(
                    Key={
                        'item': itemid
                        },
                    UpdateExpression="SET #ct = #ct - :c",
                    ConditionExpression="#ct >= :c",
                    ExpressionAttributeValues={
                        ':c': amount
                        },
                    ReturnValues="UPDATED_NEW",
                    ExpressionAttributeNames={
                        '#ct': 'count'
                        }
                    )

            responses.append({itemid: res['Attributes']['count']})

        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException as f:
            responses.append({itemid: 'n'})
        except Exception as e:
            #Can be trouble if first items work but later ones don't.
            print(str())
            return str(e)

    return simplejson.dumps(responses)
