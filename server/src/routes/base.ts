import express from "express";
import { spawn, ChildProcess, exec } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

import dotenv from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";
import psTree from "ps-tree";
let isCurrentlyRunning = false;
let filepaths = ["SO", "flights", "Folkstable/SevenStates"];
const dotenv_path =
  "server\\src\\database_connection.env";
dotenv.config({ path: dotenv_path });
const apiKey = process.env.GEMINI_KEY;
const genAI = new GoogleGenerativeAI(apiKey);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
var router = express.Router();
let pythonProcess: ChildProcess | null = null;
// Example usage to check if the process is still running
const checkIfProcessIsRunning = async () => {
  const isProcessRunning = (pid: number): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      psTree(pid, (err, children) => {
        if (err) {
          return reject(err);
        }
        resolve(children.length > 0);
      });
    });
  };

  if (pythonProcess && pythonProcess.pid) {
    const running = await isProcessRunning(pythonProcess.pid);
    return running ? true : false;
  } else {
    return false;
  }
};
const stopPythonProcess = () => {
  try {
    const pid = pythonProcess.pid;
    if (pid === null) return;
    exec(`taskkill /PID ${pid} /T /F`, (error, stdout, stderr) => {
      if (error) {
        return;
      }
    });
  } catch (error) {}
};

