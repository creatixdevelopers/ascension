<script setup lang="ts">
import { ChevronLeft, ChevronRight, Home, Users } from "lucide-vue-next";

const props = defineProps(["collapsed"]);
</script>

<template>
  <div class="hidden border-r bg-muted/40 md:block">
    <div class="flex h-full max-h-screen flex-col gap-2">
      <div
        class="relative flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6"
      >
        <NuxtLink to="/" class="flex items-center gap-2 font-semibold">
          {{ collapsed ? "A" : "Acme Inc" }}
        </NuxtLink>
        <Button
          class="rounded-full absolute right-0 translate-x-1/2 z-50"
          variant="outline"
          size="icon"
          @click="$emit('toggleSidebar')"
        >
          <ChevronRight v-if="collapsed" class="w-4 h-4" />
          <ChevronLeft v-else class="w-4 h-4" />
        </Button>
      </div>
      <nav
        class="flex flex-col gap-2 px-2 text-sm font-medium lg:px-4"
        :class="{ 'items-center': collapsed, 'items-start': !collapsed }"
      >
        <NuxtLink
          class="flex items-center rounded-lg p-2 text-muted-foreground hover:bg-accent transition-all"
          :class="{ 'w-fit': collapsed, 'w-full': !collapsed }"
          activeClass="bg-primary hover:bg-primary text-white dark:text-black"
          to="/"
        >
          <Home class="h-4 w-4" />
          <p v-if="!collapsed" class="ml-2">Home</p>
        </NuxtLink>
        <NuxtLink
          class="flex items-center rounded-lg p-2 text-muted-foreground hover:bg-accent transition-all"
          :class="{ 'w-fit': collapsed, 'w-full': !collapsed }"
          activeClass="bg-primary hover:bg-primary text-white dark:text-black"
          to="/users"
        >
          <Users class="h-4 w-4" />
          <p v-if="!collapsed" class="ml-2">Users</p>
        </NuxtLink>
      </nav>
    </div>
  </div>
</template>

<style scoped></style>
