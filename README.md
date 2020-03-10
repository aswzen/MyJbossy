
# myJBossy #

![enter image description here](https://github.com/aswzen/MyJbossy/blob/master/sc.png?raw=true)

### Introduction ###

This app allows you the see current deployed war/jar files in some servers, by using their (Jboss and Wildfly) APIs we can get so many information about the packages.

### To Do ###
- [X] Remove deployments
- [ ] Multiple environment
- [ ] Restart jboss/wildfly feature
- [ ] Upload package feature
- [ ] Lookup log
- [ ] Library installer

### Requirements ###

- Python 3
- Bash Access

### Installation ###

Run below command in sequence
1. Setup environment
`nano config.json`
3. Cloning this repository
4. Creating environment
`python3 -m venv venv` or by `py -3 -m venv venv`
5. Activate the environment
`. venv/bin/activate` or by `. venv/scripts/activate`
6. Installing the flask framework 
`pip install Flask`
7. Setting flask app main file
`export FLASK_APP=main.py`
8. Running the program
`flask run`
If you want to make it accessible from outside network you can use 
`flask run --host=0.0.0.0`

### Libraries ###
- [Flask Framework](https://flask.palletsprojects.com/)
- [w2ui](http://w2ui.com/)
- [JBOSS Api Docs](https://docs.jboss.org/author/display/WFLY10/The+HTTP+management+API)
- [JBoss EAP 7.2 Model Reference](http://wildscribe.github.io/)
- [JBoss HTTP Api doc](https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/6.4/html/administration_and_configuration_guide/sect-deploy_with_the_http_api)

