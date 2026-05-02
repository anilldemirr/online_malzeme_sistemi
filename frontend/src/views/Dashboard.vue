<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore, formatRelative } from '../stores/inventory'
import AppIcon from '../components/AppIcon.vue'
import Card from '../components/ui/Card.vue'
import Button from '../components/ui/Button.vue'
import Avatar from '../components/ui/Avatar.vue'
import StatusBadge from '../components/ui/StatusBadge.vue'

const store = useInventoryStore()
const router = useRouter()

const myItems = computed(() => store.myItems)
const myPending = computed(() => store.myPendingRequests)

const incomingTransfers = computed(() =>
  store.transactions.filter(
    t => t.tip === 'devir' && t.durum === 'beklemede' && t.hedef_uye_id === store.currentUserId && !t.b_onayli
  )
)

const outgoingTransfers = computed(() =>
  store.transactions.filter(
    t => t.tip === 'devir' && t.durum === 'beklemede' && t.talep_eden_id === store.currentUserId
  )
)

const managerStats = computed(() => {
  if (!store.isManager) return null
  return {
    pendingReq: store.pendingRequests.length,
    pendingTransfers: store.pendingTransfers.length,
    staged: store.stagedItems.length,
    circulating: store.items.filter(i => i.durum === 'kullanimda').length,
  }
})

