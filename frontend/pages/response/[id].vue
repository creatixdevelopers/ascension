<script setup lang="ts">
import { LoaderCircleIcon } from "lucide-vue-next"
import { Badge } from "~/components/ui/badge"
import { useDateFormat } from "@vueuse/core"

definePageMeta({
  layout: "dashboard",
  title: "Response"
})
useHead({
  title: "Response"
})

const route = useRoute()

const responseId = route.params.id
const { data, status } = useAPI(`/api/quiz/response/${responseId}/`)
const options = ["Strongly Disagree", "Disagree", "Somewhat Agree", "Agree", "Strongly Agree"]
</script>

<template>
  <div v-if="data" class="flex flex-col gap-4">
    <div class="flex items-end justify-between border-b-2 pb-2">
      <div>
        <p class="text-2xl text-emerald-500">{{ data.user.name }}</p>
        <p class="">{{ data.user.email }}</p>
      </div>
      <Badge variant="secondary" class="rounded-md"
        >Created: {{ useDateFormat(data.created, "Do MMM, YYYY - HH:mm") }}
      </Badge>
    </div>
    <Card v-for="(questions, pillar) in data.data" :key="pillar">
      <div class="px-3 pt-3 pb-2">
        <p class="text-xl">{{ pillar }}</p>
      </div>
      <Table class="mb-4 w-full">
        <TableHeader>
          <TableRow class="w-full">
            <TableHead class="w-2/3 font-bold">Question</TableHead>
            <TableHead class="w-2/3 font-bold">Response</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(question, index) in questions" :key="index">
            <TableCell class="py-2">{{ question.question }}</TableCell>
            <TableCell class="py-2">{{ question.response ? options[question.response]: '--' }}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Card>
  </div>
  <div v-else class="flex h-full w-full items-center justify-center">
    <LoaderCircleIcon class="h-4 w-4 animate-spin" />
  </div>
</template>
