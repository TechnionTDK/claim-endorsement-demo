# Claim Endorsement Frontend

Installation:

- Ensure npm, python and miniconda are installed on your local machine.
- in order to install the React and Node.JS dependencies run the line `npm install all` from the command line twice. Once in the main project folder for the React dependencies and once from the 'server' folder for the Node.JS dependencies.
- create a conda virtual enviourment called `condaenv` using the command `conda create --name condaenv`and install the requirements using the command `pip install -r requirements.txt` to install all the requirements in the condaenv enviourment.
- update the file `my_config.py` to reflect where you want to have your .env file
- create the .env in the location listed in `myconfig.py`. It should have the following variables

```js
CONNECTION_USERNAME = "<YOUR POSTGRES USERNAME>";
CONNECTION_PASSWORD = "<YOUR POSTGRES PASSWORD>";
SERVER_IP = "<IP OF THE SERVER WHERE POSTGRES IS RUN>";
GEMINI_KEY =
  "<YOUR GOOGLE GEMINI KEY(NEEDED TO CONNECT TO GOOGLE GEMINI IN ORDER TO GET EXPLANATIONS)>";
```

how to run:

Open 2 terminals, one in the base project folder and one in the 'server' folder and run the following command on each:

```js
npm run dev
```

the condaenv does not need to be activcated beforehand.

after both started,the server and site should be online locally.

troubleshooting:
There are still requirements missing after running `pip install -r requirements.txt`: - You can either install the missing requirments manually or alternatively you can download a copy of a virtualenv from `https://mega.nz/fm/ehgVjazQ`. paste the content of the envs folder to your miniconda envs folder which is usually located in `C:\Users\<USER_NAME>\miniconda3\envs`
