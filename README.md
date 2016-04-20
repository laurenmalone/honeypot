# honeypot

Python honeypot framework with plugin API

authbind must be installed to allow plugins to bind to well-known ports without running as root. To set up authbind, create the file `/etc/authbind/byuid/<uid>`, where `<uid>` is the `uid` of the user that will run the honeypot (can be obtained with `id -u <username>`, substituting the actual user name). The file should contain the line `0.0.0.0/32:1,1023` to allow binding to any well-known port (anything in the range 1-1023, inclusive). Start the honeypot by running `./start.sh`, which will use authbind.

[Project Plan](https://docs.google.com/document/d/1NPZYz_Gn41zKydzIijU4lbnletNN57zfZNM8AaEY_ZQ/edit?usp=sharing)

[Research Doc](https://docs.google.com/document/d/10FqRp2M8X2r19Jm75DzA1jPB805p85qZo2l6CmV1bM0/edit?usp=sharing)

[Download Debian Package](http://cs4260honeypot.com.s3-website-us-west-2.amazonaws.com/debian/HoneyPotPackage.deb)
