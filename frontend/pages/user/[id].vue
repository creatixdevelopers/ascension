<script setup lang="ts">
import { LoaderCircleIcon } from "lucide-vue-next"
import { Badge } from "~/components/ui/badge"
import {useDateFormat} from "@vueuse/core";
import PaymentHistory from "~/pages/user/paymentHistory.vue";

definePageMeta({
  layout: "dashboard",
  title: `User`
})
useHead({
  title: "User"
})

const route = useRoute()

const userId = route.params.id
const { data, status } = useAPI(`/api/user/${userId}/`, { method: "GET" })
</script>

<template>
  <div v-if="data" class="flex flex-col gap-4">
    <div class="flex justify-between items-end border-b-2 pb-2">
      <div>
        <p class="text-2xl text-emerald-500">{{ data.name }}</p>
        <p class="">{{ data.email }}</p>
      </div>
      <Badge variant="secondary" class="rounded-md">Created: {{ useDateFormat(data.created, "Do MMM, YYYY - HH:mm") }}</Badge>
    </div>
    <PaymentHistory :user-id="data.uid" />
  </div>
  <div v-else class="flex h-full w-full items-center justify-center">
    <LoaderCircleIcon class="h-4 w-4 animate-spin" />
  </div>
</template>
