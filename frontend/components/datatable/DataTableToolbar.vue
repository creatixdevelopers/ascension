<script setup lang="ts">
import type { Table } from "@tanstack/vue-table";

import DataTableViewOptions from "./DataTableViewOptions.vue";
import { Input } from "~/components/ui/input";
import { Search } from "lucide-vue-next";
import { useDebounceFn } from "@vueuse/core";

interface DataTableToolbarProps {
  table: Table<any>;
}

const props = defineProps<DataTableToolbarProps>();

const setGlobalFilter = useDebounceFn((value: string) => {
  props.table.setGlobalFilter(value);
}, 1000);
</script>

<template>
  <div class="flex items-center justify-between">
    <div class="relative w-full max-w-sm items-center">
      <span
        class="absolute start-0 inset-y-0 flex items-center justify-center px-2"
      >
        <Search class="size-3 text-muted-foreground" />
      </span>
      <Input
        placeholder="Search..."
        class="h-8 w-[150px] lg:w-[250px] pl-7"
        @input="setGlobalFilter($event.target.value)"
      />
    </div>
    <DataTableViewOptions :table="table" />
  </div>
</template>
