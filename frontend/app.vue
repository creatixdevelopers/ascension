<script setup lang="ts">
import { ConfigProvider } from "radix-vue";
import { Toaster } from "@/components/ui/sonner";

const useIdFunction = () => useId();
</script>

<template>
  <!-- Required to fix hydration mismatch errors with radix-vue/shadcn components -->
  <ConfigProvider :use-id="useIdFunction">
    <NuxtLayout>
      <Toaster richColors />
      <NuxtPage />
    </NuxtLayout>
  </ConfigProvider>
</template>
