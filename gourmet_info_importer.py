# -*- coding: utf-8 -*-

import csv
import json

import boto3

with open('gourmet_info_list_db.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('GourmetInfo')
        table.put_item(
            Item={
                "name": row[0],
                "yomi": row[1],
                "prefecture": row[2],
                "detail": row[3]
            }
        )

    
