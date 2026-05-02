<script setup>
import { onMounted, onUnmounted } from 'vue'
import AppIcon from './AppIcon.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, required: true },
  subtitle: { type: String, default: null },
  icon: { type: String, default: null },
  tone: { type: String, default: 'brand' },
  size: { type: String, default: 'md' },
})

const emit = defineEmits(['close'])

const toneClass = {
  brand: 'bg-brand-soft text-brand-dark dark:bg-brand/15 dark:text-brand-light',
  sky:   'bg-sky-50 text-sky-700 dark:bg-sky-500/15 dark:text-sky-300',
  amber: 'bg-amber-50 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300',
  rose:  'bg-rose-50 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300',
}

const widthClass = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
}

function onKeydown(e) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-end sm:items-center justify-center anim-fade"
      role="dialog"
      aria-modal="true"
    >
      <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" @click="emit('close')" />
      <div
        :class="[
          'relative w-full mx-2 sm:mx-4 mb-2 sm:mb-0 bg-surface-light dark:bg-surface-dark rounded-alpine shadow-alpine-lg border border-slate-200 dark:border-slate-700 anim-scale max-h-[90vh] flex flex-col overflow-hidden',
          widthClass[size],
        ]"
      >
        <!-- Header -->
        <div class="flex items-start gap-3 p-5 pb-4 border-b border-slate-200 dark:border-slate-700">
          <div
            v-if="icon"
            :class="['shrink-0 w-10 h-10 rounded-alpine flex items-center justify-center', toneClass[tone]]"
          >
            <AppIcon :name="icon" :size="20" />
          </div>
          <div class="flex-1 min-w-0">
            <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ title }}</h2>
            <p v-if="subtitle" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ subtitle }}</p>
          </div>
          <button
            @click="emit('close')"
            aria-label="Kapat"
            class="w-9 h-9 inline-flex items-center justify-center rounded-alpine text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            <AppIcon name="X" :size="18" />
          </button>
        </div>
        <!-- Body -->
        <div class="p-5 overflow-y-auto flex-1">
          <slot />
        </div>
        <!-- Footer -->
        <div
          v-if="$slots.footer"
          class="px-5 py-4 border-t border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-900/30 flex items-center justify-end gap-2"
        >
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>
