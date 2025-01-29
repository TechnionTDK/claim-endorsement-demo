# Claim Endorsement Frontend

Installation:

- Ensure npm, python and miniconda are installed on your local machine.
- In order to install the React and Node.JS dependencies run the line `npm install all` from the command line twice. Once in the main project folder for the React dependencies and once from the 'server' folder for the Node.JS dependencies.
- Create a conda virtual enviourment called `condaenv` using the command `conda create --name condaenv`and install the requirements using the command `pip install -r requirements.txt` to install all the requirements in the condaenv enviourment.
- Update the file `my_config.py` to reflect where you want to have your .env file
- Create the .env in the location listed in `myconfig.py`. It should have the following variables

```js
CONNECTION_USERNAME = "<YOUR POSTGRES USERNAME>";
CONNECTION_PASSWORD = "<YOUR POSTGRES PASSWORD>";
SERVER_IP = "<IP OF THE SERVER WHERE POSTGRES IS RUN>";
GEMINI_KEY =
  "<YOUR GOOGLE GEMINI KEY(NEEDED TO CONNECT TO GOOGLE GEMINI IN ORDER TO GET EXPLANATIONS)>";
```

How to run:

Open 2 terminals, one in the base project folder and one in the 'server' folder and run the following command on each:

In the terminal for the server you should see `Server running! port 3005`.
In the terminal for the frontend you should see `Local:   http://localhost:5173/`.

```js
npm run dev
```

The condaenv does not need to be activcated beforehand.

After both started,the server and the frontend should be online locally at ports 3005 and 5173 correspondingly. In order to interact with the frontend open `http://localhost:5173/` in your browser.
Troubleshooting:

- There are still requirements missing after running `pip install -r requirements.txt`:
  - You can either install the missing requirments manually or alternatively you can download a copy of a virtualenv from `https://mega.nz/fm/ehgVjazQ`. Paste the content of the envs folder to your miniconda envs folder which is usually located in `C:\Users\<USER_NAME>\miniconda3\envs`
