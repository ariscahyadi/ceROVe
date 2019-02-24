# ceROVe
Outsource ROV Feature at 2nd APNIC Hackathon
# Introduction
The project is to design an application which can be deployed on the network to handle RAOs instead of having the ROA on the router
And yes It is possible to make a simple program to outsource the ROV from the router as per the attached python code.
# Goal
No router software upgrade is required
- No downtime
- Support from the vendor for remote configuration

Valid/Invalid prefix matching in the network function
- It can be run in the x86 high-end server for large number of routes

Apply policy routing
- Common configuration for all router
- Avoid misconfiguration

# Data sets Used
- Data sets used on in this application are from APNIC(for the Valid Routes)
 http://data1.labs.apnic.net:8080/export
 - and Nusene(GItHub) for the Invalid routes.
 https://gist.github.com/nusenu/74e03bdbe9a2201dfd086f8fe9301300#file-2018-09-14-unreachable_invalids_prefix-origin-pairs-txt
 
# Setup
- Virtualbox - Ubuntu server
- MiniNet for the creating Topology and virtual routers
- Language - python v3 was used to read from parsh datas from json files.
# Conclusion
- It is possible to make a simple program to outsource the ROV from the router 
- With the application it is easier to query to many different Trust Anchor for different ROA’s state
As future work:
- Use online REST API call (if reliable)
- Push the config to the HW router/switch
