<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
  title: "Home"
})

useHead({
  title: "Home"
})

const authStore = useAuthStore()
const { state: auth } = storeToRefs(authStore)
</script>

<template>
  <p class="text-2xl">
    Hi <span class="font-bold">{{ auth.user.name }}</span
    >, welcome back!
  </p>
</template>
