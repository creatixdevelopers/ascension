<script setup>
import DataTable from "~/components/datatable/DataTable.vue"
import { h } from "vue"
import DataTableColumnHeader from "~/components/datatable/DataTableColumnHeader.vue"
import { useDateFormat } from "@vueuse/core"
import { Check, Cross } from "lucide-vue-next"
import { Badge } from "~/components/ui/badge"
import NuxtLink from "#app/components/nuxt-link.js";

definePageMeta({
  layout: "dashboard",
  title: "Responses"
})
useHead({
  title: "Responses"
})

const columns = [
  {
    accessorKey: "created",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Created" }),
    cell: ({ row }) => {
      const formattedDate = useDateFormat(
        row.getValue("created"),
        "Do MMM, YYYY - HH:mm"
      )
      return h(NuxtLink, {to: `/response/${row.id}`, "class": "text-blue-500 hover:underline"}, formattedDate.value)
    }
  },
  {
    accessorKey: "user.name",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "User" }),
    cell: ({ row }) => {
      return h(NuxtLink, {to: `/user/${row.id}`, "class": "text-blue-500 hover:underline"}, row.original.user.name)
    },
    enableHiding: false
  },
  {
    accessorKey: "user.email",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Email" }),
    cell: ({ row }) => h("p", row.original.user.email)
  }
]

const { state, onStateChange } = useDataTable()

const { data, status } = useAPI("/api/quiz/response/data-table/", {
  method: "POST",
  body: state
})
</script>

<template>
  <DataTable
    :controlled="true"
    :columns="columns"
    :data="data?.data"
    :rowCount="data?.total"
    :loading="false"
    @change="onStateChange"
  />
</template>
