// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  modules: [
    "@nuxtjs/tailwindcss",
    "shadcn-nuxt",
    "@pinia/nuxt",
    "@nuxtjs/color-mode"
  ],
  shadcn: {
    prefix: "",
    componentDir: "./components/ui"
  },
  colorMode: {
    preference: "dark",
    fallback: "dark",
    classSuffix: "",
    storage: "cookie", // or 'sessionStorage' or 'localStorage'
    storageKey: "theme"
  },
  app: {
    head: {
      link: [{ rel: "icon", type: "image/png", href: "data:," }],
    }
  },
  runtimeConfig: {
    public: {
      apiBase: "http://localhost:8000"
    }
  },
  devtools: { enabled: true }
})
