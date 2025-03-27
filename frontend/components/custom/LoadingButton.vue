<script setup>
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-vue-next";

const props = defineProps({
  loading: { type: Boolean, default: false },
});
</script>

<template>
  <Button :disabled="loading">
    <Loader2 v-if="loading" class="w-4 h-4 mr-2 animate-spin" />
    <template v-if="loading">
      <slot name="loading">Loading...</slot>
    </template>
    <template v-else>
      <slot name="default">Login</slot>
    </template>
  </Button>
</template>
