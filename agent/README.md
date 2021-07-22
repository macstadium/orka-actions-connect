# Configure your macOS agent image

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
15. Pass this new image file name in your GitHub Actions workflow in the `spin_up` job. 
