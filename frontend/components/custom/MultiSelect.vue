<script setup lang="ts">
import type { ComputedRef, Ref } from "vue";
import { ref } from "vue";
import { Check, ChevronDown } from "lucide-vue-next";

import { cn } from "@/lib/utils";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  TagsInput,
  TagsInputItem,
  TagsInputItemDelete,
  TagsInputItemText,
} from "@/components/ui/tags-input";

type optionType = {
  label: string;
  value: string;
};

const props = defineProps({
  options: {
    type: [Array<string>, Array<optionType>],
    required: true,
  },
  placeholder: { type: String, required: false, default: "" },
});

const open: Ref<boolean | undefined> = ref(false);
const selectedOptions: Ref<Array<optionType>> = ref([]);
const formattedOptions: ComputedRef<Array<optionType>> = computed(() => {
  return props.options.map((opt) => {
    if (typeof opt === "object") {
      return opt;
    } else {
      return { label: opt, value: opt };
    }
  });
});

function displayValue(value: optionType) {
  return value.label;
}

function isSelected(value: string) {
  return selectedOptions.value.find((opt: optionType) => opt.value === value);
}

function handleOptionClick(option: optionType) {
  if (isSelected(option.value)) {
    selectedOptions.value = selectedOptions.value.filter(
      (opt: optionType) => opt.value !== option.value,
    );
  } else {
    selectedOptions.value = [...selectedOptions.value, option];
  }
}
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <TagsInput v-model="selectedOptions" :display-value="displayValue">
        <TagsInputItem
          v-for="(item, i) in selectedOptions"
          :key="i"
          :value="item"
        >
          <TagsInputItemText />
          <TagsInputItemDelete />
        </TagsInputItem>
        <p class="flex-1 text-gray-400">
          {{ selectedOptions.length > 0 ? "" : placeholder }}
        </p>
        <ChevronDown
          class="transition-all transform opacity-50"
          :class="{ 'rotate-180': open }"
        />
      </TagsInput>
    </PopoverTrigger>
    <PopoverContent
      align="start"
      class="p-0"
      style="width: var(--radix-popover-trigger-width)"
    >
      <Command>
        <CommandInput class="h-9" placeholder="Search framework..." />
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandList>
          <CommandGroup>
            <CommandItem
              v-for="option in formattedOptions"
              :key="option.value"
              :value="option.label"
              @select="
                (ev) => {
                  handleOptionClick(option);
                }
              "
            >
              {{ option.label }}
              <Check
                :class="
                  cn(
                    'ml-auto h-4 w-4',
                    isSelected(option.value) ? 'opacity-100' : 'opacity-0',
                  )
                "
              />
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>
