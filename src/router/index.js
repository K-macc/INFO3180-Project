import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddProfileForm from '../components/AddProfileForm.vue'
import LoginForm from '../components/LoginForm.vue'
import Logout from '../components/Logout.vue'
import RegistrationForm from '../components/RegistrationForm.vue'
import FavouritesView from '../views/FavouritesView.vue'
import ProfileDetailsView from '../views/ProfileDetailsView.vue'
import UserProfileView from '../views/UserProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: RegistrationForm
    },
    {
      path: '/login',
      name: 'login',
      component: LoginForm
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout,
      // This will be handled by a method that clears auth tokens
      beforeEnter: (to, from, next) => {
        // Logout logic here
        next('/')
      }
    },
    {
      path: '/users/:user_id',
      name: 'user-profile-info',
      component: UserProfileView
    },
    {
      path: '/profiles/new',
      name: 'new-profile',
      component: AddProfileForm
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
  ]

})
export default router