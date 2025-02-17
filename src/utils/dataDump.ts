import { ASC7CompareValues } from "./ACS7/ACS7CompareValues";
import { ACS7GroupByOptions } from "./ACS7/ACS7GroupByOptions";
import { ACS7TranslationDict } from "./ACS7/ACS7TranslationDict";
import { ACS7ValuesDict } from "./ACS7/ACS7ValuesDict";
import { FlightsCompareValues } from "./Flights/FlightsCompareValues";
import { FlightsGroupByOptions } from "./Flights/FlightsGroupByOptions";
import { FlightsTranslationDict } from "./Flights/FlightsTranslationDict";
import { FlightsValuesDict } from "./Flights/FlightsValuesDict";
import { HMCompareValues } from "./HM/HMCompareValues";
import { HMGroupByOptions } from "./HM/HMGroupByOptions";
import { HMTranslationDict } from "./HM/HMTranslationDict";
import { StackOverflowCompareValues } from "./StackOverflow/StackOverflowCompareValues";
import { StackOverflowGroupByOptions } from "./StackOverflow/StackOverflowGroupByOptions";
import { StackOverflowTranslationDict } from "./StackOverflow/StackOverflowTranslationDict";

interface groupByOptions {
  [key: string]: string[];
}
interface compareValues {
  [key: string]: { [key: string]: string[] };
}
interface aggregateOptions {
  [key: string]: string;
}
export const aggregateDB: aggregateOptions = {
  "Stack Overflow": "Converted Yearly Comp",
  "US Census": "(is this ACS7?)PINCP",
  Flights: "Departure Delay",
  HM: "Price",
};

export const options = {
  responsive: true,
  scales: {
    y: {
      min: 0,
      max: 1,
    },
  },
  plugins: {
    legend: {
      display: false,
      position: "bottom" as const,
    },
    title: {
      display: true,
      text: "",
    },
    tooltip: {
      bodyFont: {
        size: 22, // Set the font size for tooltip text
      },
    },
  },
};
export const parameters: { [key: number]: string } = {
  0: "Semantic Similarity",
  1: "Statistical Significance",
  2: "Analysis of Variance",
  3: "Mutual Information",
  4: "Coverage (group size)",
};
export const parametersAltered: { [key: number]: string } = {
  0: "Semantic Similarity",
  1: "Avarage Difference",
  2: "Analysis of Variance",
  3: "Mutual Information",
  4: "Coverage (group size)",
};

export const popupTexts: { [key: string]: string } = {
  Phase1: "Phase 1: Database",
  Phase2: "Phase 2: Claim",
  Phase3:
    "Phase 3: Scoring Weights I think the better idea is to have the one here, and describe all the elements here",
  "Semantic Similarity": "Semantic Similarity Info Text",
  "Statistical Significance": "Statistical Significance Info Text",
  "Avarage Difference": "Avarage Difference Info Text",
  "Analysis of Variance": "Analysis of Variance Info Text",
  "Mutual Information": "Mutual Information Info Text",
  Covarage: "Covarage Info Text",
};
export const topOptions = [10, 15, 25, 50, 100];
export const aggregateFunctions = ["Avg", "Median", "Count"];

export const translateDB: { [key: string]: number } = {
  ["Stack Overflow"]: 0,
  ["Flights"]: 1,
  ["US Census"]: 2,
  ["HM"]: 3,
};
export const groupByOptions: groupByOptions = {
  "Stack Overflow": StackOverflowGroupByOptions,
  "US Census": ACS7GroupByOptions,
  Flights: FlightsGroupByOptions,
  HM: HMGroupByOptions,
};
export const compareValues: compareValues = {
  "Stack Overflow": StackOverflowCompareValues,
  "US Census": ASC7CompareValues,
  Flights: FlightsCompareValues,
  HM: HMCompareValues,
};

export const translationDict: { [key: string]: string } = {
  ...StackOverflowTranslationDict,
  ...ACS7TranslationDict,
  ...FlightsTranslationDict,
  ...HMTranslationDict,
};
export const valuesDict: { [key: string]: { [subKey: string]: string } } = {
  ...ACS7ValuesDict,
  ...FlightsValuesDict,
};
export const compareTitle: { [key: string]: string } = {
  "Stack Overflow": "Salary",
  "US Census": "Salary",
  Flights: "Departure Delay",
  HM: "Price",
};
