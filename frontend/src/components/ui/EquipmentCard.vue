<script setup>
import AppIcon from '../AppIcon.vue'
import StatusBadge from './StatusBadge.vue'

defineProps({
  model: { type: Object, required: true },
  item: { type: Object, default: null },
  countAvailable: { type: Number, default: null },
  density: { type: String, default: 'comfortable' },
})
</script>

<template>
  <article
    class="group bg-surface-light dark:bg-surface-dark border border-slate-200/80 dark:border-slate-700/60 rounded-alpine shadow-alpine hover:shadow-alpine-md transition-all overflow-hidden flex flex-col"
  >
    <!-- Visual header -->
    <div
      :class="[
        'relative flex items-center justify-center overflow-hidden',
        density === 'compact' ? 'h-24' : 'h-36',
        model.kategori === 'kitap'
          ? 'bg-gradient-to-br from-amber-50 to-orange-100 dark:from-amber-500/10 dark:to-orange-500/10'
          : 'bg-gradient-to-br from-brand-soft to-emerald-100 dark:from-brand/10 dark:to-emerald-500/10',
      ]"
    >
      <div
        class="absolute inset-0 opacity-30"
        :style="{
          backgroundImage: 'radial-gradient(circle at 30% 30%, currentColor 0, transparent 50%)',
          color: model.kategori === 'kitap' ? '#F59E0B' : '#73B928',
        }"
      />
      <AppIcon
        :name="model.icon || 'Box'"
        :size="density === 'compact' ? 36 : 56"
        :stroke="1.25"
        :class="model.kategori === 'kitap' ? 'text-amber-700/70 dark:text-amber-300/80' : 'text-brand-dark/70 dark:text-brand-light/80'"
      />
      <span class="absolute top-2 left-2 text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded-full bg-white/80 dark:bg-slate-900/70 text-slate-700 dark:text-slate-200 backdrop-blur-sm">
        {{ model.kategori }}
      </span>
      <span v-if="item" class="absolute top-2 right-2 inline-flex items-center gap-1 text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-slate-900/85 text-white">
        <AppIcon name="QrCode" :size="10" /> {{ item.demirbas_no }}
      </span>
    </div>

    <!-- Body -->
    <div :class="['flex-1 flex flex-col', density === 'compact' ? 'p-3' : 'p-4']">
      <div class="flex items-start justify-between gap-2 mb-1">
        <div class="min-w-0 flex-1">
          <div class="text-[11px] font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">{{ model.marka_yayin_evi }}</div>
          <h3 :class="['font-semibold text-slate-900 dark:text-slate-100 leading-snug truncate', density === 'compact' ? 'text-sm' : 'text-base']">
            {{ model.model_adi }}
          </h3>
        </div>
        <StatusBadge v-if="item" :status="item.durum" size="sm" />
        <span
          v-else-if="countAvailable !== null"
          class="shrink-0 text-[11px] font-semibold px-2 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 whitespace-nowrap"
        >
          {{ countAvailable }} depoda
        </span>
      </div>
      <p v-if="density !== 'compact'" class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2 mb-3">
        {{ model.aciklama }}
      </p>
      <div class="mt-auto pt-2">
        <slot name="action" />
      </div>
    </div>
  </article>
</template>
