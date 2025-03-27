<script setup lang="ts">
import {
  Home,
  LogOut,
  Menu,
  Moon,
  SquareUserRound,
  Sun,
  UserRound,
  Users,
} from "lucide-vue-next";
import { Button } from "~/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

const { state, logout } = useAuthStore();
const colorMode = useColorMode();
const route = useRoute();

function toggleTheme(): void {
  colorMode.preference = colorMode.preference === "light" ? "dark" : "light";
}

async function handleLogout(): Promise<void> {
  const { status } = await logout();
  if (status) {
    navigateTo("/login");
  }
}
</script>

<template>
  <header
    class="sticky top-0 z-40 flex h-14 items-center gap-4 px-4 lg:h-[60px] lg:px-8 lg:pr-6 bg-white/50 dark:bg-neutral-900/50 backdrop-blur-xl border-b border-white/20 dark:border-neutral-800/50"
  >
    <Sheet>
      <SheetTrigger as-child>
        <Button variant="outline" size="icon" class="shrink-0 md:hidden">
          <Menu class="h-5 w-5" />
          <span class="sr-only">Toggle navigation menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" class="flex flex-col">
        <nav class="grid gap-2 text-lg font-medium">
          <NuxtLink to="/" class="flex items-center gap-2 font-semibold">
            Acme Inc
          </NuxtLink>
          <NuxtLink
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all"
            to="/"
            activeClass="bg-primary text-white dark:text-black"
          >
            <Home class="h-4 w-4" />
            Home
          </NuxtLink>
          <NuxtLink
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
            to="/roles"
            activeClass="bg-muted"
          >
            <SquareUserRound class="h-4 w-4" />
            Roles
          </NuxtLink>
          <NuxtLink
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
            to="/users"
            activeClass="bg-muted"
          >
            <Users class="h-4 w-4" />
            Users
          </NuxtLink>
        </nav>
      </SheetContent>
    </Sheet>
    <div class="w-full flex-1">
      <h1 class="text-lg font-semibold md:text-2xl">
        {{ route.meta.title || "Dashboard" }}
      </h1>
    </div>
    <Button
      variant="secondary"
      size="icon"
      class="rounded-full"
      title="Toggle theme"
      @click="toggleTheme"
    >
      <Moon v-if="colorMode.preference === 'light'" class="h-4 w-4" />
      <Sun v-else class="h-4 w-4" />
      <span class="sr-only">Toggle theme</span>
    </Button>
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Button
          variant="secondary"
          size="icon"
          class="rounded-full"
          title="Toggle user menu"
        >
          <UserRound class="h-4 w-4" />
          <span class="sr-only">Toggle user menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" class="min-w-48">
        <DropdownMenuLabel>
          <p>{{ state.user.name }}</p>
          <p class="text-gray-500">{{ state.user.email }}</p>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem class="cursor-pointer" @click="handleLogout">
          <LogOut class="mr-2 h-4 w-4" />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </header>
</template>
