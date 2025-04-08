<script setup lang="ts">
import DataTable from "~/components/datatable/DataTable.vue"
import { h } from "vue"
import DataTableColumnHeader from "~/components/datatable/DataTableColumnHeader.vue"
import { useDateFormat } from "@vueuse/core"
import { Badge } from "~/components/ui/badge"
import type {ColumnDef} from "@tanstack/vue-table";

interface PaymentHistoryProps {
  userId: string;
}
const props = withDefaults(defineProps<PaymentHistoryProps>(), {});

const columns = [
  {
    accessorKey: "payment_id",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Payment ID" }),
    cell: ({ row }) => h("p", row.getValue("payment_id"))
  },
  {
    accessorKey: "type",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Type" }),
    cell: ({ row }) => {
      const role = row.getValue("type")
      return h(Badge, { variant: "secondary", class: "rounded-md" }, role)
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
  },
  {
    accessorKey: "valid_until",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Valid Until" }),
    cell: ({ row }) => {
      const validUntil = row.getValue("valid_until")
      if (validUntil) {
        const formattedDate = useDateFormat(validUntil, "Do MMM, YYYY - HH:mm")
        return h("p", formattedDate.value)
      } else {
        return h("p", "--")
      }
    }
  }
]

// const { state, onStateChange } = useDataTable()
const { data, status } = useAPI(`/api/payment/user/${props.userId}/`)
console.log(data.value)
</script>

<template>
  <p class="text-xl">Payment History</p>
  <DataTable
    :controlled="false"
    :columns="columns"
    :data="data"
    :loading="status==='pending'"
    @change="onStateChange"
  />
</template>