function navigate(name) { router.push({ name }) }
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8 topo-bg min-h-[calc(100vh-4rem)]">
    <!-- Greeting -->
    <header class="mb-6 md:mb-8 anim-fade">
      <div class="flex items-center gap-2 mb-1">
        <span class="text-xs font-semibold uppercase tracking-wider text-brand-dark dark:text-brand-light">Genel Bakış</span>
        <span v-if="store.isManager" class="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-brand text-white">
          <AppIcon name="Shield" :size="10" /> Yönetici Modu
        </span>
      </div>
      <h1 class="text-3xl md:text-4xl font-bold tracking-tight text-slate-900 dark:text-slate-50">
        Merhaba, <span class="text-brand-dark dark:text-brand-light">{{ store.currentUser?.ad?.split(' ')[0] }}</span>
      </h1>
      <p class="text-slate-500 dark:text-slate-400 mt-1 text-sm md:text-base">
        {{ store.isManager
          ? 'Bekleyen işlemleri ve envanteri buradan yönetebilirsiniz.'
          : 'Üzerinizdeki malzeme ve bekleyen taleplerinize hızlı bakış.' }}
      </p>
    </header>

    <!-- Stat tiles -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 mb-6">
      <button @click="navigate('my-inventory')" class="text-left bg-surface-light dark:bg-surface-dark border border-slate-200/80 dark:border-slate-700/60 rounded-alpine p-4 hover:shadow-alpine-md transition-shadow">
        <div class="w-9 h-9 rounded-alpine flex items-center justify-center mb-3 bg-brand-soft text-brand-dark dark:bg-brand/15 dark:text-brand-light"><AppIcon name="Backpack" :size="18" /></div>
        <div class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-slate-50 leading-none">{{ myItems.length }}</div>
        <div class="mt-1.5 text-xs text-slate-500 dark:text-slate-400"><span class="font-semibold text-slate-700 dark:text-slate-300">Üzerimde</span> zimmetli malzeme</div>
      </button>
      <div class="text-left bg-surface-light dark:bg-surface-dark border border-slate-200/80 dark:border-slate-700/60 rounded-alpine p-4">
        <div class="w-9 h-9 rounded-alpine flex items-center justify-center mb-3 bg-amber-50 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300"><AppIcon name="Clock" :size="18" /></div>
        <div class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-slate-50 leading-none">{{ myPending.length }}</div>
        <div class="mt-1.5 text-xs text-slate-500 dark:text-slate-400"><span class="font-semibold text-slate-700 dark:text-slate-300">Bekleyen</span> taleplerim</div>
      </div>
      <div class="text-left bg-surface-light dark:bg-surface-dark border border-slate-200/80 dark:border-slate-700/60 rounded-alpine p-4">
        <div class="w-9 h-9 rounded-alpine flex items-center justify-center mb-3 bg-sky-50 text-sky-700 dark:bg-sky-500/15 dark:text-sky-300"><AppIcon name="Switch" :size="18" /></div>
        <div class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-slate-50 leading-none">{{ incomingTransfers.length + outgoingTransfers.length }}</div>
        <div class="mt-1.5 text-xs text-slate-500 dark:text-slate-400"><span class="font-semibold text-slate-700 dark:text-slate-300">Aktif Devir</span> devam ediyor</div>
      </div>
      <button @click="navigate('equipment')" class="text-left bg-surface-light dark:bg-surface-dark border border-slate-200/80 dark:border-slate-700/60 rounded-alpine p-4 hover:shadow-alpine-md transition-shadow">
        <div class="w-9 h-9 rounded-alpine flex items-center justify-center mb-3 bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300"><AppIcon name="Box" :size="18" /></div>
        <div class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-slate-50 leading-none">{{ store.models.length }}</div>
        <div class="mt-1.5 text-xs text-slate-500 dark:text-slate-400"><span class="font-semibold text-slate-700 dark:text-slate-300">Katalog</span> malzeme türü</div>
      </button>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6">
      <!-- Active checkouts -->
      <Card class="lg:col-span-2 p-5 anim-slide">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100">Üzerimdeki Malzeme</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400">Zimmetinizdeki fiziksel envanter</p>
          </div>
          <Button variant="ghost" size="sm" icon-right="ArrowRight" @click="navigate('my-inventory')">Tümü</Button>
        </div>
        <div v-if="myItems.length === 0" class="flex flex-col items-center text-center py-10 px-4">
          <div class="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mb-3 text-slate-400"><AppIcon name="Backpack" :size="22" /></div>
          <p class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-1">Şu an üzerinizde zimmetli malzeme bulunmuyor</p>
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">Bir tırmanış için ihtiyacınız olan malzemeyi katalogdan talep edebilirsiniz.</p>
          <Button variant="primary" icon="Plus" @click="navigate('equipment')">Kataloğa Git</Button>
        </div>
        <ul v-else class="divide-y divide-slate-100 dark:divide-slate-800">
          <li v-for="item in myItems.slice(0, 4)" :key="item.id" class="flex items-center gap-3 py-3 first:pt-0 last:pb-0">
            <div class="w-10 h-10 rounded-alpine bg-brand-soft dark:bg-brand/15 flex items-center justify-center text-brand-dark dark:text-brand-light shrink-0">
              <AppIcon :name="store.getModel(item.model_id)?.icon || 'Box'" :size="18" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">{{ store.getModel(item.model_id)?.model_adi }}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">{{ item.demirbas_no }}</div>
            </div>
            <StatusBadge :status="item.durum" size="sm" />
          </li>
        </ul>
      </Card>

      <!-- Pending requests -->
      <Card class="p-5 anim-slide" style="animation-delay:60ms">
        <div class="mb-4">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100">Bekleyen Taleplerim</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400">Yönetici onayı bekliyor</p>
        </div>
        <div v-if="myPending.length === 0" class="text-center py-6 text-sm text-slate-500 dark:text-slate-400">
          <AppIcon name="Check" :size="32" class="mx-auto mb-2 text-emerald-500" />
          Bekleyen talep yok
        </div>
        <ul v-else class="space-y-3">
          <li v-for="t in myPending" :key="t.id" class="flex items-start gap-3 p-3 rounded-alpine border border-amber-200/60 bg-amber-50/40 dark:bg-amber-500/5 dark:border-amber-500/20">
            <AppIcon name="Clock" :size="16" class="text-amber-600 dark:text-amber-400 mt-0.5" />
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.getModel(t.model_id)?.model_adi }}</div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">{{ formatRelative(t.created) }} talep edildi</div>
            </div>
          </li>
        </ul>
      </Card>

      <!-- Incoming transfers needing B-confirm -->
      <Card v-if="incomingTransfers.length > 0" class="lg:col-span-3 p-5 anim-slide border-sky-200 dark:border-sky-500/30">
        <div class="flex items-center gap-2 mb-3">
          <div class="w-8 h-8 rounded-alpine bg-sky-50 dark:bg-sky-500/15 text-sky-600 dark:text-sky-300 flex items-center justify-center pulse-ring">
            <AppIcon name="Switch" :size="16" />
          </div>
          <div class="flex-1">
            <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100">Size Yönelik Devir İşlemleri</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400">Teslim aldığınızı onaylamanız bekleniyor</p>
          </div>
        </div>
        <ul class="space-y-2">
          <li v-for="t in incomingTransfers" :key="t.id" class="flex items-center gap-3 p-3 rounded-alpine bg-slate-50 dark:bg-slate-800/40">
            <Avatar :user="store.getUser(t.talep_eden_id)" :size="36" />
            <AppIcon name="ArrowRight" :size="16" class="text-slate-400" />
            <Avatar :user="store.currentUser" :size="36" />
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">{{ store.getModel(t.model_id)?.model_adi }}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">{{ store.getItem(t.assigned_item_id)?.demirbas_no }} · {{ store.getUser(t.talep_eden_id)?.ad }}</div>
            </div>
            <Button size="sm" icon="Check" @click="store.confirmTransferReceipt(t.id)">Teslim Aldım</Button>
          </li>
        </ul>
      </Card>

      <!-- Manager mission control -->
      <Card v-if="store.isManager && managerStats" class="lg:col-span-3 p-5 anim-slide border-brand/30 bg-gradient-to-br from-brand-soft/30 to-transparent dark:from-brand/5">
        <div class="flex items-start justify-between gap-4 mb-4">
          <div>
            <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <AppIcon name="Shield" :size="18" class="text-brand" /> Yönetici Görevleri
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400">İşlem bekleyen kuyruğu</p>
          </div>
          <Button size="sm" icon-right="ArrowRight" @click="navigate('manager')">Panele Git</Button>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div v-for="stat in [
            { label: 'Bekleyen Talep', value: managerStats.pendingReq, icon: 'Inbox', color: 'amber' },
            { label: 'Devir İşlemi', value: managerStats.pendingTransfers, icon: 'Switch', color: 'sky' },
            { label: 'Staging', value: managerStats.staged, icon: 'Layers', color: 'violet' },
            { label: 'Sahada', value: managerStats.circulating, icon: 'Backpack', color: 'emerald' },
          ]" :key="stat.label"
            :class="[
              'bg-surface-light dark:bg-surface-dark border-2 rounded-alpine p-3',
              stat.color === 'amber' ? 'border-amber-200 dark:border-amber-500/30' :
              stat.color === 'sky' ? 'border-sky-200 dark:border-sky-500/30' :
              stat.color === 'violet' ? 'border-violet-200 dark:border-violet-500/30' :
              'border-emerald-200 dark:border-emerald-500/30',
            ]"
          >
            <div :class="[
              'flex items-center gap-2 mb-1',
              stat.color === 'amber' ? 'text-amber-700 dark:text-amber-300' :
              stat.color === 'sky' ? 'text-sky-700 dark:text-sky-300' :
              stat.color === 'violet' ? 'text-violet-700 dark:text-violet-300' :
              'text-emerald-700 dark:text-emerald-300',
            ]">
              <AppIcon :name="stat.icon" :size="14" />
              <span class="text-[11px] font-semibold uppercase tracking-wider">{{ stat.label }}</span>
            </div>
            <div class="text-2xl font-bold text-slate-900 dark:text-slate-50">{{ stat.value }}</div>
          </div>
        </div>
      </Card>

      <!-- Audit peek -->
      <Card class="lg:col-span-3 p-5 anim-slide">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <AppIcon name="History" :size="16" /> Son Aktivite
          </h2>
          <span class="text-[11px] text-slate-500 dark:text-slate-400 inline-flex items-center gap-1">
            <AppIcon name="Shield" :size="10" /> Değiştirilemez denetim kaydı
          </span>
        </div>
        <ol class="space-y-2.5">
          <li v-for="a in store.audit.slice(0, 5)" :key="a.id" class="flex items-start gap-3 text-sm">
            <Avatar :user="store.getUser(a.aktor_id)" :size="28" />
            <div class="flex-1 min-w-0">
              <div class="text-slate-700 dark:text-slate-200">
                <span class="font-semibold">{{ store.getUser(a.aktor_id)?.ad }}</span> · {{ a.action }}
              </div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                {{ formatRelative(a.t) }} · <span class="font-mono">{{ a.target }}</span>
              </div>
            </div>
          </li>
        </ol>
      </Card>
    </div>
  </main>
</template>
