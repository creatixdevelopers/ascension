<script setup lang="ts">
import LoadingButton from "~/components/custom/LoadingButton.vue"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { toTypedSchema } from "@vee-validate/zod"
import * as z from "zod"
import { useForm } from "vee-validate"
import {
  FormControl,
  FormField,
  FormItem,
  FormMessage
} from "@/components/ui/form"
import { toast } from "vue-sonner"
import { EyeIcon, EyeOffIcon } from "lucide-vue-next"

definePageMeta({ layout: "auth", title: "Login" })
useHead({ title: "Login" })

const { login } = useAuthStore()
const loading = ref(false)
const passwordVisible = ref(false)

const { handleSubmit } = useForm({
  validationSchema: toTypedSchema(
    z.object({
      email: z
        .string()
        .trim()
        .email("Please enter a valid email address")
        .min(2, "Email address must be at least 5 characters")
        .max(128, "Email address can be at max 128 characters"),
      password: z
        .string()
        .trim()
        .min(8, "Password must be at least 8 characters")
        .max(32, "Password must be at max 32 characters")
    })
  )
})
const onPasswordVisibilityToggle = () => {
  passwordVisible.value = !passwordVisible.value
}
const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  const { status, response } = await login(values)
  if (!status) {
    toast.error(response.message)
    loading.value = false
  } else {
    navigateTo("/")
  }
  loading.value = false
})
</script>

<template>
  <div class="flex h-full w-full items-center justify-center">
    <Card class="w-full max-w-sm">
      <CardHeader>
        <CardTitle class="mb-2 text-center text-3xl font-bold">
          Login
        </CardTitle>
        <CardDescription class="text-balance text-center text-muted-foreground">
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent class="grid gap-4">
        <form class="grid gap-4" @submit.prevent="onSubmit">
          <FormField v-slot="{ componentField }" name="email">
            <FormItem>
              <Label>Email</Label>
              <FormControl>
                <Input type="email" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="password">
            <FormItem>
              <Label>Password</Label>
              <FormControl>
                <div class="relative w-full max-w-sm items-center">
                  <Input
                    :type="passwordVisible ? 'text' : 'password'"
                    v-bind="componentField"
                  />
                  <span
                    class="absolute inset-y-0 end-0 flex cursor-pointer items-center justify-center px-2"
                    @click="onPasswordVisibilityToggle"
                  >
                    <EyeIcon
                      v-if="!passwordVisible"
                      class="size-4 text-muted-foreground"
                    />
                    <EyeOffIcon v-else class="size-4 text-muted-foreground" />
                  </span>
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <LoadingButton :loading="loading">
            Login
            <template #loading>Logging In...</template>
          </LoadingButton>
        </form>
        <div class="mt-4 text-center text-sm">
          Don't have an account?
          <a href="#" class="underline"> Sign up </a>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
