import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
    router: useRouter(),
    flashMessage: ''
  }),
  actions: {
    login(userData, token) {
      this.user = userData;
      this.token = token;
      this.isAuthenticated = true;
      localStorage.setItem('jwt', token);
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('jwt');
      this.router.push('/');
    },
    setFlashMessage(message) {
      this.flashMessage = message;
    }
  }
})