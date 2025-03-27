<script setup lang="ts">
import type { Column } from "@tanstack/vue-table";
import {
  ArrowDown,
  ArrowUp,
  ArrowUpDown,
  Equal,
  EyeOff,
  Pin,
} from "lucide-vue-next";

import { cn } from "@/lib/utils";
import { Button } from "~/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";

interface DataTableColumnHeaderProps {
  column: Column<any>;
  title: string;
}

defineProps<DataTableColumnHeaderProps>();
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
};
</script>

<template>
  <div
    v-if="column.getCanSort()"
    :class="cn('flex items-center space-x-2', $attrs.class ?? '')"
  >
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Button
          variant="ghost"
          size="sm"
          class="-ml-3 h-8 data-[state=open]:bg-accent"
        >
          <span class="font-bold">{{ title }}</span>
          <ArrowDown
            v-if="column.getIsSorted() === 'desc'"
            class="ml-2 h-4 w-4"
          />
          <ArrowUp
            v-else-if="column.getIsSorted() === 'asc'"
            class="ml-2 h-4 w-4"
          />
          <ArrowUpDown v-else class="ml-2 h-3.5 w-3.5" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start">
        <DropdownMenuItem
          v-if="column.getIsSorted() !== false"
          @click="column.clearSorting()"
        >
          <Equal class="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
          No Sort
        </DropdownMenuItem>
        <DropdownMenuItem
          v-if="column.getIsSorted() !== 'asc'"
          @click="column.toggleSorting(false)"
        >
          <ArrowUp class="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
          Sort Ascending
        </DropdownMenuItem>
        <DropdownMenuItem
          v-if="column.getIsSorted() !== 'desc'"
          @click="column.toggleSorting(true)"
        >
          <ArrowDown class="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
          Sort Descending
        </DropdownMenuItem>
        <DropdownMenuSeparator v-if="column.getCanHide()" />
        <DropdownMenuItem
          v-if="column.getCanHide()"
          @click="column.toggleVisibility(false)"
        >
          <EyeOff class="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
          Hide Column
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          v-if="column.getCanPin() && !column.getIsPinned()"
          @click="column.pin('left')"
        >
          <Pin class="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
          Pin Column
        </DropdownMenuItem>
        <DropdownMenuItem
          v-if="column.getIsPinned()"
          @click="column.pin(false)"
        >
          <Pin class="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
          Unpin Column
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </div>
  <div v-else :class="$attrs.class" class="font-bold">
    {{ title }}
  </div>
</template>
