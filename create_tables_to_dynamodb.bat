@echo off

rem create tables
aws dynamodb create-table --cli-input-json file://tables/table_GourmetInfo.json
