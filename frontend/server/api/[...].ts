import { joinURL } from "ufo"

export default defineEventHandler(async (event) => {
  const proxyURL = useRuntimeConfig().public.apiBase || "http://localhost:8000"
  const path = event.path.replace("/api", "/api")
  const url = joinURL(proxyURL, path)
  return proxyRequest(event, url)
})
