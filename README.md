# orka-actions-connect

Run native GitHub Actions jobs ephemerally on MacStadium's Orka.  

When your iOS and macOS minutes on GitHub Actions get to be too cost intensive, consider using this adaptor to run your existing GitHub Actions workflow on single use macOS VMs in MacStadium's Orka. 

## Overview

This system relies on two Actions -- `jeff-vincent/orka-actions-spin-up@master` and `jeff-vincent/orka-actions-tear-down@master`. You can see example usage of these in the `/workflow/example_workflow.yml` file.

These Actions run on GitHub Actions self-hosted runners tagged 'master'. These 'master' runners will be responsible for creating and destroying ephemeral macOS compute resources running in Orka. These 'masters' can be run in the K8s sandbox associated with Orka for HA, or in Docker, or directly on an adjacent Orka VM. 

The orka-spin-up and orka-tear-down Actions do what you'd expect, but the agent that they spin up also registers itself as a GitHub self-hosted runner tagged specifically for the given job it has been spun up for. A registration script pulls metadata from the VM that was set by the Action that spun it up, and then registers a self-hosted runner accordingly. In order to keep the flow synchronous, and thereby avoid the problem of no appropriately tagged runner being found, the orka-spin-up Action waits for the runner to register itself before it completes. 

The unique tag that has been applied to the newly minted runner is passed to the "native job" or your existing GitHub Actions job or series of jobs to be executed on macOS. These jobs are passed to the ephemeral Orka VM that was just spun up, and that will ultimately be torn down to restore compute resoures to the available pool, while also offering a fresh VM for every workflow execution.


## Prerequesites

- Set up an [Orka](https://orkadocs.macstadium.com/docs) Account

## Usage

There are three components to deploy to make this system work.

### Workflow

You will need to add 30+ lines to your existing GitHub Actions workflow definition. This will spin up a new macOS compute resource based on an image you've defined, pass your existing workflow to that new VM, and finally tear the VM down and remove the runner from GitHub.

### Master

You simply need one or more long-living GitHub Actions self-hosted runners tagged as 'master'. You can stand these up in Orka's K8s Sandbox for HA, or in Docker running on a sibling VM in Orka.

### Agent

You will need to create an Orka .img file based on your targeted OS. To do so, spin up an Orka VM based on your targed OS. Copy the files in the above `agent` directory onto the VM. Then, on the VM, open the Automator application, create an application that runs the `runner_connect.py` file that you just placed on the VM. Drop the resulting .app in login items for the default user, and enable auto-login for the default user. Save the VM image, and use this new image in your workflow file.
