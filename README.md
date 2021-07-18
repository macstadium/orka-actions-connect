# orka-actions-connect

Run native GitHub Actions jobs ephemerally on MacStadium's Orka.  

Orka-Actions-Connect will allow you to run your existing GitHub Actions workflow on single use macOS VMs in MacStadium's Orka. 

## Overview
Orka-Actions-Connect relies on two Actions -- `jeff-vincent/orka-actions-spin-up@master` and `jeff-vincent/orka-actions-tear-down@master`. You can see example usage of these in the `/workflow/example_workflow.yml` file.

These Actions run on GitHub Actions self-hosted runners tagged 'master'. These 'master' runners are responsible for creating and destroying ephemeral macOS compute resources running in Orka. They can be run in the K8s sandbox associated with Orka for HA, or in Docker on an adjacent Orka VM. 

The resulting macOS compute resource registers itself as a GitHub self-hosted runner tagged specifically for the given job it has been spun up for. A registration script that has been [added to the targeted `.img` file defined in Orka] pulls metadata from the VM that was set by the Action that spun it up, and then registers a self-hosted runner accordingly. In order to keep the flow synchronous, and thereby avoid the problem of no appropriately tagged runner being found, the [Orka-Action-Spin-Up](https://github.com/jeff-vincent/orka-actions-spin-up) Action waits for the runner to register itself before it completes. 

The unique tag that has been applied to the newly minted runner is passed to the "native job" or your existing GitHub Actions job or series of jobs to be executed on macOS. These jobs are passed to the ephemeral Orka VM that was just spun up, and that will ultimately be torn down to restore compute resoures to the available pool, while also offering a fresh VM for every workflow execution.


## Prerequesites

- Set up an [Orka](https://orkadocs.macstadium.com/docs) Account

## Usage

There are three components to this system.

### Workflow

You will need to add ~30 lines to your existing GitHub Actions workflow definition. This will handle spinning up a new macOS compute resource based on an image you've defined, passing your existing workflow to that new VM, and finally tearing the VM down and removing the runner from GitHub.

>[View the workflow documentation](https://github.com/jeff-vincent/orka-actions-spin-up/blob/master/README.md)

### Master

You simply need one or more long-living GitHub Actions self-hosted runners tagged as 'master'. You can stand these up in Orka's K8s Sandbox for HA, or in Docker running on a sibling VM in Orka.

>[Example `docker run` command](https://github.com/jeff-vincent/orka-actions-connect/blob/main/master/start_master.sh)

>NOTE: you'll need to set a valid token (most likely generated from the GitHub UI).

### Agent

You will need to create an Orka `.img` file based on your targeted OS to act as a template for your dynamically generated macOS compute instances. 

>[View the agent documentation](#)

