<script setup>
import Navbar from './components/Navbar.vue'
import ToastStack from './components/ui/ToastStack.vue'
import AppIcon from './components/AppIcon.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-50 antialiased">
    <Navbar />
    <div class="flex-1">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </div>
    <footer class="border-t border-slate-200 dark:border-slate-800 py-6 mt-auto">
      <div class="max-w-7xl mx-auto px-4 md:px-8 flex flex-col md:flex-row items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400">
        <div class="flex items-center gap-2">
          <AppIcon name="Mountain" :size="14" class="text-brand" />
          <span><strong>Alpin Malzeme Takip Sistemi</strong> — Vue 3 + Tailwind + Pinia mimarisi</span>
        </div>
        <div class="font-mono">v1.0 — prototype</div>
      </div>
    </footer>
    <ToastStack />
  </div>
</template>

<style>
.page-enter-active, .page-leave-active { transition: opacity .2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
</style>
