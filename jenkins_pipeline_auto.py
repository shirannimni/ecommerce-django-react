import jenkins
import json
import os

#host = "http://localhost:8080"
host = "http://ec2-18-171-184-254.eu-west-2.compute.amazonaws.com"
username = "shirannimni"
password = "11d4c61136ea26ef90313480d55374b72c"

server = jenkins.Jenkins(host, username, password)

#test the api communication:
user = server.get_whoami()
version = server.get_version()

#print test:
print(f"Hello {user['fullName']} from jenkins {version}")

##jobs

#create empty job:
#server.create_job("job1", jenkins.EMPTY_CONFIG_XML)

#copy job1 to job2
#create a job and put it in a xml file

#job2_xml = open("job2.xml",mode="r", encoding="utf-8").read()
#server.create_job("job2", job2_xml)

#view jobs:
#jobs = server.get_jobs()
#print(jobs)

#get all jobs from the specific view:
#jobs = server.get_jobs(view_name='view name')
#print jobs

#get the job config:
#job1 = server.get_job_config('job1')
#print(job1)

#disable a job:
#server.disable_job('job1')

#enable disable job:
#server.enable_job('write your job name')

#delete a job:
#server.delete_job('write your job name1')
#server.delete_job('write your job name2')

#job_name = jobs[0]['name']
#server.build_job(job_name)
#job_number = server.get_job_info(job_name)['lastCompletedBuild']['number']

#print (job_number):
#print(f'job {job_name} has been started!')

#print(server.get_build_console_output(job_name, job_name))


#builds:

#build a parameterized job:
#requires creating and configuring the api-test job to accept 'param1' & 'param2'
#server.build_job('job1', {'param1': 'test value 1', 'param2': 'test value 2'})
#last_build_number = server.get_job_info('job1')['lastCompletedBuild']['number']


