# Claim Endorsement Demo
This is a github repository for the demo described in "ClaimIt: Finding Convincing Views to Endorse a Claim", a demo paper submitted to SIGMOD 2025.

## Backend Setup
1. Downloading the data files:
Download the 4 directories and their files from the [link](https://technionmail-my.sharepoint.com/:f:/g/personal/shunita_campus_technion_ac_il/Egf-pA0G3k9ErDCE4wCnE-IBF59yCKsiblO2R1MAhl07jw?e=PZI4W3) and place them under server/data/.

1. Setup a postgresql database on the machine that will be used to run the server. Refer to https://www.postgresql.org/download/ for instructions for your specific machine.
1. To support the 4 datasets of the paper, create new databases with the following names: ACS7_disc, SO_disc, flights_disc, hm.

1. Prepare an enviroment file:
1.1 Update the file `my_config.py` to reflect where you want to have your .env file. Then create the .env in the location listed in `myconfig.py`. It should have the following variables:
```js
CONNECTION_USERNAME = "<YOUR POSTGRES USERNAME>";
CONNECTION_PASSWORD = "<YOUR POSTGRES PASSWORD>";
SERVER_IP = "<IP OF THE SERVER WHERE POSTGRES IS RUN>";
GEMINI_KEY =
  "<YOUR GOOGLE GEMINI KEY(NEEDED TO CONNECT TO GOOGLE GEMINI IN ORDER TO GET EXPLANATIONS)>";
```
5. Run the script server/src/upload_to_postgres.py to upload all 4 datasets into the corresponding databases.

# Frontend Setup

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

- If there are still requirements missing after running `pip install -r requirements.txt`:
  - You can either install the missing requirments manually or alternatively you can download a copy of a virtualenv from `https://mega.nz/fm/ehgVjazQ`. Paste the content of the envs folder to your miniconda envs folder which is usually located in `C:\Users\<USER_NAME>\miniconda3\envs`
