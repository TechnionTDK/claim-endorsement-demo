import { useEffect, MutableRefObject, useRef } from "react";
export const useUpdateRef = <T>(value: T): MutableRefObject<T> => {
  const ref = useRef<T>(value);

  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref;
};
