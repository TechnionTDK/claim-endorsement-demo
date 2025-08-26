import { useEffect, useState } from "react";
import * as React from "react";
import { createData } from "./utils/createChart";
import "./css/App.css";
import MySideBar from "./sidebar/MySideBar";

import DataDisplay from "./TableDispaly/dataDisplay";
import InfiniteScroll from "react-infinite-scroll-component";

import {
  checksortFunction,
  TranslateForURL,
  TranslatePath,
} from "./utils/utilFunctions";
import {
  GetData,
  retrieveOriginalQuery,
  StartCalculationWrapper,
  StopCalculationWrapper,
} from "./BL/FetchFunctions";
import {
  Data,
  DataType,
  Dataset,
  ContextType,
  FullData,
  loadingStates,
} from "./utils/interfaces";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

import { translateDB } from "./utils/dataDump";
import { useUpdateRef } from "./utils/MyRefHook";
import { addChart } from "./utils/addChart";
import { message } from "./UtilComps/message";
import DataDisplayOriginalQuery from "./TableDispaly/dataDisplayOriginalQuery";
import TableDisplayHeader from "./TableDispaly/tableDisplayHeader";

export const MyContext = React.createContext<ContextType | null>(null);

function App() {
  const [loading, setLoading] = useState(false);
  const [databaseData, setDatabaseData] = useState<FullData>({
    data: [],
    grouped: [],
  });
  const [index, setIndex] = useState(0);
  const [intervalData, setIntervalData] = useState<number>(0);
  const [highlightedIndex, setHighlightedIndex] = useState<string>("-1");
  const [collapsed, setCollapsed] = useState(false);
  const [selectedDatabase, setSelectedDatabase] = useState("Stack Overflow");
  const [selectedGroupBy, setSelectedGroupBy] = useState(0);
  const [selectedCompare1, setSelectedCompare1] = useState(0);
  const [selectedCompare2, setSelectedCompare2] = useState(1);
  const [aggregateFunction, setAggregateFunction] = useState(0);
  const [groupDataBool, setGroupDataBool] = useState(false);
  const [top, setTop] = useState(10);
  const [data, setData] = useState<Data[] | null>(null);
  const [SortedData, setSortedData] = useState<Data[] | null>(null);
  const [hoveredData, setHoveredData] = useState<Dataset[] | null>(null);
  const [normalizedData, setNormalizedData] = useState<DataType[]>([
    { value: 100, name: "0" },
    { value: 100, name: "1" },
    { value: 100, name: "2" },
    { value: 100, name: "3" },
    { value: 100, name: "4" },
  ]);
  const [maxDiff, setMaxDiff] = useState<number>(0);
  const [isChangeable, setIsChangeable] = useState<boolean>(true);
  const [loadingStates, setLoadingStates] = useState<loadingStates[]>([]);
  const [predicateText, setPredicateText] = useState<JSX.Element>(<div></div>);
  const [sortingOptions, setSortingOptions] = useState<number[]>([0, 0]);
  const [originalQueryData, setOriginalQueryData] = useState<number[]>([
    0, 0, 0, 0,
  ]);
  const normRef = useUpdateRef(normalizedData);
  const sortedRef = useUpdateRef(SortedData);
  const normRef2 = useUpdateRef(databaseData);
  const topRef = useUpdateRef(top);
  const normIndex = useUpdateRef(index);
  const intervalref = useUpdateRef(intervalData);
  const isChangeableRef = useUpdateRef(isChangeable);
  const clearIntervalWrapper = () => {
    clearInterval(intervalref.current);
    setIntervalData(0);
    setLoading(false);
  };
  useEffect(() => {
    setSortedData(() => {
      if (data) {
        return [...data].sort(checksortFunction(normRef, sortingOptions));
      }
      return data;
    });
  }, [data, sortingOptions, normalizedData]);
  useEffect(() => {
    if (intervalData) {
      setIsChangeable(false);
      return;
    }
    if (SortedData) return;
    setIsChangeable(true);
  }, [intervalData, SortedData]);
  const stopCalculation = async () => {
    setIsChangeable(true);
    setLoading(false);
    const filepath = translateDB[selectedDatabase];
    await StopCalculationWrapper(filepath);
    setIndex(0);
    setDatabaseData({
      data: [],
      grouped: [],
    });
    /*console.log("getting here");*/
  };

  const startCalculation = async () => {
    try {
      setOriginalQueryData([0, 0, 0, 0]);
      setIsChangeable(false);
      setHighlightedIndex("-1");
      setHoveredData(null);
      setTop(10);
      //console.log("has started");
      setSelectedDatabase(selectedDatabase);

      let { db, agg, grp, g1, g2 } = TranslateForURL(
        selectedDatabase,
        aggregateFunction,
        selectedGroupBy,
        selectedCompare1,
        selectedCompare2
      );
      // console.log(db, agg, grp, g1, g2);

      await StartCalculationWrapper(db, agg, grp, g1, g2);

      setLoading(true);
      setTimeout(async () => {
        var x = await StartIntervalFetch(groupDataBool);
        setIntervalData(x);
      }, 1000);
      setTimeout(async () => {
        var originalQueryData = await retrieveOriginalQuery();
        do {
          originalQueryData = await retrieveOriginalQuery();
        } while (
          originalQueryData[0] == 0 &&
          originalQueryData[1] == 0 &&
          originalQueryData[2] == 0 &&
          originalQueryData[3] == 0
        );
        setOriginalQueryData([...originalQueryData]);
      }, 2000);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  const fetchData = async (group: boolean) => {
    try {
      const index = translateDB[selectedDatabase];
      const combinedData = await GetData(normIndex.current, index);

      //console.log(data);
      if (combinedData == null) {
        if (!normRef || normRef.current.length == 0) {
          alert(
            "this query resulted in no results, please try another one dfhsdjfhkjsdhfjkdshfkjdshfjkd"
          );
        }

        clearIntervalWrapper();
        await stopCalculation();
        return;
      }
      const { dataUnit, grouped } = combinedData;

      let onlyData: FullData;
      //console.log("this is the data");

      onlyData = { data: dataUnit, grouped };

      setDatabaseData({ ...onlyData });
      setIndex((old) => old + dataUnit.length);
      if (dataUnit.length == 0) {
        clearIntervalWrapper();
        setLoading(false);
      }
      addChart(
        normRef2,
        setData,
        aggregateFunction,
        selectedDatabase,
        setMaxDiff,
        group
      )();
    } catch (error) {
      // console.error("Error fetching data:", error);
    }
  };

  const StartIntervalFetch = (group: boolean) => {
    const interval = setInterval(() => {
      fetchData(group);
    }, 2000);
    return interval;
  };

  const unfoldData = (index: number) => {
    // console.log(SortedData);

    setSortedData((old) => {
      if (old == null) return null;
      const newData = [...old];
      return newData.map((value: any) => {
        if (value.index == index) {
          value.unfolded = !value.unfolded;
        }
        return value;
      });
    });
  };
  const SetExplanation = (
    index: string,
    explanation: string,
    modelName: string
  ) => {
    //  console.log(index);

    if (groupDataBool) {
      setSortedData((old) => {
        if (old == null) return null;
        const newData = [...old];
        return newData.map((value: any) => {
          //   console.log(index.split(" and "));

          //   console.log(value.index == `${index.split(" and ")[0]} and 0`);

          if (value.index == `${index.split(" and ")[0]} and 0`) {
            value = {
              ...value,
              fullList: value.fullList.map((value2: any) => {
                // console.log(index.split(" and ")[1]);

                if (value2.index == index) {
                  value2.explanation = { explanation, modelName };
                }
                return value2;
              }),
            };
          }
          return value;
        });
      });
    } else {
      setSortedData((old) => {
        if (old == null) return null;
        const newData = [...old];
        return newData.map((value: any) => {
          if (value.index == index) {
            value.explanation = { explanation, modelName };
          }
          return value;
        });
      });
    }
    setSortedData((old) => {
      if (old == null) return null;
      const newData = [...old];
      return newData.map((value: any) => {
        if (value.index == index) {
          value.explanation = { explanation, modelName };
        }
        return value;
      });
    });
  };
  const setExample = (
    database: string,
    groupBy: number,
    compare1: number,
    compare2: number,
    aggregateFunction: number
  ) => {
    // console.log("this is the groupby", groupBy);

    setSelectedDatabase(database);
    setSelectedGroupBy(groupBy);
    setSelectedCompare1(compare1);
    setSelectedCompare2(compare2);
    setAggregateFunction(aggregateFunction);
  };

  const clearData = (interval: number) => {
    clearIntervalWrapper();

    setData([]);
  };

  // Temporary copies
  const changeDatabase = (database: string) => {
    setSelectedGroupBy(0);
    setSelectedCompare1(0);
    setSelectedCompare2(1);
    setAggregateFunction(0);
    setSelectedDatabase(database);
  };
  const [hasMoreData, setHasMoreData] = useState(true);

  // Modify the useEffect that watches SortedData
  useEffect(() => {
    // Update hasMoreData based on current data
    if (SortedData) {
      setHasMoreData(SortedData.length > top || loading);
    }
  }, [SortedData, top, loading]);

  return (
    <div id="mainDiv">
      <MyContext.Provider
        value={{
          originalQueryData,
          clearIntervalWrapper,
          maxDiff,
          isChangeable: isChangeableRef.current,
          setLoadingStates,
          loadingStates,
          unfoldData,
          createData,
          loading,
          top,
          setTop,
          setExample,
          addChart: addChart(
            normRef2,
            setData,
            aggregateFunction,
            selectedDatabase,
            setMaxDiff,
            groupDataBool
          ),
          normalizedData,
          setNormalizedData,
          startCalculation,
          stopCalculation,
          clearData,
          setCollapsed,
          groupDataBool,
          collapsed,
          selectedDatabase,
          setSelectedDatabase: changeDatabase,

          selectedGroupBy,

          setSelectedGroupBy,
          selectedCompare1,

          setSelectedCompare1,
          selectedCompare2,

          setSelectedCompare2,
          aggregateFunction,

          setAggregateFunction,
          setGroupDataBool,
          intervalData: intervalref.current,
          SetExplanation,
          setIntervalData,
        }}
      >
        <MySideBar></MySideBar>

        <div style={{ width: "80vw" }}>
          <TableDisplayHeader
            hoveredData={hoveredData}
            predicateText={predicateText}
            sortingOptions={sortingOptions}
            setSortingOptions={setSortingOptions}
          ></TableDisplayHeader>

          <div>
            {originalQueryData[0] == 0 &&
            originalQueryData[1] == 0 &&
            originalQueryData[2] == 0 &&
            originalQueryData[3] == 0 ? (
              <div></div>
            ) : (
              <DataDisplayOriginalQuery></DataDisplayOriginalQuery>
            )}

            <InfiniteScroll
              scrollThreshold={0.2}
              style={{ overflow: "visible" }} // Add this to prevent scroll issues
              dataLength={top}
              next={() => {
                console.log("in next");

                setTop((old) => {
                  if (sortedRef.current == null) return 0;

                  return old + 10 > sortedRef.current.length ? old : old + 10;
                });
              }}
              hasMore={hasMoreData}
              loader={<h4>Loading... Don't worry, this may take a while</h4>}
              endMessage={<div>hello There</div>}
            >
              {SortedData === null ? (
                <div id="no_data">
                  {" "}
                  <div>this is where the data will be displayed</div>
                </div>
              ) : (
                SortedData.slice(0, top).map((dataValues, index) => (
                  <DataDisplay
                    key={index}
                    dataValues={dataValues}
                    index={index}
                    setPredicateText={setPredicateText}
                    setHoveredData={setHoveredData}
                    highlightedIndex={highlightedIndex}
                    setHighlightedIndex={setHighlightedIndex}
                    father={true}
                  ></DataDisplay>
                ))
              )}
            </InfiniteScroll>
          </div>
        </div>
      </MyContext.Provider>
    </div>
  );
}

export default App;
