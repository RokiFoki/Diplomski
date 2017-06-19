import pymssql
import codecs
import time
import argparse
import os
from utils import get_file_name_from_dates
from datetime import datetime

IP = str("161.53.18.12")+":"+str(1955)
username = 'roko'
password = 'g546z6rhtf'
DBname = "ExperientialSamplingAnalyticsDev2"

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()  

query = """
	SELECT ContextualInfo.Time, [User].Name, LogEvent.EventName, LogEvent.EventType, CONVERT(NVARCHAR(MAX), LogEvent.JSONparams) 
	FROM LogEvent 
	JOIN ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
	JOIN [User] ON ContextualInfo.UserId = [User].Id
	WHERE ContextualInfo.Time BETWEEN '12/7/2016' and '12/7/2016 23:59:59'
"""

print(query)

cursor.execute(query)
for row in cursor:
	print(row)