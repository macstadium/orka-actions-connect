# orka-actions-connect

Orka-Actions-Connect will allow you to run your existing GitHub Actions workflow on single use macOS VMs in MacStadium's Orka. 

## Overview
Orka-Actions-Connect relies on two Actions -- `jeff-vincent/orka-actions-up@v1.0.1` and `jeff-vincent/orka-actions-down@v1.0.0`. These Actions are meant to run on `ubuntu-latest`. They are responsible for connecting to your Orka environment via VPN, spinning up a macOS VM, and ultimately tearing it down.

The resulting macOS compute resource registers itself as a GitHub self-hosted runner tagged specifically for the given job it has been spun up for. A registration script that has been added to the targeted `.img` file defined in Orka pulls metadata from the VM that was set by the Action that spun it up, and then registers a self-hosted runner accordingly. In order to keep the flow synchronous, and thereby avoid the problem of no appropriately tagged runner being found, the [Orka-Action-Up](https://github.com/jeff-vincent/orka-actions-up) Action waits for the runner to register itself before it completes. 

The unique tag that has been applied to the newly minted runner is passed to the "native job" or your existing GitHub Actions job or series of jobs to be executed on macOS. These jobs are passed to the ephemeral Orka VM that was just spun up, and that will ultimately be torn down to restore compute resoures to the available pool, while also offering a fresh VM for every workflow execution.


## Prerequesites

- Set up an [Orka](https://orkadocs.macstadium.com/docs) Account

## Configure your macOS agent image

1. [Spin up an Orka VM](https://orkadocs.macstadium.com/docs/quick-start#5-create-and-deploy-your-first-vm-instance)
2. Clone this repo down to the VM. 
3. Run the following:
```
cd orka-actions-connect/agent && ./setup.sh
```
4. Open the Automator App
5. Choose "Application"
6. In the following view, click "Utilities" in the leftmost menu and then double click "Run Shell Script".
7. Enter the following in the view:
```
python3 /Users/admin/agent/runner_connect.py
```
8. Save the application. 
9. Navigate to "System Preferences" > "Users & Groups". Select "Login Items" and then drag and drop your new application to add it to your login items for the selected user.
10. Click "Login Options" in this same view, and enable automatic login for your default user.
11. From your local machine via the Orka CLI, run:
```
orka image list
```
12. Collect the VM ID of the machine you've been working on.
13. Again from the CLI, run:
```
orka image save
```
14. Pass the ID you just collected and name the image with the suffix `.img`.
15. Pass this new image file name in your GitHub Actions workflow as your `orkaBaseImage`. 

## Example Workflow

```
on:
  push:
    branches:
      - main

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
    - name: Job 1
      id: job1
      uses: jeff-vincent/orka-actions-up@v1.0.1
      with:
        orkaIP: http://10.221.188.100
        orkaUser: ${{ secrets.ORKA_USER }}
        orkaPass: ${{ secrets.ORKA_PASS }}
        orkaBaseImage: gha_bigsur_v3.img
        githubUser: ${{ secrets.GH_USER }}
        githubPat: ${{ secrets.GH_PAT }}
        githubRepoName: orka-actions-up
        vpnUser: ${{ secrets.VPN_USER }}
        vpnPassword: ${{ secrets.VPN_PASSWORD }}
        vpnAddress: ${{ secrets.VPN_ADDRESS }}
        vpnServerCert: ${{ secrets.VPN_SERVER_CERT }}
    outputs:
      vm-name: ${{ steps.job1.outputs.vm-name }}
         
  job2:
    needs: job1
    runs-on: [self-hosted, "${{ needs.job1.outputs.vm-name }}"]
    steps:
    - name: Job 2
      id: job2
      run: |
        sw_vers
  job3:
    if: always()
    needs: [job1, job2]
    runs-on: ubuntu-latest
    steps:
    - name: Job 3
      id: job3
      uses: jeff-vincent/orka-actions-down@v1.0.0
      with:
        orkaIP: http://10.221.188.100
        orkaUser: ${{ secrets.ORKA_USER }}
        orkaPass: ${{ secrets.ORKA_PASS }}
        orkaBaseImage: gha_bigsur_v3.img
        githubUser: ${{ secrets.GH_USER }}
        githubPat: ${{ secrets.GH_PAT }}
        githubRepoName: orka-actions-up
        vpnUser: ${{ secrets.VPN_USER }}
        vpnPassword: ${{ secrets.VPN_PASSWORD }}
        vpnAddress: ${{ secrets.VPN_ADDRESS }}
        vpnServerCert: ${{ secrets.VPN_SERVER_CERT }}
        vmName: ${{ needs.job1.outputs.vm-name }}
```

## job2 example output

```
Run sw_vers
  sw_vers
  shell: /bin/bash -e {0}
ProductName:	macOS
ProductVersion:	11.3
BuildVersion:	20E232
```
