import { readonly, ref } from "vue";
import { io, Socket } from "socket.io-client";

export function useSocket() {
  const config = useRuntimeConfig();
  const socket = ref<Socket | null>(null);

  const connectSocket = () => {
    if (!socket.value) {
      socket.value = io(config.public.baseURL, { path: "/ws/socket.io" });
    }
  };

  const disconnectSocket = () => {
    if (socket.value) {
      socket.value.disconnect();
      socket.value = null;
    }
  };

  const on = (event: string, callback: (...args: any[]) => void) => {
    if (socket.value) {
      socket.value.on(event, callback);
    }
  };

  const off = (event: string, callback: (...args: any[]) => void) => {
    if (socket.value) {
      socket.value.off(event, callback);
    }
  };

  const emit = (event: string, ...args: any[]) => {
    if (socket.value) {
      socket.value.emit(event, ...args);
    }
  };

  const dispose = () => {
    disconnectSocket();
  };

  return {
    connectSocket,
    disconnectSocket,
    on,
    off,
    emit,
    socket: readonly(socket),
    dispose,
  };
}
