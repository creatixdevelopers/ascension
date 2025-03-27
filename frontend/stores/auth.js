export const useAuthStore = defineStore("auth", () => {
  const initialState = {
    token: null,
    user: null
  }
  const state = reactive({ ...initialState })

  const isAuthenticated = computed(() => !!state.token)

  async function login(credentials) {
    try {
      const response = await $fetch("/api/auth/login/", {
        method: "POST",
        body: credentials
      })
      if (response?.token) {
        state.token = response.token
        await fetchUser()
        return { status: true }
      }
    } catch (error) {
      console.error("Error logging in", error.data)
      return { status: false, response: error.data }
    }
  }

  async function fetchUser() {
    const { data, error } = await useAPI("/api/auth/me/")
    if (error.value) {
      console.error("Error fetching user", error.value)
    }
    if (data.value) {
      state.user = data.value
    }
  }

  async function refreshToken() {
    const { data, error } = await useFetch("/api/auth/refresh/", {
      method: "POST",
      credentials: "include"
    })

    if (error.value) {
      console.error("Failed to refresh token:", error.value.data)
      return { status: false }
    }
    if (data.value) {
      state.token = data.value.token || null
      return { status: true }
    }
  }

  async function logout() {
    try {
      const response = await $fetch("/api/auth/logout/", {
        method: "POST"
      })
      state.token = initialState.token
      state.user = initialState.user
      return { status: true, response: response }
    } catch (error) {
      console.error("Error logging out", error.data)
      return { status: false, response: error.data }
    }
  }

  return {
    state,
    isAuthenticated,
    login,
    fetchUser,
    refreshToken,
    logout
  }
})
