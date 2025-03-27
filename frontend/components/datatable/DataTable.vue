<script setup lang="ts">
import type {
  Column,
  ColumnDef,
  ColumnFiltersState,
  PaginationState,
  SortingState,
  VisibilityState,
} from "@tanstack/vue-table";
import {
  FlexRender,
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from "@tanstack/vue-table";
import { ref } from "vue";
import DataTablePagination from "./DataTablePagination.vue";
import DataTableToolbar from "./DataTableToolbar.vue";
import { valueUpdater } from "~/lib/utils";
import { LoaderCircle } from "lucide-vue-next";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table";

interface DataTableProps {
  controlled: boolean;
  columns: ColumnDef<any>[];
  data: any[];
  rowCount: number | undefined;
  loading: boolean;
}

const props = withDefaults(defineProps<DataTableProps>(), {
  controlled: false,
  rowCount: undefined,
  loading: false,
});
const emit = defineEmits(["change"]);

const pagination = ref<PaginationState>({ pageSize: 10, pageIndex: 0 });
const sorting = ref<SortingState>([]);
const search = ref<string | undefined>(undefined);
const columnFilters = ref<ColumnFiltersState>([]);
const columnVisibility = ref<VisibilityState>({});
const rowSelection = ref({});

const pageSize = computed(() => pagination.value.pageSize);
const skip = computed(
  () => pagination.value.pageSize * pagination.value.pageIndex,
);

const table = useVueTable({
  get columns() {
    return props.columns;
  },
  get data() {
    return props.data || [];
  },
  get rowCount() {
    return props.controlled ? props.rowCount || 0 : (props.data || []).length;
  },
  state: {
    get sorting() {
      return sorting.value;
    },
    get pagination() {
      return pagination.value;
    },
    get columnFilters() {
      return columnFilters.value;
    },
    get columnVisibility() {
      return columnVisibility.value;
    },
    get globalFilter() {
      return search.value;
    },
    get rowSelection() {
      return rowSelection.value;
    },
  },
  getRowId: (row) => row.uid,
  enableRowSelection: false,
  manualPagination: props.controlled,
  manualSorting: props.controlled,
  manualFiltering: props.controlled,
  onPaginationChange: (updaterOrValue: any) =>
    valueUpdater(updaterOrValue, pagination),
  onSortingChange: (updaterOrValue: any) =>
    valueUpdater(updaterOrValue, sorting),
  onGlobalFilterChange: (updaterOrValue: any) =>
    valueUpdater(updaterOrValue, search),
  onColumnFiltersChange: (updaterOrValue: any) =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: (updaterOrValue: any) =>
    valueUpdater(updaterOrValue, columnVisibility),
  onRowSelectionChange: (updaterOrValue: any) =>
    valueUpdater(updaterOrValue, rowSelection),
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFacetedRowModel: getFacetedRowModel(),
  getFacetedUniqueValues: getFacetedUniqueValues(),
});

function getPinnedClasses(column: Column<any>) {
  if (column.getIsPinned()) {
    return `sticky left-0 z-10 shadow-xl shadow-black dark:shadow-white bg-background`;
  } else {
    return "relative";
  }
}

watch([pagination, sorting, search, columnFilters], () => {
  emit("change", {
    skip: toRaw(skip.value),
    limit: toRaw(pageSize.value),
    order: toRaw(sorting.value),
    search: toRaw(search.value),
    filters: toRaw(columnFilters.value),
  });
});
</script>

<template>
  <div class="relative space-y-2">
    <div
      v-if="loading"
      class="z-10 absolute bg-white/50 dark:bg-black/50 flex justify-center items-center w-full h-full"
    >
      <LoaderCircle class="size-12 animate-spin" />
    </div>
    <DataTableToolbar :table="table" />
    <div class="rounded-md border overflow-x-scroll">
      <Table>
        <TableHeader>
          <TableRow
            v-for="headerGroup in table.getHeaderGroups()"
            :key="headerGroup.id"
          >
            <TableHead
              v-for="header in headerGroup.headers"
              :key="header.id"
              :class="getPinnedClasses(header.column)"
            >
              <FlexRender
                v-if="!header.isPlaceholder"
                :render="header.column.columnDef.header"
                :props="header.getContext()"
              />
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <template v-if="table.getRowModel().rows?.length">
            <TableRow
              v-for="row in table.getRowModel().rows"
              :key="row.id"
              :data-state="row.getIsSelected() && 'selected'"
            >
              <TableCell
                v-for="cell in row.getVisibleCells()"
                :key="cell.id"
                :class="getPinnedClasses(cell.column)"
              >
                <FlexRender
                  :render="cell.column.columnDef.cell"
                  :props="cell.getContext()"
                />
              </TableCell>
            </TableRow>
          </template>
          <TableRow v-else>
            <TableCell :colspan="columns.length" class="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
    <DataTablePagination :table="table" />
  </div>
</template>
