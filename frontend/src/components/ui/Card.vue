<script setup>
defineProps({
  interactive: { type: Boolean, default: false },
  class: { type: String, default: '' },
})
</script>

<template>
  <div
    :class="[
      'bg-surface-light dark:bg-surface-dark border border-slate-200/80 dark:border-slate-700/60 rounded-alpine shadow-alpine',
      interactive ? 'hover:shadow-alpine-md transition-shadow cursor-pointer' : '',
      $props.class,
    ]"
  >
    <slot />
  </div>
</template>
