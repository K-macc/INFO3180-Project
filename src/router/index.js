import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AddProfileForm from '../components/AddProfileForm.vue'
// import Login from '../views/Login.vue'
import Logout from '../components/Logout.vue'
import Register from '../views/Register.vue'
import FavouritesView from '../views/FavouritesView.vue'
import ProfileDetailsView from '../views/ProfileDetailsView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import UserPage from '../views/UserPage.vue'
import CheckProfiles from '../views/CheckProfiles.vue'
import UpdateProfile from '../components/UpdateProfile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout
    },
    {
      path: '/users/:user_id',
      name: 'user-profile-info',
      component: UserProfileView
    },
    {
      path: '/users',
      name: 'home-users',
      component: UserPage
    },
    {
      path: '/profiles/new',
      name: 'new-profile',
      component: AddProfileForm
    },
    {
      path: '/profiles/check',
      name: 'check-profiles',
      component: CheckProfiles
    },
    {
      path: '/profiles/update/:profile_id',
      name: 'update-profile',
      component: UpdateProfile
    },
    {
      path: '/profiles/:profile_id',
      name: 'profile-details',
      component: ProfileDetailsView
    },
    {
      path: '/profiles/favourites',
      name: 'favourite-profiles',
      component: FavouritesView
    }    
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },

})
export default router