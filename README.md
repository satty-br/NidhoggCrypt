# NidhoggCrypt Readme

NidhoggCrypt is a powerful and secure http remote reverse shell project inspired by the legendary creature from Norse mythology, Nidhogg. The project focuses on enabling encrypted file downloads through HTTP transmission, ensuring data privacy and protection during transfer.

## Explain


```
                    +----------------+                 +---------+
+---------+         |                |                 |         |
| Python  | Console |                |       +---------+   HTTP  |
| Console +-------->+   Reverse      |       |         |  Client |
|         |         |    server      |       |         |         |
+---------+         |    Python      |       |         +---------+
                    |                |       |
                    |                |       |         +---------+ 
                    |                |  HTTP |         |         |
                    |                +<------+---------+  HTTP   |
+---------+         |                |       |         |  Client |
|         |         |                |       |         |         |
| HTTP    |   HTTP  |                |       |         +---------+
| API     +-------->+                |       |         
|         |         |                |       |
+---------+         |                |       |
                    +----------------+       |         +---------+
                                             |         |         |
                                             |         |   HTTP  |
                                             +---------+  Client |
                                                       |         |
                                                       +---------+

```






## Features:

Remote Reverse Shell: NidhoggCrypt provides a fully functional reverse shell that allows remote access to a target system.

Encryption: The project incorporates strong encryption algorithms to secure files before transmission, safeguarding sensitive data from unauthorized access.

Norse Mythology Theme: NidhoggCrypt draws inspiration from Norse mythology, with its name paying homage to the malicious dragon or serpent, Nidhogg, known for its destructive nature.

HTTP File Downloads: Users can download files via HTTP using URLs, making the process simple and accessible.

## How It Works:

Install NidhoggCrypt on both the host and target systems.

Establish a connection between the host and the target by initiating the reverse shell.

Users can then send URLs containing files they wish to download securely.

NidhoggCrypt encrypts the requested files before transferring them via HTTP to the target system.

## Installation:

clone repo 

Usage:

Launch the ngc.ppy reverse shell server, you can interact via console or endpoint.

Launch the cli_ngc.py in target system.

Security Considerations:

NidhoggCrypt employs state-of-the-art encryption techniques to ensure the confidentiality of transmitted files. However, it is recommended to use the tool responsibly and adhere to all applicable laws and ethical guidelines.
Disclaimer:

NidhoggCrypt is an open-source project provided as-is, without any warranty or guarantee of its performance or security. The developers are not responsible for any misuse or damage caused by the use of this tool.

Contributing:
We welcome contributions from the open-source community to enhance and improve NidhoggCrypt. Please refer to the contribution guidelines in the repository for more information.

License:
NidhoggCrypt is licensed under the MIT license. Refer to the LICENSE file for more details.

Contact:
For any questions, feedback, or support, please contact us at satty@satty.com.br.
Thank you for using NidhoggCrypt! 
