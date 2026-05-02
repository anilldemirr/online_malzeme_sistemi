<script setup>
defineProps({
  user: { type: Object, default: null },
  size: { type: Number, default: 36 },
  ring: { type: Boolean, default: false },
})
</script>

<template>
  <div
    v-if="user"
    :class="[
      'shrink-0 inline-flex items-center justify-center rounded-full font-semibold text-white',
      ring ? 'ring-2 ring-white dark:ring-slate-800' : '',
    ]"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
      background: user.renk,
      fontSize: `${size * 0.38}px`,
    }"
    :aria-label="user.ad"
  >
    {{ user.avatar }}
  </div>
</template>
