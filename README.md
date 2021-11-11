# orka-actions-connect

Orka-Actions-Connect will allow you to run your existing GitHub Actions workflow on single use macOS VMs in MacStadium's Orka. 

## Overview
Orka-Actions-Connect relies on two Actions -- [`jeff-vincent/orka-actions-up@v1.0.1`](https://github.com/marketplace/actions/orka-actions-up) and [`jeff-vincent/orka-actions-down@v1.0.0`](https://github.com/marketplace/actions/orka-actions-down). These Actions are meant to run on `ubuntu-latest`. They are responsible for connecting to your Orka environment via VPN, spinning up a macOS VM, and ultimately tearing it down.

The resulting macOS VM in Orka registers itself as a GitHub self-hosted runner tagged specifically for the given workflow it has been spun up for. At this point, any number of `Jobs`, structured such as `job2` below, will be run on the ephemeral macOS instance. Regardless of the number of jobs run on the macOS VM, the final job must follow the structure of `Job3` in the example below.


## Prerequesites

- Set up an [Orka](https://orkadocs.macstadium.com/docs) Account

## Configure your macOS agent image

1. [Spin up an Orka VM](https://orkadocs.macstadium.com/docs/quick-start#5-create-and-deploy-your-first-vm-instance)
2. Clone this repo down to the VM. 
3. Run the following:
```
cd orka-actions-connect/agent && sudo ./setup.sh
```
4. From your local machine via the Orka CLI, run:
```
orka image list
```
5. Collect the VM ID of the machine you've been working on.
6. Again from the CLI, run:
```
orka image save
```
7. Pass the ID you just collected and name the image with the suffix `.img`.
8. Pass this new image file name in your GitHub Actions workflow as your `orkaBaseImage`. 

## Example Workflow

```
on:
  push:
    branches:
      - main

jobs:
  job1:
    runs-on: ubuntu-latest          # NOTE: both orka-actions-up and orka-actions-down run on `ubuntu-latest`
    steps:
    - name: Job 1
      id: job1
      uses: jeff-vincent/orka-actions-up@v1.0.1
      with:
        orkaIP: http://10.221.188.100
        orkaUser: ${{ secrets.ORKA_USER }}
        orkaPass: ${{ secrets.ORKA_PASS }}
        orkaBaseImage: gha_bigsur_v3.img             # NOTE: this `.img` file is the agent that has been defined in Orka
        githubUser: ${{ secrets.GH_USER }}           # All other Orka-related values can be found in your provided IP Plan
        githubPat: ${{ secrets.GH_PAT }}
        githubRepoName: orka-actions-up
        vpnUser: ${{ secrets.VPN_USER }}
        vpnPassword: ${{ secrets.VPN_PASSWORD }}
        vpnAddress: ${{ secrets.VPN_ADDRESS }}
        vpnServerCert: ${{ secrets.VPN_SERVER_CERT }}
    outputs:
      vm-name: ${{ steps.job1.outputs.vm-name }}
         
  job2:            # NOTE: this is where your macOS-based, GitHub Actions workflow will be executed.
    needs: job1     
    runs-on: [self-hosted, "${{ needs.job1.outputs.vm-name }}"]     # NOTE: this section of the workflow can contain any number of seperate jobs,
    steps:                                                          # but each must have this `runs-on` value.
    - name: Job 2
      id: job2
      run: |
        sw_vers
  job3:
    if: always()
    needs: [job1, job2]               # NOTE: all jobs you wish to run on the macOS instance, 
    runs-on: ubuntu-latest            # along with the `orka-actions-up` job, must be listed here.
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
