export default defineNuxtRouteMiddleware(async (to, from) => {
  const auth = useAuthStore()
  const layout = to.meta.layout

  // Ensure authentication state is initialized
  if (!auth.state.user) {
    await auth.fetchUser()
  }

  // Redirect logic
  if (!auth.isAuthenticated && layout !== "auth") {
    return navigateTo("/login")
  } else if (auth.isAuthenticated && layout === "auth") {
    return navigateTo("/")
  }

  // Get logged in state
  // if (!auth.isVerified) {
  //   await auth.verifyLogin()
  // }
  //
  // if (layout) {
  //   if (layout === "auth") {
  //     // if user is authenticated, redirect to login page
  //     if (auth.isAuthenticated) {
  //       return navigateTo("/")
  //     }
  //   } else if (layout === "dashboard") {
  //     // if user is not authenticated, redirect to login page
  //     if (!auth.isAuthenticated) {
  //       return navigateTo("/login")
  //     }
  //   }
  // }
})
