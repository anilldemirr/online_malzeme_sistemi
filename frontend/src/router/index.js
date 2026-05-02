import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('../views/Dashboard.vue'),
  },
  {
    path: '/equipment',
    name: 'equipment',
    component: () => import('../views/EquipmentList.vue'),
  },
  {
    path: '/my-inventory',
    name: 'my-inventory',
    component: () => import('../views/MyInventory.vue'),
  },
  {
    path: '/manager',
    name: 'manager',
    component: () => import('../views/ManagerPanel.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
