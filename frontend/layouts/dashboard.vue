<script setup lang="ts">
import Header from "~/components/layout/Header.vue";
import Sidebar from "~/components/layout/Sidebar.vue";

const colorMode = useColorMode();

const sidebarCollapsed = ref(false);
const isDark = computed(() => colorMode.value === "dark");

function handleSidebarCollapseToggle() {
  sidebarCollapsed.value = !sidebarCollapsed.value;
}
</script>

<template>
  <div
    class="grid min-h-screen w-full transition-all"
    :class="{
      'md:grid-cols-[250px_1fr]': !sidebarCollapsed,
      'md:grid-cols-[60px_1fr]': sidebarCollapsed,
      'bg-neutral-950 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]':
        isDark,
      'bg-white bg-[radial-gradient(120%_80%_at_50%_-10%,rgba(0,163,255,0.2)_0,rgba(0,163,255,0.08)_50%,rgba(0,163,255,0)_100%)]':
        !isDark,
    }"
  >
    <Sidebar
      :collapsed="sidebarCollapsed"
      @toggleSidebar="handleSidebarCollapseToggle"
    />
    <div class="flex flex-col">
      <Header />
      <main
        class="flex flex-1 flex-col gap-2 p-4 lg:gap-2 lg:px-8 overflow-x-scroll transition-all"
        :class="{
          'md:max-w-[calc(100vw-250px)]': !sidebarCollapsed,
          'md:max-w-[calc(100vw-60px)]': sidebarCollapsed,
        }"
      >
        <slot />
      </main>
    </div>
  </div>
</template>
