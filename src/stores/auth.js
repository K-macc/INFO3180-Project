import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export const isAuthenticated = ref(false);

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    router: useRouter(),
    flashMessage: '',
    user_id: null,
    profile_id: null,
    current_fav_id: null  
  }),
  actions: {
    login(userData, token, user_id) {
      this.user = userData;
      this.user_id = user_id;
      this.token = token;
      isAuthenticated.value = true;
      localStorage.setItem('jwt', token);
    },
    logout() {
      this.user = null;
      isAuthenticated.value = false;
      localStorage.removeItem('jwt');
      this.router.push('/');
    },
    setFlashMessage(message) {
      this.flashMessage = message;
    },
    setProfileId(profile_id) {
      this.profile_id = profile_id;
    },
    setUserId(user_id) {
      this.user_id = user_id;
    }
  }
});
