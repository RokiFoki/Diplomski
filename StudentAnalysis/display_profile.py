import time
import codecs
import glob
import numpy as np
from radar_graph import plot_chart_plot
from utils import get_value_from_file
import argparse
import os

parser = argparse.ArgumentParser(description="calculates and displays student profile")
parser.add_argument('names', metavar="name", help="name of the student", type=str, nargs="+")
parser.add_argument('-ip', help="IP address of the database", default="161.53.18.12", type=str)
parser.add_argument('-port', help="PORT of the database", default=1955, type=int)
parser.add_argument('-db', help="Database name", default="ExperientialSamplingAnalyticsDev2", type=str)
				
args = parser.parse_args()

names = args.names
ip = args.ip
port = args.port
db = args.db
username = get_value_from_file('config.txt', 'username')
password = get_value_from_file('config.txt', 'password')

types_from_indicator = {
	"collaborative" : "collaborative",	
	"AR" : "AR",
	"player" : "competitive"
}

type_indicators = {
	"collaborative" : "",	
	"AR" : "_AR",
	"competitive" : "_player"
}

type_sql_collumns = {
	"collaborative": "collaborative_score",
	"AR", "AR_score",
	"competitive": "competitive_score"
}

types = sorted(type_indicators.keys())

grades = []
for name in names:
	student_grades = []
	for type in types:
		file_name = "tmp/users/results/{}{}_real.txt".format(name, type_indicators[type])
		if os.path.isfile(file_name):
			with open(file_name, "r") as f:
				grade = np.mean(np.array([float(line.strip().split(":")[1]) for line in f.readlines()]))
		else:
			grade = 0

		student_grades.append(grade)

	grades.append(student_grades)


conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))

cursor = conn.cursor()  


query = """ 
DECLARE @user_id int
SELECT TOP 1 @user_id = Id from [User] where Name =  {6}

begin tran

	update UserTypeScores set {0}={3}, {1}={4}, {2}={5}
	where UserId = @user_id and [date] = '{7}'

	if @@rowcount = 0
	begin
		insert into UserTypeScores (UserId, {0}, {1}, {2}, [date])
		values (@user_id, {3}, {4}, {5}, '{7}')
	end

commit tran

""".format(*types, *grdes, name, "null")

print("executing query ({})".format(query))

cursor.execute(query)
print("query executed") 

plot_chart_plot(
	grades,
	types,
	['b', 'r', 'g', 'm', 'y'],
	names
)