async function callAI(prompt: any, modelName: string) {
  const model = genAI.getGenerativeModel({
    model: modelName,
    systemInstruction: `You are a helpful assistant that is tasked with translating queries and results into a natural sounding sentence
your responses need to be concise, and only be the natural sounding sentence you produce.
the response has to be not more than 30 words longs, but it's preferable you keep it as short as possible with maximum natural-soundness
here are examples for you to learn from
the parameters given to you are a database name, predicate 2-4 data parameters and the original sentence that you need to improve. your task is to respond with the natural sounding sentence
'Stack Overflow':[
 {
 "predicate": "LearnCodeCoursesCert=Other & NEWCollabToolsWantToWorkWith=PyCharm",
 "BSc avg salary": 13450,
 "MSC avg salary": 54750,
 "BSc count": 6,
 "MSc count": 10,
 "original sentence": Among the 16 people (out of 38K) who NEWCollabToolsWantToWorkWith=PyCharm and LearnCodeCoursesCert=Other, MSc graduates earn a higher salary on average ($54750) than BSc graduates($13450)."
 "sentence": "Among the 16 people (out of 38K) who want to work with PyCharm and learn to code through online courses, MSc graduates earn a higher salary on average ($54.7K) than BSc graduates($13.4K)."
 },
 {
 "predicate": "Ethnicity=Sountheast Asian",
 "BSc avg salary": 42302,
 "MSC avg salary": 82871,
 "BSc count": 226,
 "MSc count": 54,
 "original sentence": Among the 280 people (out of 38K) who Ethnicity=Sountheast Asian, MSc graduates earn a higher salary on average ($82871) than BSc graduates($42302)."
 "sentence": "Among the 280 people (out of 38K) who define themselves as Southeast Asian, MSc graduates earn a higher salary on average ($83K) than BSc graduates."
 },
 {
 "predicate": "OpSysProfessional use=Linux-based",
 "BSc avg salary": 165692,
 "MSC avg salary": 167230,
 "BSc count": 6497,
 "MSc count": 4201,
"original sentence": Among the 10698 people (out of 38K) who OpSysProfessional use=Linux-based, MSc graduates earn a higher salary on average ($167230) than BSc graduates($165692)."
 "sentence": "Among the 10,698 people (out of 38K) who use Linux based operating systems, MSc graduates earn a higher salary on average ($167K) than BSc graduates."
 },
 {
 "predicate": "OpSysProfessional use=Linux-based & YearsCode=0-10",
 "BSc avg salary": 120599,
 "MSC avg salary": 133620,
 "BSc count": 3126,
 "MSc count": 1399,
 "original sentence": Among the 4525 people (out of 38K) who OpSysProfessional use=Linux-based and YearsCode=0-10, MSc graduates earn a higher salary on average ($133620) than BSc graduates($120599)."
 "sentence": "Among the 4,525 people (out of 38K) who use Linux based operating systems and have been coding for up to 10 years, MSc graduates earn a higher salary on average ($134K) than BSc graduates."
 },
 {
 "predicate": "Employment=Independent contractor/freelance/self-employed & YearsCoder=10-20",
 "BSc avg salary": 100013,
 "MSC avg salary": 145399,
 "BSc count": 349,
 "MSc count": 338,
 "original sentence": Among the 687 people (out of 38K) who Employment=Independent contractor/freelance/self-employed and YearsCode=10-20, MSc graduates earn a higher salary on average ($145399) than BSc graduates($100013)."
 "sentence": "Among the 687 people (out of 38K) who are independent or freelancers and have been coding for 10 to 20 years, MSc graduates earn a higher salary on average ($145K) than BSc graduates."
 },
 {
 "predicate": "Country=Croatia & WorkExp=0-10",
 "BSc avg salary": 30474,
 "MSC avg salary": 45933,
 "BSc count": 12,
 "MSc count": 28,
 "original sentence": Among the 40 people (out of 38K) who Country=Croatia and WorkExp=0-10, MSc graduates earn a higher salary on average ($45933) than BSc graduates($30474)."
 "sentence": "Among the 40 people (out of 38K) in Croatia who have up to 10 years of work experience, MSc graduates earn a higher salary on average ($46K) than BSc graduates."
 },
 {
 "predicate": "WorkExp=20-30",
 "BSc avg salary": 224574,
 "MSC avg salary": 255,958.90,
 "BSc count": 1005,
 "MSc count": 667,
 "original sentence": Among the 1672 people (out of 38K) who WorkExp=20-30, MSc graduates earn a higher salary on average ($255,958.90) than BSc graduates($224574)."
 "sentence": "Among the 1672 people (out of 38K) who have 20-30 years of work experience, MSc graduates earn a higher salary on average ($256K) than BSc graduates."
 },
 {
 "predicate": "Country=Croatia & YearsCode=0-10",
 "BSc avg salary": 21946,
 "MSC avg salary": 45987,
 "BSc count": 12,
 "MSc count": 28,
 "original sentence": Among the 40 people (out of 38K) who Country=Croatia and YearsCode=0-10, MSc graduates earn a higher salary on average ($45987) than BSc graduates($21946)."
 "sentence": "Among the 40 people (out of 38K) in Croatia who have been coding for under 10 years, MSc graduates earn a higher salary on average ($46K) than BSc graduates."
 },
 {
 "predicate": "Country=India",
 "BSc avg salary": 51651,
 "MSC avg salary": 52,511.31,
 "BSc count": 1591,
 "MSc count": 458,
 "original sentence": Among the 2049 people (out of 38K) who Country=India, MSc graduates earn a higher salary on average ($52,511.31) than BSc graduates($51651)."
 "sentence": "Among the 2049 people (out of 38K) who work in India, MSc graduates earn a higher salary on average ($52.5K) than BSc graduates."
 },
 {
 "predicate": "BuyNewTool=Ask developers I know/work with & LanguageWantToWorkWith=Bash/Shell",
 "BSc avg salary": 197018,
 "MSC avg salary": 312710,
 "BSc count": 148,
 "MSc count": 86,
 "original sentence": Among the 234 people (out of 38K) who LanguageWantToWorkWith=Bash/Shell and BuyNewTool=Ask developers I know/work with , MSc graduates earn a higher salary on average ($312710) than BSc graduates($197018)."
 "sentence": "Among the 234 people (out of 38K) who want to work with Bash/Shell language and decide what new tools to buy by asking developers they know, MSc graduates earn a higher salary on average ($313K) than BSc graduates."
 },
 {
 "predicate": "BuyNewTool=Ask developers I know/work with",
 "BSc avg salary": 165769,
 "MSC avg salary": 182384,
 "BSc count": 900,
 "MSc count": 542,
 "original sentence": Among the 1442 people (out of 38K) who BuyNewTool=Ask developers I know/work with , MSc graduates earn a higher salary on average ($182384) than BSc graduates($165769)."
 "sentence": "Among the 1442 people (out of 38K) who decide what new tools to buy by asking developers they know, MSc graduates earn a higher salary on average ($182K) than BSc graduates."
 },
 {
 "predicate": "Country=Iran & YearsCodePro=0-10",
 "BSc avg salary": 39194,
 "MSC avg salary": 56190,
 "BSc count": 106,
 "MSc count": 68,
 "original sentence": Among the 174 people (out of 38K) who Country=Iran and YearsCodePro=0-10, MSc graduates earn a higher salary on average ($56190) than BSc graduates($39194)."
 "sentence": "Among the 174 people (out of 38K) in Iran who have been professionally coding for under 10 years, MSc graduates earn a higher salary on average ($56K) than BSc graduates."
 },
 {
 "predicate": "Country=Germany",
 "BSc avg salary": 113545,
 "MSC avg salary": 134642,
 "BSc count": 831,
 "MSc count": 1041,
 "original sentence": Among the 1872 people (out of 38K) who Country=Germany, MSc graduates earn a higher salary on average ($134642) than BSc graduates($113545)."
 "sentence": "Among the 1872 people (out of 38K) who work in Germany, MSc graduates earn a higher salary on average ($135K) than BSc graduates"
 },
 {
 "predicate": "OfficeStackSyncWantToWorkWith=Microsoft Teams & PlatformHaveWorkedWith=OpenStack",
 "BSc avg salary": 48749,
 "MSC avg salary": 98014,
 "BSc count": 7,
 "MSc count": 15,
 "original sentence": Among the 22 people (out of 38K) who PlatformHaveWorkedWith=OpenStack and OfficeStackSyncWantToWorkWith=Microsoft Teams, MSc graduates earn a higher salary on average ($98014) than BSc graduates($48749)."
 "sentence": "Among the 22 people (out of 38K) who have worked with OpenStack platform and would like to work with Microsoft Teams, MSc graduates earn a higher salary on average ($98K) than BSc graduates."
 },
 {
 "predicate": "NEWCollabToolsHaveWorkedWith=Notepad++ & OrgSize=I don't know",
 "BSc avg salary": 62759,
 "MSC avg salary": 231458,
 "BSc count": 23,
 "MSc count": 9,
 "original sentence": Among the 32 people (out of 38K) who NEWCollabToolsHaveWorkedWith=Notepad++ & OrgSize=I don't know, MSc graduates earn a higher salary on average ($231458) than BSc graduates($62759)."
 "sentence": "Among the 32 people (out of 38K) who have worked with Notepad++ and do not know the size of their organization, MSc graduates earn a higher salary on average ($231K) than BSc graduates."
 },
 {
 "predicate": "OfficeStackAsyncHaveWorkedWith=Jira Work Management & OfficeStackSyncWantToWorkWith=Rocketchat",
 "BSc avg salary": 43585,
 "MSC avg salary": 213557,
 "BSc count": 20,
 "MSc count": 7,
 "original sentence": Among the 27 people (out of 38K) who OfficeStackAsyncHaveWorkedWith=Jira Work Management and OfficeStackSyncWantToWorkWith=Rocketchat, MSc graduates earn a higher salary on average ($213557) than BSc graduates($43585)."
 "sentence": "Among the 27 people (out of 38K) who have worked with Jira and want to work with Rocketchat, MSc graduates earn a higher salary on average ($160K) than BSc graduates."
 },
 {
 "predicate": "Ethnicity=Indian & NEWCollabToolsWantToWorkWith=Vim",
 "BSc avg salary": 75211,
 "MSC avg salary": 160885,
 "BSc count": 46,
 "MSc count": 14,
 "original sentence": Among the 60 people (out of 38K) who Ethnicity=Indian & NEWCollabToolsWantToWorkWith=Vim, MSc graduates earn a higher salary on average ($160885) than BSc graduates($75211)."
 "sentence": "Among the 60 people (out of 38K) who define themselves as Indian and want to work with Vim, MSc graduates earn a higher salary on average ($160K) than BSc graduates."
 },
 {
 "predicate": "OpSysProfessional use=Windows & WebframeHaveWorkedWith=Express",
 "BSc avg salary": 103820,
 "MSC avg salary": 180683,
 "BSc count": 218,
 "MSc count": 90,
 "original sentence": Among the 308 people (out of 38K) who OpSysProfessional use=Windows & WebframeHaveWorkedWith=Express, MSc graduates earn a higher salary on average ($180683) than BSc graduates($103820)."
 "sentence": "Among the 308 people (out of 38K) who use Windows operating system and have worked with the Express web framework, MSc graduates earn a higher salary on average ($180K) than BSc graduates."
 }
]
'Flights':[
 {
 "predicate": "scheduled_departure=3:00-4:00",
 "saturday delays": "43",
 "monday delays": "30",
 "sentence": "Among flights scheduled_departure=3:00-4:00, there are more flight delays on Saturdays (43) vs. Mondays (30).",
 "sentence": "Among flights scheduled to depart between 3:00-4:00 AM, there are more flight delays on Saturdays (43) vs. Mondays (30).",
 },
 {
  "predicate": "airline=HA",
 "saturday delays": "1,028.00",
 "monday delays": "986",
 "original sentence": "Among flights airline=HA, there are more flight delays on Saturdays (1,028) vs. Mondays (986).",
 "sentence": "Among flights operated by Hawaiian Airlines Inc., there are more flight delays on Saturdays (1,028) vs. Mondays (986).",
 },
 {
  "predicate": "Month=10",
 "saturday delays": "9,549.00",
 "monday delays": "8,744",
 "original sentence": "In Month=10, there were more flight delays on Saturdays (9549) vs. Mondays (8744).",
 "sentence": "In October, there were more flight delays on Saturdays (9,549) vs. Mondays (8,744).",
 },
 {
  "predicate": "air_time=390-400",
 "saturday delays": "51",
 "monday delays": "41",
 "original sentence": "Among flights air_time=390-400, there were more flight delays on Saturdays (51) vs. Mondays (41).",
 "sentence": "Among flights with air time between 390 and 400 minutes, there were more flight delays on Saturdays (51) vs. Mondays (41).",
 },
 {
  "predicate": "day (of month)=30-41",
 "saturday delays": "3,753.00",
 "monday delays": "257",
 "original sentence": "Among flights day (of month)=30-41, there were more flight delays on Saturdays (3,753) vs. Mondays (2573).",
 "sentence": "Among flights on the last days of the month (30-31), there were more flight delays on Saturdays (3,753) vs. Mondays (2573).",
 },
 {
  "predicate": "FLIGHT_NUMBER=2",
 "saturday delays": "49",
 "monday delays": "48",
 "original sentence": "Among flights FLIGHT_NUMBER=2, there are more flight delays on Saturdays (49) vs. Mondays (48).",
 "sentence": "Among flights with flight number 2, there are more flight delays on Saturdays (49) vs. Mondays (48).",
 },
 {
  "predicate": "FLIGHT_NUMBER=3507",
 "saturday delays": "13",
 "monday delays": "10",
 "original sentence": "Among flights FLIGHT_NUMBER=3507, there were more flight delays on Saturdays (13) vs. Mondays (10).",
 "sentence": "Among flights with flight number 3507, there were more flight delays on Saturdays (13) vs. Mondays (10).",
 },
 {
  "predicate": "SCHEDULED_TIME=480-490",
 "saturday delays": "17",
 "monday delays": "14",
 "original sentence": "Among flights SCHEDULED_TIME=480-490, there were more flight delays on Saturdays (17) vs. Mondays (14).",
 "sentence": "Among flights with scheduled duration between 480 and 490 minutes, there were more flight delays on Saturdays (17) vs. Mondays (14).",
 },
 {
  "predicate": "FLIGHT_NUMBER=3430",
 "saturday delays": "16",
 "monday delays": "14",
 "original sentence": "Among flights FLIGHT_NUMBER=3430, there were more flight delays on Saturdays (16) vs. Mondays (14).",
 "sentence": "Among flights with flight number 3430, there were more flight delays on Saturdays (16) vs. Mondays (14).",
 },
 {
  "predicate": "FLIGHT_NUMBER=4867",
 "saturday delays": "14",
 "monday delays": "9",
 "original sentence": "Among flights FLIGHT_NUMBER=4867, there were more flight delays on Saturdays (14) vs. Mondays (9).",
 "sentence": "Among flights with flight number 4876, there were more flight delays on Saturdays (14) vs. Mondays (9).",
 }
]
'ACS':[
 {
 "predicate": "Marital status=Never married & Ethnicity=african american",
 "Men avg salary": 16720,
 "Women avg salary": 21507,
 "Men count": 24762,
 "Women count": 24249,
 "original sentence": "Among the 49011 (out of 1.2M) african american and never married, women have a higher income on average ($21507) than men."
 "sentence": "Among the 49,011 (out of 1.2M) African Americans who were never married, women have a higher income on average ($21.5K) than men."
 },
 {
 "predicate": "Raw labor-force status=Not in the labor force & Marital status=Never Married",
 "Men avg salary": 7201,
 "Women avg salary": 7325,
 "Men count": 71044,
 "Women count": 58418,
  "original sentence": "Among the 129462 (out of 1.2M) Raw labor-force status=Not in the labor force and Marital=status Never Married, women have a higher income on average ($7325) than men."
 "sentence": "Among the 129,462 people (out of 1.2M) who are not in the labor force and were never married, women have a higher income on average ($7,325) than men."
 },
 {
 "predicate": "Insurance through a current or former employer or union=yes & Related child=yes",
 "Men avg salary": 1017,
 "Women avg salary": 1044,
 "Men count": 14448,
 "Women count": 13918,
  "original sentence": "Among the 28366 (out of 1.2M) Insurance through a current or former employer or union=yes and Related child=yes, women have a higher income on average ($1044) than men."
 "sentence": "Among the 28,366 people (out of 1.2M) with insurance through an employer or union, who have a child, women have a higher income on average ($1,044) than men."
 },

 {
 "predicate": "Class of worker=Employee of a private for-profit company or business, or of an individual, for wages, salary, or commissions & Own child=yes",
 "Men avg salary": 3436,
 "Women avg salary": 3474,
 "Men count": 3698,
 "Women count": 3897,
 "original sentence": "Among the 7595 (out of 1.2M) Class of worker=Employee of a private for-profit company or business, or of an individual, for wages, salary, or commissions and Own child=yes, women have a higher income on average ($3474) than men."
 "sentence": "Among the 7,595 people (out of 1.2M) who work for a private company and have a child, women have a higher income on average ($3,474) than men."
 },
 {
 "predicate": "Grade level attending=12 & Last worked 1-5 years ago",
 "Men avg salary": 1656,
 "Women avg salary": 2768,
 "Men count": 545,
 "Women count": 385,
 "original sentence": "Among the 930 (out of 1.2M) Grade level attending=12 and Last worked 1-5 years ago, women have a higher income on average ($2768) than men."
 "sentence": "Among the 930 (out of 1.2M) 12th grade students who have last worked 1-5 years ago, women have a higher income on average ($2,768) than men."
 },
 {
 "predicate": "Age=20-30 & work for armed forces",
 "Men avg salary": 36789,
 "Women avg salary": 39288,
 "Men count": 1360,
 "Women count": 239,
 "original sentence": "Among the 1599 (out of 1.2M) Age=20-30 & work for armed forces, women have a higher income on average ($39288) than men."
 "sentence": "Among the 1,599 people (out of 1.2M) of age 20-30 who work in the armed forces, women have a higher income on average ($39K) than men."
 },
 {
 "predicate": "Veteran Service Disability Rating (percentage)=Not Reported & Cognitive difficulty = no",
 "Men avg salary": 46610,
 "Women avg salary": 57222,
 "Men count": 538,
 "Women count": 44,
 "original sentence": "Among the 582 (out of 1.2M) Veteran Service Disability Rating (percentage)=Not Reported and Cognitive difficulty = no, women have a higher income on average ($57222) than men."
 "sentence": "Among the 582 (out of 1.2M) army veterans who have not reported a Veteran Service Disability Rating and who do not have cognitive difficulty, women have a higher income on average ($57K) than men."
 },
 {
 "predicate": "Veteran Service Disability Rating (percentage)=Not Reported",
 "Men avg salary": 43222,
 "Women avg salary": 50323,
 "Men count": 672,
 "Women count": 58,
 "original sentence": "Among the 730 (out of 1.2M) Veteran Service Disability Rating (percentage)=Not Reported , women have a higher income on average ($50323) than men."
 "sentence": "Among the 730 (out of 1.2M) army veterans who have not reported a Veteran Service Disability Rating, women have a higher income on average ($50K) than men."
 },

 {
 "predicate": "Never married & last worked over 5 years ago",
 "Men avg salary": 5649,
 "Women avg salary": 6155,
 "Men count": 49843,
 "Women count": 41471,
 "original sentence": "Among the 91314 (out of 1.2M) Never married and last worked over 5 years ago , women have a higher income on average ($6155) than men."
 "sentence": "Among the 91K people (out of 1.2M) who were never married and have not worked in the last 5 years, women have a higher income on average ($6,155) than men."
 },
 {
 "predicate": "JWDP=40-50 & SOCP=272012",
 "Men avg salary": 98318,
 "Women avg salary": 105045,
 "Men count": 73,
 "Women count": 45,
 "original sentence": "Among the 118 (out of 1.2M) JWDP=40-50 & SOCP=272012 , women have a higher income on average ($105045) than men."
 "sentence": "Among the 118 people (out of 1.2M) who depart for work between 6:45-7:35 and work as producers and directors, women have a higher income on average ($105K) than men."
 },
 {
 "predicate": "HICOV=2 & OCCP_grouped=CON",
 "Men avg salary": 28784,
 "Women avg salary": 29476,
 "Men count": 9608,
 "Women count": 284,
 "original sentence": "Among the 9892 (out of 1.2M) HICOV=2 & OCCP_grouped=CON , women have a higher income on average ($29476) than men."
 "sentence": "Among the 9,892 people (out of 1.2M) who do not have health insurance and work in construction, women have a higher income on average ($29K) than men."
 },
 {
 "predicate": "OCCP=2145.0 & REGION=4",
 "Men avg salary": 58543,
 "Women avg salary": 60086,
 "Men count": 125,
 "Women count": 458,
 "original sentence": "Among the 583 (out of 1.2M) OCCP=2145.0 & REGION=4, women have a higher income on average ($60086) than men."
 "sentence": "Among the 583 people (out of 1.2M) who work as paralegals and legal assistants in west US, women have a higher income on average ($60K) than men."
 },
 {
 "predicate": "PUMA=10504 & RAC3P=2",
 "Men avg salary": 15191,
 "Women avg salary": 22105,
 "Men count": 91,
 "Women count": 83,
 "original sentence": "Among the 174 (out of 1.2M) PUMA=10504 & RAC3P=2, women have a higher income on average ($22105) than men."
 "sentence": "Among the 174 African American people (out of 1.2M) in Polk county (Florida), women have a higher income on average ($22K) than men."
 },
 {
 "predicate": "POBP=247 & RACWHT=1",
 "Men avg salary": 43437,
 "Women avg salary": 51467,
 "Men count": 32,
 "Women count": 54,
 "original sentence": "Among the 86 (out of 1.2M) POBP=247 & RACWHT=1, women have a higher income on average ($51467) than men."
 "sentence": "Among the 86 people who define themselves as White (out of 1.2M) who were born in Vietnam, women have a higher income on average ($51K) than men."
 }
]`,
  });
  try {
    const result = await model.generateContent(prompt);
    console.log(result.response.text());
    return result.response.text();
  } catch (e) {
    console.log("error");
    console.log(e);
    return "error";
  }
}
const deleteFile = async (pathname) => {
  console.log("this is the pathfile of the delete file look at a me file");
  console.log(pathname);

  const filePath = path.join("data", pathname, "results", "demo_test.csv");
  console.log(filePath);
  if (!fs.existsSync(filePath)) {
    return;
  }
  fs.unlink(filePath, (err) => {
    if (err) {
      console.error(`Error deleting file: ${err}`);
      return;
    }
    console.log("File deleted successfully");
  });
  return;
};
const fixPricesHM = (data, dbName) => {
  var data2 = data;
  if (dbName === "hm") {
    data2 = data.map((item) => {
      item["mean1"] = item["mean1"] * 1000;
      item["mean2"] = item["mean2"] * 1000;
      return item;
    });
  }
  return data2;
};
const callPythonMain = async (dbname, aggtype, grpattr, g1, g2) => {
  return new Promise((resolve, reject) => {
    isCurrentlyRunning = true;
    //pythonProcess = spawn("py", ["src/createData.py"]);
    pythonProcess = spawn(
      "conda",
      [
        "run",
        "-n",
        "claimit",
        "python",
        "src/claim_endorse_demo.py",
        "--dbname",
        dbname,
        "--aggtype",
        aggtype,
        "--grpattr",
        grpattr,
        "--g1",
        `"${g1}"`,
        "--g2",
        `"${g2}"`,
      ],
      { shell: true }
    );

    console.log("finished writing");

    let data = "";
    pythonProcess.stdout.on("data", (chunk) => {
      data += chunk.toString();
      isCurrentlyRunning = false;
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
      isCurrentlyRunning = false;
      reject(data.toString());
    });

    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        //  console.log(`pythonProcess exited with code ${code}`);
        isCurrentlyRunning = false;

        reject(`Process exited with code ${code}`);
      }
      isCurrentlyRunning = false;
      resolve(data);
    });
    pythonProcess.on("exit", (code) => {
      if (code !== 0) {
        //   console.log(`pythonProcess exited with code ${code}`);
        isCurrentlyRunning = false;

        reject(`Process exited with code ${code}`);
      }
      isCurrentlyRunning = false;
      resolve(data);
    });
  });
};
const calcValue = (dataItem) => {
  const cosSim = Math.max(dataItem["Cosine Similarity"], 0);
  const invP = Math.max(dataItem["Inverted pvalue"], 0);
  const normAnova = Math.max(dataItem["Normalized Anova F Stat"], 0);
  const normMI = Math.max(0, dataItem["Normalized_MI"]);
  const coverage = Math.max(0, dataItem["Coverage"]);
  return cosSim + invP + normAnova + normMI + coverage;
};
const getMax = (data) => {
  const tempData = [...data];
  tempData.sort((a, b) => calcValue(b) - calcValue(a));
  return tempData;
};
function emptyFileOriginalQuery() {
  const filePath = path.join(
    __dirname,
    "../../../src/assets/demo_test_ORIGINAL.json"
  );
  fs.writeFile(filePath, JSON.stringify({}), (err) => {
    if (err) {
      console.error("Error emptying the file:", err);
    }
    console.log("File emptied successfully");
  });
}
router.get("/", async (req, res) => {
  try {
    emptyFileOriginalQuery();
    const dbname = decodeURIComponent(req.query.dbname as string);
    console.log(dbname);
    const aggtype = decodeURIComponent(
      req.query.aggtype as string
    ).toLowerCase();
    console.log(aggtype);

    const grpattr = decodeURIComponent(req.query.grpattr as string);
    console.log(grpattr);
    const g1 = decodeURIComponent(req.query.g1 as string);
    console.log(g1);
    const g2 = decodeURIComponent(req.query.g2 as string);
    console.log(g2);

    console.log("Starting Python process...");
    callPythonMain(dbname, aggtype, grpattr, g1, g2)
      .then((output) => {
        console.log(output);
      })
      .catch((error) => {
        console.error("Error calling Python main:", error);
      });

    res.status(200).send();
  } catch (error) {
    const status = error.status || 500;
    res.status(status).send(error);
  }
});

