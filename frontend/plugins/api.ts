export default defineNuxtPlugin((nuxtApp) => {
  const auth = useAuthStore()

  const api = $fetch.create({
    credentials: "include",
    retry: false,
    onRequest({ request, options, error }) {
      if (auth.state.token) {
        options.headers.set("Authorization", `Bearer ${auth.state.token}`)
      }
    },
    async onResponseError({ request, response, options }) {
      if (response.status === 401) {
        await nuxtApp.runWithContext(async () => {
          const resp = await auth.refreshToken()
          if (resp?.status) {
            options.retryStatusCodes = [401]
            options.retryDelay = 0
            options.retry = 1
          } else {
            await auth.logout()
          }
        })
      }
    }
  })

  // Expose as useNuxtApp().$api
  return { provide: { api } }
})
