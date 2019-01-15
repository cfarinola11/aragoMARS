# aragoMARS
Helpers for HIRO MARS 

LoadMARS.py
Requirements: python3 and pip3
OS: CentOS and RedHat
Modules: requests json glob re urllib3

Use this Python script to load MARS nodes to a HIRO 5.x instance. The source MARS nodes must be in JSON format. The script will ask whether you want to perform an update or a creation and proceed accordingly. Also, if the owner doesn't exist in the database, you'll have an opportunity to create it on the fly. 

Hint: Export nodes with this command
(hiro_get_marsnode -T <token> -d <some directory> --output-format json)
