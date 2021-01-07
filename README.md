# Advanced_port_scanner
An application which displays the vulnerabilites of opened ports in a network on a particular operating system.

**WHY IS VULNERABILITY SCANNING IMPORTANT?**

Vulnerability scanning is an organized approach to the testing, identification analysis, and reporting potential security issues on a network. Every time a computer connects to the internet, there is a risk of a hacker taking advantage of some new vulnerability. So an external scan will mimic how hackers on the internet can attempt to gain access to a network. So once a scan is done, we get to know the system's external and internal vulnerabilities so we can take precautions to save our system from getting hacked.

First, I have understood how the Nessus tool works from there; I got an idea to create a vulnerability scanner. I have created a GUI application (vulnerability scanner). First, you have to enter the Target IP address and mention the starting and ending port address. After entering the target address, starting and ending ports and then pressing the scan button will show the opened ports between starting and ending ports. Below the scan, you have a vulnerability scan (button) that will search for the vulnerabilities in a database taken from NVD and displays them.
