import Vue from 'vue';
import Router from 'vue-router';
import store from '@/store';
import Home from '@/views/HomeView.vue';
import User from '@/views/UserView.vue';
import Login from '@/views/LoginView.vue';
import Logout from '@/views/LogoutView.vue';
import Register from '@/views/RegisterView.vue';
import Task from '@/views/resource/TaskView.vue';
import NotFound from '@/views/NotFoundView.vue';
import TaskList from '@/views/resource/TaskList.vue';
import Schedule from '@/views/resource/ScheduleView.vue';
import About from '@/views/AboutView.vue'
Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.VUE_APP_BASE_URL,

  routes: [
    {
      path: "/",
      name: "Index",
      redirect: "/home",
    },
    {
      path: "/home",
      name: "Home",
      component: Home,
    },
    {
      path: "/user",
      name: "User",
      component: User,
      meta: { requiresAuth: true }
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: "/logout",
      name: "Logout",
      component:Logout,
    },
    {
      path: "/register",
      name: "Register",
      component: Register,
      meta: { requiresAuth: false }
    },
    {
      path: "/task",
      name: "Task",
      meta: { requiresAuth: true },
      component: Task,
    },
    {
      path: "/tasklist",
      name: "TaskList",
      meta: { requiresAuth: true },
      component: TaskList,
    },
    {
      path: "/schedule",
      name: "Schedule",
      meta: { requiresAuth: true },
      component: Schedule,
    },
    {
      path: "/about",
      name: "About",
      // route level code-splitting
      component: About,
    },
    {
      path: '*',
      name: 'NotFound',
      component:NotFound,
    }
  ]
});


// global guard before each route
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = store.state.authenticated
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
  from;
})

// global hook after each route
router.afterEach((to, from) => {
    to;
    from;
});

export default router;
