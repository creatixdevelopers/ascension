<script setup lang="ts">
import type { NuxtError } from "#app";
import { CornerUpLeft } from "lucide-vue-next";

useHead({ title: "Error" });

const props = defineProps({
  error: Object as () => NuxtError,
});

const handleError = () => {
  clearError({ redirect: "/" });
};
</script>

<template>
  <NuxtLayout name="auth">
    <div class="flex justify-center items-center min-h-screen w-full">
      <div class="flex flex-col items-center">
        <h2 class="text-center text-6xl mb-5">
          {{ error ? error.statusCode : 404 }}
        </h2>
        <div v-if="error?.statusCode == 404">
          <p class="text-center">Looks like you may have taken a wrong turn.</p>
          <p class="text-center">
            Don't worry... it happens to the best of us. Let's get you back on
            track.
          </p>
        </div>
        <div v-else-if="error?.statusCode == 500">
          <p class="text-center">Oops, something went wrong!</p>
          <p class="text-center">We'll get it fixed soon</p>
        </div>
        <Button class="mt-5" @click="handleError">
          <CornerUpLeft class="h-4 w-4 me-1" />
          Return Home
        </Button>
      </div>
    </div>
  </NuxtLayout>
</template>
