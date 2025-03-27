import type { UseFetchOptions } from "nuxt/app"
import { appendResponseHeader } from "h3"
import type { H3Event } from "h3"

export function useAPI<T>(
  url: string | (() => string),
  options?: UseFetchOptions<T>
) {
  const auth = useAuthStore()

  return useFetch(url, {
    ...options,
    $fetch: useNuxtApp().$api as typeof $fetch
  })
}