router.get("/send-data", async (req, res) => {
  const index = req.query.prev ? parseInt(req.query.prev as string) : 0;
  const options = {
    maxBuffer: 1000 * 1024 * 1024, // Increase maxBuffer to 10 MB
  };
  const running = await checkIfProcessIsRunning();
  const dbName = req.query.dbName;
  console.log("look at me look at me ");
  console.log(dbName);
  console.log(req.query);

  exec(
    `py src/1-CreateData.py ${index} ${dbName}`,
    options,
    (error, stdout, stderr) => {
      if (error) {
        console.log("hello");

        console.error(`exec error: ${error}`);
        return;
      }
      try {
        const sanitizedStdout = stdout
          .replace(/\bNaN\b/g, '"N/A"')
          .replace(/\bN E W\b/g, "New");

        if (stdout.trim() == "-1") {
          console.log("in here");
          if (running) {
            console.log("is currently running");

            res.status(200).send({ isEmpty: false });
            return;
          }
          res.status(200).send({ isEmpty: true });
          return;
        }

        const data = JSON.parse(sanitizedStdout);
        console.log("look here look here ");
        // console.log(data);

        if (data.length == 0) {
          if (isCurrentlyRunning) {
            console.log("is currently running");

            res.status(200).send({ isEmpty: false });
            return;
          }
          console.log("finished");

          res.status(200).send({ isEmpty: true });
          return;
        }
        console.log("-------------------------------");

        console.log("has done here");
        var data2 = fixPricesHM(data, dbName);
        const groupedData = data2.reduce((acc: any, item: any) => {
          const key = `${item.Attr1_str}-${item.Attr2_str}`;
          if (!acc[key]) {
            acc[key] = [];
          }
          acc[key].push(item);
          return acc;
        }, {} as Record<string, (typeof data)[0][]>);

        var separatedArrays = Object.values(groupedData);
        //console.log(separatedArrays);
        //console.log(separatedArrays.length);

        const sortedArrays2 = separatedArrays
          .map((item) => getMax(item))
          .map((item) => {
            return { best: item[0], fullList: item };
          });

        res
          .status(200)
          .send({ data: data, isEmpty: false, grouped: sortedArrays2 });
      } catch (error) {
        console.log(error);
        res.status(500).send({ error: "An error has occurred" });
      }
    }
  );

  return;
});

