# pyCheckMyInternet

Checks for the state of your internet connection every 5 minutes. 
For that we assume:

* You are behind a router (```192.168.0.1```).
* The primary DNS of your router is provided by your ISP

A test can yield 3 possible results:

  Sign     | Description 
-----------|-----------------------
```GOOD``` | Your internet connection is fine
```DNS```  | Your internet connection is up, but your ISP DNS is not responding. Changing the DNS on your devices will help you.
```DEAD``` | Your internet connection is down.


## Usage

Run this program in the background. 
If the state of your internet connction changes, an entry in ```internet.log``` will be created.
In this file, you will see the current state, the last state, and the duration of the last state.



