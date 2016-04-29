


> 

Honeypot
-----------
Python honeypot framework with plugin API

**Installing honeypot**
You'll need a few things to get you started before you can use honeypot.
Run the following commands:
`dpkg -i HoneyPotPackage.deb` 
`cd /HP_Install/` 
`bash setup.sh` 
Setup Authbind (see Setting up Authbind). 
Return to honeypot directory and run start.sh. 
Your honeypot is running!


**Setting up Authbind**

Authbind must be installed to allow plugins to bind to well-known ports without running as root. To set up authbind, create the file /etc/authbind/byuid/<uid>, where <uid> is the uid of the user that will run the honeypot (can be obtained with id -u <username>, substituting the actual user name). The file should contain the line 0.0.0.0/32:1,1023 to allow binding to any well-known port (anything in the range 1-1023, inclusive). Start the honeypot by running ./start.sh, which will use authbind.

**Writing a plugin**

Several items are needed in order for a new plugin to run, persist to db, and show results in visual tool. Extend Template from plugin_template.py to inherit some of the needed attributes and functionality.

To run, plugin must have the following:

 - class named Plugin
 - get_port() inside Plugin class (returns port number)
 - run(socket, address, session), inside Plugin class, where session can be used to write to db

To write to db and use visual tool, Plugin class must have the following:

 - get_display() (returns name of the plugin that you will be displayed in the visual tool)
 - get_description() (returns description of plugin)
 - get_orm() (returns ORM)
 - get_value() (returns name of plugin)
 - nested class that defines a table, which must:
	 - extend Base from base.py
	 - define table name
	 - define primary key
	 - include ip_address column
	 - include time column
	 - include feature column (point on the map)
	 - ex: 

	 `    class Http(Base):`
	`__tablename__ = "http"`
	`id = Column(Integer, primary_key=True)`
	`ip_address= Column(String, nullable=False)`
        `command = Column(String)`
        `path = Column(String)`
        `version = Column(String)`
        `headers = Column(String)`
        `time = Column(DateTime)`
        `feature = Column(String)`



**Configuring your honeypot**
You can edit honeypot.ini to configure your honeypot. honeypot.ini has several sections that correlate with specific files in the program. The section titles are surrounded with brackets. [honeypot] specifies paths of the database, plugins directory, log file, and also a list ports that the user wants to listen on. [https] specifies names of certificate and private key files for ssl connection. If an item is not specified in its section, data specified in [default] will be used.

[Project Plan](https://docs.google.com/document/d/1NPZYz_Gn41zKydzIijU4lbnletNN57zfZNM8AaEY_ZQ/edit?usp=sharing)

[Research Doc](https://docs.google.com/document/d/10FqRp2M8X2r19Jm75DzA1jPB805p85qZo2l6CmV1bM0/edit?usp=sharing)

[Download Debian Package](http://cs4260honeypot.com.s3-website-us-west-2.amazonaws.com/debian/HoneyPotPackage.deb)

[SQLAlchemy Session Docs](http://docs.sqlalchemy.org/en/latest/orm/session.html)
