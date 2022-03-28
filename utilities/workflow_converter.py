import argparse
import yaml

class WorkflowConverter:
	def __init__(self, args):
		self.workflow_path = args.workflow_path
		self.up = {'spin-up': {'runs-on': 'ubuntu-latest', 'steps': [{'name': 'spin-up', 'id': 'spin-up', 'uses': 'jeff-vincent/orka-actions-up@v1.1.1', 'with': {'orkaUser': '${{ secrets.ORKA_USER }}', 'orkaPass': '${{ secrets.ORKA_PASS }}', 'orkaBaseImage': 'gha-agent.img', 'githubPat': '${{ secrets.GH_PAT }}', 'vpnUser': '${{ secrets.VPN_USER }}', 'vpnPassword': '${{ secrets.VPN_PASSWORD }}', 'vpnAddress': '${{ secrets.VPN_ADDRESS }}', 'vpnServerCert': '${{ secrets.VPN_SERVER_CERT }}', 'vcpuCount': 6, 'coreCount': 6}}], 'outputs': {'vm-name': '${{ steps.job1.outputs.vm-name }}'}}}
		self.down = {'tear-down': {'if': 'always()', 'needs': ['spin-up'], 'runs-on': 'ubuntu-latest', 'steps': [{'name': 'tear-down', 'id': 'tear-down', 'uses': 'jeff-vincent/orka-actions-down@v1.1.0', 'with': {'orkaUser': '${{ secrets.ORKA_USER }}', 'orkaPass': '${{ secrets.ORKA_PASS }}', 'githubPat': '${{ secrets.GH_PAT }}', 'vpnUser': '${{ secrets.VPN_USER }}', 'vpnPassword': '${{ secrets.VPN_PASSWORD }}', 'vpnAddress': '${{ secrets.VPN_ADDRESS }}', 'vpnServerCert': '${{ secrets.VPN_SERVER_CERT }}', 'vmName': '${{ needs.job1.outputs.vm-name }}'}}]}}
		self.jobs_list = []
		self.data = None
		self.jobs_list.append(self.up)

	def parse_yaml(self):
		with open(self.workflow_path) as f:
			self.data = yaml.load(f, Loader=yaml.FullLoader)

		for key, value in self.data['jobs'].items():
			single_job = {key:value}
			single_job[key]['runs-on'] = ["self-hosted", "${{ needs.spin-up.outputs.vm-name }}"]
			single_job[key]['needs'] = ["spin-up"]
			self.jobs_list.append(single_job)
			self.down['tear-down']['needs'].append(key)
		self.jobs_list.append(self.down)

	def assemble_yaml(self):
		for i in self.jobs_list:
			key = list(i)[0]
			self.data['jobs'][key] = i[key]

		with open('new_yaml.yml', 'w+') as f:
			f.write(yaml.dump(self.data))


def main(args):
	converter = WorkflowConverter(args)
	converter.parse_yaml()
	converter.assemble_yaml()

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--filepath', help='list deployed VMs', action='store', dest='workflow_path')
	return parser.parse_args()

if __name__ == "__main__":
	args = parse_args()
	main(args)
