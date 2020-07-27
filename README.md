# Programming assignment – cell phone tariff

Your task is to create application for calculation of the monthly bill of mobile tariff. Individual calls and sent SMSs are in the data.csv file. This file contains following columns:
* **datetime** – date and time of the call / SMS
* **number** – phone number
* **duration** – the length of the call (for an empty SMS)
* **type** – VS (call within the same operator), VM (call to different operator), SS (SMS within the same operator), SM (SMS to different operator)

Parameters of the tariff are defined as follows:

| Parameter                                | Value                          |
|------------------------------------------|--------------------------------|
| Monthly fee                              | 900                            |
| Free minutes                             | 100                            |
| Numbers free of charge                   | +420732563345, +420707325673   |
| Fee for minute within operator‘s network | 1,50                           |
| Fee for minute out operator‘s network    | 3,50                           |
| Free SMSs                                | 10                             |
| Fee for SMSs within operator‘s network   | 1.00                           |
| Fee for SMSs out of operator‘s network   | 2.00                           |

First minute is always charged full, then by seconds.Result of your application should be following information:
* Whole charged sum (monthly fee, calls, SMSs)
* Number of airtime minutes within operator‘s network and their charged sum
* Number of sent SMSs within operator‘s network and their charged sum
* Number of airtime minutes out of operator‘s network and their charged sum
* Number of sent SMSs out of operator‘s network and their charged sum
