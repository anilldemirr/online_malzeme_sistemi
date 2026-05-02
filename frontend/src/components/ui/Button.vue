<script setup>
import AppIcon from '../AppIcon.vue'

const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  icon: { type: String, default: null },
  iconRight: { type: String, default: null },
  disabled: { type: Boolean, default: false },
  class: { type: String, default: '' },
})

const sizeClass = {
  sm: 'h-9 px-3 text-sm gap-1.5',
  md: 'h-11 px-4 text-sm gap-2',
  lg: 'h-12 px-5 text-base gap-2',
}

const variantClass = {
  primary:   'bg-brand hover:bg-brand-dark text-white shadow-alpine font-semibold disabled:opacity-50 disabled:cursor-not-allowed',
  secondary: 'bg-slate-100 hover:bg-slate-200 text-slate-900 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-100 font-semibold disabled:opacity-50',
  ghost:     'bg-transparent hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium',
  danger:    'bg-rose-500 hover:bg-rose-600 text-white font-semibold disabled:opacity-50',
  outline:   'bg-transparent border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 font-medium',
}
</script>

<template>
  <button
    :disabled="disabled"
    :class="[
      'inline-flex items-center justify-center rounded-alpine transition-all active:scale-[.97]',
      sizeClass[size],
      variantClass[variant],
      props.class,
    ]"
  >
    <AppIcon v-if="icon" :name="icon" :size="size === 'sm' ? 16 : 18" />
    <slot />
    <AppIcon v-if="iconRight" :name="iconRight" :size="size === 'sm' ? 16 : 18" />
  </button>
</template>
