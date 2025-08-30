export interface Data {
  predicate: number; //will be changed to reflect more data
  labels: string[];
  datasets: Dataset[];
  attribute1: string;
  attribute2: string;
  N1: number;
  N2: number;
  mean1: number;
  mean2: number;
  value1: string;
  value2: string;
  time: number;
  fullList: DatabaseData[];
  unfolded: boolean;
  explanation: any;
  uniqueKey: string;
}
export interface loadingStates {
  name: string;
  value: boolean;
}
export interface PredicateType {
  attribute1: string;
  value1: string;
  attribute2: string;
  value2: string;
  mean1: number;
  N1: number;
  mean2: number;
  N2: number;
}
export interface DataType {
  value: number;
  name: string;
}
export interface Dataset {
  label: string;
  data: number;
  backgroundColor: string;
}
export interface HoverDataProps {
  data: Dataset[] | null;
  predicate: JSX.Element;
}
export interface Phase1Props {
  selectedDatabase: string;

  selectInitial: (e: any) => void;
}
export interface Phase2Props {}
export interface Phase3Props {
  clearData: (interval: number) => void;
}

export interface PredicateProps {
  func: (event: any) => void;
  folded: boolean;
  showIcon: boolean;
  predicate: JSX.Element;
}
export interface SortIconProps {
  color: string;
  sorting: number;
  onClickSort: () => void;
}
export interface loadingStates {
  name: string;
  value: boolean;
}
export interface HeaderDisplayProps {
  sortingOptions: number[];
  setSortingOptions: React.Dispatch<React.SetStateAction<number[]>>;
}
export interface ContextType {
  dataArrayLength: number;
  collapse: boolean;
  setCollapse: React.Dispatch<React.SetStateAction<boolean>>;
  originalQueryData: Number[];
  clearIntervalWrapper: () => void;
  maxDiff: number;
  isChangeable: boolean;
  loadingStates: loadingStates[];
  setLoadingStates: React.Dispatch<React.SetStateAction<loadingStates[]>>;
  setIntervalData: React.Dispatch<React.SetStateAction<number>>;
  setGroupDataBool: React.Dispatch<React.SetStateAction<boolean>>;
  unfoldData: (index: number) => void;
  SetExplanation: (
    index: string,
    explanation: string,
    modelName: string
  ) => void;
  createData: (
    databaseData: any,
    aggFunction: string,
    database: string
  ) => any[];
  loading: boolean;
  intervalData: number;
  top: number;
  addChart: () => void;
  setNormalizedData: React.Dispatch<React.SetStateAction<DataType[]>>;
  normalizedData: DataType[];
  groupDataBool: boolean;

  setSelectedDatabase: (databse: string) => void;
  selectedDatabase: string;

  collapsed: boolean;
  setCollapsed: React.Dispatch<React.SetStateAction<boolean>>;
  startCalculation: () => Promise<void>;
  stopCalculation: () => Promise<void>;
  clearData: (interval: number) => void;
  setTop: React.Dispatch<React.SetStateAction<number>>;
  selectedGroupBy: number;

  setSelectedGroupBy: React.Dispatch<React.SetStateAction<number>>;
  selectedCompare1: number;
  selectedCompare2: number;

  setSelectedCompare1: React.Dispatch<React.SetStateAction<number>>;
  setSelectedCompare2: React.Dispatch<React.SetStateAction<number>>;

  aggregateFunction: number;
  setAggregateFunction: (value: any) => void;
  setExample: (
    database: string,
    groupBy: number,
    compare1: number,
    compare2: number,
    aggregateFunction: number
  ) => void;
}
export interface FullData {
  data: DatabaseData[];
  grouped: { best: DatabaseData; fullList: DatabaseData[] }[];
}
export interface DatabaseData {
  number1: number;
  number2: number;
  number3: number;
  number4: number;
  number5: number;
  attribute1: string;
  attribute2: string;
  value1: string;
  value2: string;
  mean1: number;
  N1: number;
  mean2: number;
  N2: number;
}
export interface PopupComponentProps {
  isTitle: boolean;
  text: string;
  className: string;
  idName: string;
  titleName: string;
}
export interface DataHeaderProps {
  dataValues: any;
  index: number;
  aggregateFunction: string;
}
export interface DataDisplayProps {
  dataValues: any;
  setPredicateText: React.Dispatch<React.SetStateAction<JSX.Element>>;
  setHoveredData: React.Dispatch<React.SetStateAction<Dataset[] | null>>;
  index: number;
  highlightedIndex: string;
  setHighlightedIndex: React.Dispatch<React.SetStateAction<string>>;
  father: boolean;
}

export interface AttrHeaderProps {
  title: string;
  attribute1Name: string;
  attribute2Name: string;
  aggregateFunction: string;
}