router.post("/LLM", async (req, res) => {
  const modelName = req.body.modelName as string;
  const compare = req.body.compareValue;
  const databaseName = req.body.databaseName;
  const predicate = req.body.predicate;

  const g1Name = req.body.g1Name;
  const g1CompareValue = req.body.g1CompareValue;
  const g1Amount = req.body.g1Amount;

  const g2Name = req.body.g2Name;
  const g2CompareValue = req.body.g2CompareValue;
  const g2Amount = req.body.g2Amount;

  const g1Value = `"${g1Name} count":${g1Amount}`;
  const g2Value = `"${g2Name} count":${g2Amount}`;

  const func = req.body.function;
  const g1 = `"${g1Name} ${func} ${compare}":${g1CompareValue}`;
  const g2 = `"${g2Name} ${func} ${compare}":${g2CompareValue}`;
  let sentence;
  switch (databaseName) {
    case "Flights":
      let splitted1 = g1Value.split("-")[1].split(" ")[0];
      let splitted2 = g2Value.split("-")[1].split(" ")[0];

      sentence = `Among flights ${predicate}, there are more flight delays on ${splitted2} (${g2Amount}) vs. ${splitted1} (${g1Amount}).`;

      /* console.log(
        `${databaseName}\n"predicate":${predicate} \n${splitted1}\n${splitted2} \n"original sentence": ${sentence}`
      );*/
      break;
    case "Stack Overflow":
      sentence = `Among the ${
        Number(g1Amount) + Number(g2Amount)
      } people (out of 38K) who ${predicate}, `;
      switch (func) {
        case "avg":
          sentence += ` ${g2Name} earn a higher salary on average ($${g2CompareValue}) than ${g1Name}($${g1CompareValue}).`;

          break;
        case "median":
          sentence += ` ${g2Name} earn a higher median salary ($${g2CompareValue}) than ${g1Name}($${g1CompareValue}).`;
          break;
        case "count":
          sentence += `There are more of group ${g2Name} than of group ${g1Name} .`;
          break;

        default:
          break;
      }

      /*console.log(
        `${databaseName}\n"predicate":${predicate} \n${g1} \n${g1Value} \n${g2} \n${g2Value} \n"original sentence": ${sentence}`
      );*/
      break;
    case "ACS":
      break;

    default:
      break;
  }
  console.log("???????????????????????????????????????????");

  console.log(
    `${databaseName}\n"predicate":${predicate} \n${g1} \n${g1Value} \n${g2} \n${g2Value} \n"original sentence": ${sentence}`
  );
  console.log("???????????????????????????????????????????");

  const result = await callAI(
    `${databaseName}\n"predicate":${predicate} \n${g1} \n${g1Value} \n${g2} \n${g2Value} \n"original sentence": ${sentence}`,
    modelName
  );
  if (result === "error") {
    res.status(500).send({ result: "an error has occurred, try again" });
    return;
  }
  res.status(200).send({ result });
});

router.delete("/", async (req, res) => {
  try {
    let pathname = req.query.pathname;
    stopPythonProcess();
    console.log("starting delete");

    console.log(pathname);

    deleteFile(pathname)
      .then((output) => {
        console.log("this is the output:");

        console.log(output);
        console.log("end of output");
      })
      .catch((error) => {
        console.error("Error calling Python main:", error);
      });

    res.status(200).send();
  } catch (error) {
    const status = error.status || 500;
    res.status(status).send(error);
  }
});

export default router;
