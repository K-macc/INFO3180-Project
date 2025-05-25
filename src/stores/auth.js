import { defineStore } from "pinia";
import { useRouter } from "vue-router";


export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: localStorage.getItem("jwt") || null,
    router: useRouter(),
    flashMessage: "",
    user_id: localStorage.getItem("user_id") || null,
    profile_id: localStorage.getItem("profile_id") || null,
    current_fav_id: null,
    isProfileComplete: false,
  }),
   getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    login(userData, token, user_id) {
      this.user = userData;
      this.user_id = user_id;
      this.token = token;
      localStorage.setItem("jwt", token);
      localStorage.setItem("user_id", user_id);
    },
    logout() {
      this.user = null;
      this.token = null;
      this.user_id = null;
      localStorage.removeItem("jwt");
      localStorage.removeItem("user_id");
      this.router.push("/");
    },
    restoreAuth() {
      const storedToken = localStorage.getItem("jwt");
      const storedUserId = localStorage.getItem("user_id");

      if (storedToken && storedUserId) {
        this.token = storedToken;
        this.user_id = storedUserId;
      }
    },
    setFlashMessage(message) {
      this.flashMessage = message;
    },
    setProfileId(profile_id) {
      this.profile_id = profile_id;
      localStorage.setItem("profile_id", profile_id);
    },
    setUserId(user_id) {
      this.user_id = user_id;
    },
    async checkProfileCompletion(id) {
      try {
        const response = await fetch(`/api/check-profiles/${id}`, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        const data = await response.json();
        if (data.status) {
          this.isProfileComplete = true;
          return { complete: true };
        } else {
          this.isProfileComplete = false;
          return { complete: false };
        }
      } catch (error) {
        console.error("Error checking profile completion:", error);
        return { complete: false };
      }
    },
  },
});
