import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import HomeView from '../views/HomeView.vue'
import AddProfileForm from '../components/AddProfileForm.vue'
import Logout from '../components/Logout.vue'
import Register from '../views/Register.vue'
import Register from '../views/Register.vue'
import ProfileDetailsView from '../views/ProfileDetailsView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import UserPage from '../views/UserPage.vue'
import CheckProfiles from '../views/CheckProfiles.vue'
import UpdateProfile from '../components/UpdateProfile.vue'
import MatchProfile from '../views/MatchProfile.vue'
import Reports from '../views/Reports.vue'
import UserPage from '../views/UserPage.vue'
import CheckProfiles from '../views/CheckProfiles.vue'
import UpdateProfile from '../components/UpdateProfile.vue'
import MatchProfile from '../views/MatchProfile.vue'
import Reports from '../views/Reports.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
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
      path: '/profiles/create',
      name: 'CreateProfile',
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
      path: '/profiles/match',
      name: 'match-profiles',
      component: MatchProfile
    },
    {
      path: '/reports',
      name: 'reports',
      component: Reports
    }   
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },
})

export default router