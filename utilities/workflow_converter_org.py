import argparse
import yaml

class WorkflowConverter:
	def __init__(self, args):
		self.workflow_path = args.workflow_path
		self.up = {'up': {'runs-on': 'ubuntu-latest', 'steps': [{'name': 'up', 'id': 'up', 'uses': 'jeff-vincent/orka-actions-up-org@1.0.0', 'with': {'orkaUser': '${{ secrets.ORKA_USER }}', 'orkaPass': '${{ secrets.ORKA_PASS }}', 'orkaBaseImage': 'gha-org-agent.img', 'githubPat': '${{ secrets.GH_PAT }}', 'githubOrg': 'example-org-1', 'vpnUser': '${{ secrets.VPN_USER }}', 'vpnPassword': '${{ secrets.VPN_PASSWORD }}', 'vpnAddress': '${{ secrets.VPN_ADDRESS }}', 'vpnServerCert': '${{ secrets.VPN_SERVER_CERT }}', 'vcpuCount': 3, 'coreCount': 3}}], 'outputs': {'vm-name': '${{ steps.up.outputs.vm-name }}'}}}
		self.down = {'down': {'if': 'always()', 'needs': ['up'], 'runs-on': 'ubuntu-latest', 'steps': [{'name': 'down', 'id': 'down', 'uses': 'jeff-vincent/orka-actions-down-org@1.0.0', 'with': {'orkaUser': '${{ secrets.ORKA_USER }}', 'orkaPass': '${{ secrets.ORKA_PASS }}', 'githubPat': '${{ secrets.GH_PAT }}', 'githubOrg': 'example-org-1', 'vpnUser': '${{ secrets.VPN_USER }}', 'vpnPassword': '${{ secrets.VPN_PASSWORD }}', 'vpnAddress': '${{ secrets.VPN_ADDRESS }}', 'vpnServerCert': '${{ secrets.VPN_SERVER_CERT }}', 'vmName': '${{ needs.job1.outputs.vm-name }}'}}]}}
		self.jobs_list = []
		self.data = None
		self.jobs_list.append(self.up)

	def parse_yaml(self):
		with open(self.workflow_path) as f:
			self.data = yaml.load(f, Loader=yaml.FullLoader)

		for key, value in self.data['jobs'].items():
			single_job = {key:value}
			single_job[key]['runs-on'] = ["self-hosted", "${{ needs.up.outputs.vm-name }}"]
			single_job[key]['needs'] = ["up"]
			self.jobs_list.append(single_job)
			self.down['down']['needs'].append(key)
		self.jobs_list.append(self.down)

	def assemble_yaml(self):
		for i in self.jobs_list:
			key = list(i)[0]
			self.data['jobs'][key] = i[key]

		with open('temp.yml', 'w+') as f:
			f.write(yaml.dump(self.data))
    
	def clean_yaml(self):
		with open('temp.yml', 'r') as f:
			with open('new_yaml.yml', 'a') as output:
				for line in f:
					if 'true:' in line:
						line = 'on:\n'

					if '${{ needs.up.outputs.vm-name }}' in line:
						line = '    - "${{ needs.up.outputs.vm-name }}"\n'
					output.write(line)


def main(args):
	converter = WorkflowConverter(args)
	converter.parse_yaml()
	converter.assemble_yaml()
	converter.clean_yaml()

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--filepath', help='list deployed VMs', action='store', dest='workflow_path')
	return parser.parse_args()

if __name__ == "__main__":
	args = parse_args()
	main(args)
