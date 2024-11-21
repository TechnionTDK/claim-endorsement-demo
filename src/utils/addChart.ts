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
      if (normRef2.current.data.length == 0) return;

      if (oldValues)
        return [
          ...oldValues,
          ...createData(
            normRef2.current.data,
            aggregateFunctions[aggregateFunction],
            selectedDatabase
          ),
        ].map((value, index) => {
          setMaxDiff((prev) => {
            if (value.datasets[1].data > prev) {
              return value.datasets[1].data;
            }
            return prev;
          });

          return { ...value, index: `${index}` };
        });
      else
        return createData(
          normRef2.current.data,
          aggregateFunctions[aggregateFunction],
          selectedDatabase
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
        return [
          ...oldValues,
          ...createData(
            normRef2.current,
            aggregateFunctions[aggregateFunction],
            selectedDatabase,
            true
          ),
        ].map((value: any, index: any) => {
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
