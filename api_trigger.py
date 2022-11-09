import jenkins
import time
import json
import os
import argparse
import sys
os.environ.setdefault("PYTHONHTTPSVERIFY", "0")

# URL = "https://cbjenkins-fm.devtools.intel.com/teams-dcai-dpea-paiv/"
QUEUE_POLL_INTERVAL = 2
JOB_POLL_INTERVAL = 20
OVERALL_TIMEOUT = 3600

def setup_argparse():
	args = sys.argv[1:]
	parser = argparse.ArgumentParser(
		description='add the only folder under the path to the system environment variable'
					'--user <Username for jenkins>'
					'--pass <paaword or API token>'
					'--url <jenkins URL>'
					'--job_name <Pipeline name>'
					'--token <Token name>')
	parser.add_argument("--user", '-u', dest='USERNAME', help="Enter jenkins Username", default=os.environ.get("USERNAME"))
	parser.add_argument("--pass", '-p', dest='PASSWORD', help="Enter either paaword or API token", required=True)
	parser.add_argument("--url", dest='URL', help="Enter jenkins URL", required=True)
	parser.add_argument("--job_name", dest='NAME_OF_JOB', help="Enter pipeline name", required=True)
	parser.add_argument("--token", dest='TOKEN_NAME', help="Enter token name", required=True)
	parser.add_argument("--parameters", dest='PARAMETERS', help="Enter paramters")
	ret = parser.parse_args(args)
	return ret

class DevOpsJenkins:
	def __init__(self, name, token=None):
		self.server = jenkins.Jenkins(args.URL, username=args.USERNAME, password=args.PASSWORD)
		self.name = name
		self.token = token

	def build_job(self, params=None):
		next_build_number = self.server.get_job_info(self.name)['nextBuildNumber']
		params['token'] = self.token
		self.server.build_job(self.name, parameters=params)
		queue_info  = self.server.get_queue_info()
		id = queue_info[0].get('id')
		while True:				# wait till job come out of queue and start building
			time.sleep(QUEUE_POLL_INTERVAL)
			item = self.server.get_queue_item(id)
			if item['why'] == 'Finished waiting' or item['why'] == 'None':
				break
		print("JOB is building...")
		time.sleep(5)
		start_epoch = int(time.time())
		while True:				#wait till job ends
			build_info = self.server.get_build_info(self.name, next_build_number)
			if (build_info['result'] == 'SUCCESS') or (build_info['result'] == 'FAILURE') or (build_info['result'] == 'ABORTED'):
				break
			else:
				print("{}: Job: {} Status: {}. Polling again in {} secs".format(
						time.ctime(), self.name, build_info['result'], JOB_POLL_INTERVAL))
				time.sleep(JOB_POLL_INTERVAL)
			cur_epoch = int(time.time())
			if (cur_epoch - start_epoch) > OVERALL_TIMEOUT:
				print("{}: No status before timeout".format(OVERALL_TIMEOUT))
				return 0
		return build_info

if __name__ == "__main__":
	args = setup_argparse()
	jenkins_obj = DevOpsJenkins(args.NAME_OF_JOB, args.TOKEN_NAME)
	output = jenkins_obj.build_job(json.loads(args.PARAMETERS))
	print ("Jenkins Build URL: {}".format(output['url']))
	print ("Jenkins Build result: {}".format(output['result']))
