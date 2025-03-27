<script setup lang="ts">
import type { Row } from "@tanstack/vue-table";
import { EllipsisVertical, Pencil, Trash } from "lucide-vue-next";

import { Button } from "~/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";

interface DataTableRowActionsProps {
  row: Row<any>;
}

const props = defineProps<DataTableRowActionsProps>();

function handleClick(e: Event) {
  console.log(props.row.original);
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button
        variant="ghost"
        class="flex h-8 w-8 p-0 data-[state=open]:bg-muted"
      >
        <EllipsisVertical class="h-4 w-4" />
        <span class="sr-only">Open menu</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end" class="w-[160px]">
      <DropdownMenuItem class="cursor-pointer" @click="handleClick">
        <Pencil class="size-4 mr-3" />
        Edit
      </DropdownMenuItem>
      <DropdownMenuItem class="cursor-pointer">
        <Trash class="size-4 mr-3" />
        Delete
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
