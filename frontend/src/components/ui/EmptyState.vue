<script setup>
import AppIcon from '../AppIcon.vue'

defineProps({
  icon: { type: String, default: 'Box' },
  title: { type: String, required: true },
  body: { type: String, default: null },
})
</script>

<template>
  <div class="flex flex-col items-center justify-center text-center py-16 px-6">
    <div class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mb-4 text-slate-400 dark:text-slate-500">
      <AppIcon :name="icon" :size="28" />
    </div>
    <h3 class="text-base font-semibold text-slate-900 dark:text-slate-100 mb-1">{{ title }}</h3>
    <p v-if="body" class="text-sm text-slate-500 dark:text-slate-400 max-w-sm">{{ body }}</p>
    <div v-if="$slots.action" class="mt-5">
      <slot name="action" />
    </div>
  </div>
</template>
