import { createData } from "./createChart";
import { aggregateFunctions } from "./dataDump";
import { Data, FullData } from "./interfaces";

const addChartFull = (
  normRef2: React.MutableRefObject<FullData>,
  setData: (value: React.SetStateAction<Data[] | null>) => void,
  aggregateFunction: number,
  selectedDatabase: string,
  setMaxDiff: (value: React.SetStateAction<number>) => void
): (() => void) => {
  return () => {
    if (normRef2.current.data.length == 0) return;
    setData((oldValues) => {
      if (normRef2.current.data.length == 0) return null;

      if (oldValues)
        return removeDups([
          ...oldValues,
          ...createData(
            normRef2.current.data,
            aggregateFunctions[aggregateFunction],
            selectedDatabase
          ),
        ]).map((value, index) => {
          setMaxDiff((prev) => {
            if (value.datasets[1].data > prev) {
              return value.datasets[1].data;
            }
            return prev;
          });

          return { ...value, index: `${index}` };
        });
      else
        return removeDups(
          createData(
            normRef2.current.data,
            aggregateFunctions[aggregateFunction],
            selectedDatabase
          )
        ).map((value: any, index: any) => {
          setMaxDiff((prev) => {
            if (value.datasets[1].data > prev) {
              return value.datasets[1].data;
            }
            return prev;
          });
          return { ...value, index: index };
        });
    });
  };
};

function addUniqueItems(originalList: any[], newItems: any[]): any[] {
  // Create a Map with original items first

  const uniqueMap = new Map(originalList.map((item) => [item.uniqueKey, item]));

  // Only add new items if their key doesn't exist
  newItems.forEach((item) => {
    const key = item.uniqueKey;
    if (!uniqueMap.has(key)) {
      uniqueMap.set(key, item);
    }
  });

  return Array.from(uniqueMap.values());
}

const removeDups = (data: Data[]): Data[] => {
  console.log("data length");

  console.log(data.length);

  const uniqueMap = new Map();
  const uniqueData = [...data];
  uniqueData.forEach((item) => {
    uniqueMap.set(item.uniqueKey, item);
  });
  let filtered = Array.from(uniqueMap.values());
  console.log("filtered length");
  console.log(filtered.length);
  return filtered;
};
const addChartCompact = (
  normRef2: React.MutableRefObject<FullData>,
  setData: (value: React.SetStateAction<Data[] | null>) => void,
  aggregateFunction: number,
  selectedDatabase: string,
  setMaxDiff: (value: React.SetStateAction<number>) => void
): (() => void) => {
  return () => {
    if (normRef2.current.data.length == 0) return;

    setData((oldValues) => {
      if (normRef2.current.data.length == 0) return;

      if (oldValues)
        return addUniqueItems(
          oldValues,
          createData(
            normRef2.current,
            aggregateFunctions[aggregateFunction],
            selectedDatabase,
            true
          )
        ).map((value: any, index: any) => {
          return {
            ...value,
            fullList: value.fullList.map((value2: any, myIndex: any) => {
              setMaxDiff((prev) => {
                if (value.datasets[1].data > prev) {
                  return value.datasets[1].data;
                }
                return prev;
              });
              return { ...value2, index: `${index} and ${myIndex}` };
            }),

            index: `${index} and 0`,
          };
        });
      else {
        const val = createData(
          normRef2.current,
          aggregateFunctions[aggregateFunction],
          selectedDatabase,
          true
        ).map((value: any, index: any) => {
          return {
            ...value,
            fullList: value.fullList.map((value2: any, myIndex: any) => {
              setMaxDiff((prev) => {
                if (value.datasets[1].data > prev) {
                  return value.datasets[1].data;
                }
                return prev;
              });
              return { ...value2, index: `${index} and ${myIndex}` };
            }),

            index: index,
          };
        });

        return val;
      }
    });
  };
};
export function addChart(
  normRef2: React.MutableRefObject<FullData>,
  setData: (value: React.SetStateAction<Data[] | null>) => void,
  aggregateFunction: number,
  selectedDatabase: string,
  setMaxDiff: (value: React.SetStateAction<number>) => void,
  isCompact = false
): () => void {
  if (isCompact) {
    return addChartCompact(
      normRef2,
      setData,
      aggregateFunction,
      selectedDatabase,
      setMaxDiff
    );
  } else {
    return addChartFull(
      normRef2,
      setData,
      aggregateFunction,
      selectedDatabase,
      setMaxDiff
    );
  }
}
