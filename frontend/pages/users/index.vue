<script setup>
import DataTable from "~/components/datatable/DataTable.vue"
import { h } from "vue"
import DataTableColumnHeader from "~/components/datatable/DataTableColumnHeader.vue"
import { useDateFormat } from "@vueuse/core"
import { Check, Cross } from "lucide-vue-next"
import { Badge } from "~/components/ui/badge"

definePageMeta({
  layout: "dashboard",
  title: "Users"
})
useHead({
  title: "Users"
})

const columns = [
  {
    accessorKey: "name",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "User" }),
    cell: ({ row }) => h("p", row.getValue("name")),
    enableHiding: false
  },
  {
    accessorKey: "email",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Email" }),
    cell: ({ row }) => h("p", row.getValue("email"))
  },
  {
    accessorKey: "role",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Role" }),
    cell: ({ row }) => {
      const role = row.getValue("role")
      return h(Badge, { variant: "secondary", class: "rounded-md" }, role)
    }
  },
  {
    accessorKey: "verified",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Verified" }),
    cell: ({ row }) => {
      if (row.getValue("verified")) {
        return h(Check, { class: "text-emerald-500 text-center" })
      } else {
        return h(Cross, { class: "text-amber-500 text-center" })
      }
    }
  },
  {
    accessorKey: "active",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Active" }),
    cell: ({ row }) => {
      if (row.getValue("active")) {
        return h(Check, { class: "text-emerald-500 text-center" })
      } else {
        return h(Cross, { class: "text-amber-500 text-center" })
      }
    }
  },
  {
    accessorKey: "created",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Created" }),
    cell: ({ row }) => {
      const formattedDate = useDateFormat(
        row.getValue("created"),
        "Do MMM, YYYY - HH:mm"
      )
      return h("p", formattedDate.value)
    }
  }
]

const { state, onStateChange } = useDataTable()

const { data, status } = useFetch("/api/user/data-table/", {
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
