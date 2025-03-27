<script setup lang="ts">
const colorMode = useColorMode()
const isDark = computed(() => colorMode.value === "dark")
</script>
<template>
  <div
    :class="{
      'bg-neutral-950 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]':
        isDark,
      'bg-white bg-[radial-gradient(120%_80%_at_50%_-10%,rgba(0,163,255,0.2)_0,rgba(0,163,255,0.08)_50%,rgba(0,163,255,0)_100%)]':
        !isDark
    }"
    class="absolute top-0 z-[-2] h-screen w-screen"
  >
    <slot />
  </div>
</template>
