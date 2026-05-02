<script setup>
const STATUS_MAP = {
  depoda:     { label: 'Depoda',     bg: 'bg-emerald-50 dark:bg-emerald-500/15', text: 'text-emerald-700 dark:text-emerald-300', dot: 'bg-emerald-500' },
  beklemede:  { label: 'Beklemede', bg: 'bg-amber-50 dark:bg-amber-500/15',     text: 'text-amber-700 dark:text-amber-300',     dot: 'bg-amber-500' },
  kullanimda: { label: 'Kullanımda',bg: 'bg-sky-50 dark:bg-sky-500/15',         text: 'text-sky-700 dark:text-sky-300',         dot: 'bg-sky-500' },
  staging:    { label: 'Staging',   bg: 'bg-violet-50 dark:bg-violet-500/15',   text: 'text-violet-700 dark:text-violet-300',   dot: 'bg-violet-500' },
  onaylandi:  { label: 'Onaylandı', bg: 'bg-emerald-50 dark:bg-emerald-500/15', text: 'text-emerald-700 dark:text-emerald-300', dot: 'bg-emerald-500' },
  reddedildi: { label: 'Reddedildi',bg: 'bg-rose-50 dark:bg-rose-500/15',       text: 'text-rose-700 dark:text-rose-300',       dot: 'bg-rose-500' },
  kayip:      { label: 'Kayıp',     bg: 'bg-rose-50 dark:bg-rose-500/15',       text: 'text-rose-700 dark:text-rose-300',       dot: 'bg-rose-500' },
}

const props = defineProps({
  status: { type: String, required: true },
  label: { type: String, default: null },
  size: { type: String, default: 'md' },
})

const cfg = STATUS_MAP[props.status] || STATUS_MAP.depoda
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1.5 rounded-full font-medium',
      size === 'sm' ? 'text-[11px] px-2 py-0.5' : 'text-xs px-2.5 py-1',
      cfg.bg, cfg.text,
    ]"
  >
    <span :class="['w-1.5 h-1.5 rounded-full', cfg.dot]" aria-hidden="true" />
    {{ label || cfg.label }}
  </span>
</template>
