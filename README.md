# Claim Endorsement Frontend

how to run:

- run the command line

```js
npm install all
```

from the main folder

- then again from the server folder

- create a conda virtual enviourment called `condaenv` using the command `conda create --name condaenv`and install the requirements using the command `pip install -r requirements.txt`
- after it's created you'll need to manually install to it a couple more dependencies, trial and error for now during initial runs.
- in the case you get stuck, you can download the virtualenv from `https://mega.nz/fm/ehgVjazQ`. paste the content of the envs folder to your miniconda envs folder which is located in `C:\Users\<USER_NAME>\miniconda3\envs`
- import the `data folder` contents, and add a `results/demo_test.csv` to the SO folder. this is where the results are stored for now.
- go to `claim_endorse_demo.py` and change the location of the dotenv uri according to your computers' path.

after all of this is installed open 2 terminals, one in the base folder and one in the server folder and run

```js
npm run dev
```

the condaenv does not need to be activcated while doing so

after both started,the server and site should be online locally.
