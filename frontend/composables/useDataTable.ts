import { ref } from "vue";
import type { Ref, UnwrapRef } from "vue";

interface TableState {
  skip: number;
  limit: number;
  order: Array<any>;
  search: string | undefined;
  filters: Array<any>;
}

export function useDataTable(): {
  state: Ref<UnwrapRef<TableState>>;
  onStateChange: (newState: TableState) => void;
} {
  const defaultState: TableState = {
    skip: 0,
    limit: 10,
    order: [],
    search: undefined,
    filters: [],
  };
  const state = ref<TableState>(defaultState);

  function onStateChange(newState: TableState) {
    state.value = newState;
  }

  return { state, onStateChange };
}
