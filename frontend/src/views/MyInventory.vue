<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore, formatRelative } from '../stores/inventory'
import AppIcon from '../components/AppIcon.vue'
import Card from '../components/ui/Card.vue'
import Button from '../components/ui/Button.vue'
import Avatar from '../components/ui/Avatar.vue'
import StatusBadge from '../components/ui/StatusBadge.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import ActionModal from '../components/ActionModal.vue'

const store = useInventoryStore()
const router = useRouter()

const transferOpen = ref(false)
const transferItem = ref(null)
const targetUserId = ref('')

const myItems = computed(() => store.myItems)

const incoming = computed(() =>
  store.transactions.filter(
    t => t.tip === 'devir' && t.durum === 'beklemede' && t.hedef_uye_id === store.currentUserId && !t.b_onayli
  )
)

const outgoing = computed(() =>
  store.transactions.filter(
    t => t.tip === 'devir' && t.durum === 'beklemede' && t.talep_eden_id === store.currentUserId
  )
)

const itemInTransit = computed(() => {
  const s = new Set()
  store.transactions.forEach(t => {
    if (t.tip === 'devir' && t.durum === 'beklemede') s.add(t.assigned_item_id)
  })
  return s
})

function openTransfer(item) {
  transferItem.value = item
  targetUserId.value = ''
  transferOpen.value = true
}

function submitTransfer() {
  if (!targetUserId.value) return
  store.initiateTransfer(transferItem.value.id, targetUserId.value)
  transferOpen.value = false
}
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8">
    <header class="mb-6 anim-fade">
      <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">Üzerimdeki Malzeme</h1>
      <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Zimmetinizdeki fiziksel envanter. Devir ve iade işlemleri buradan başlatılır.</p>
    </header>

    <!-- Incoming transfer alert -->
    <Card v-if="incoming.length > 0" class="p-4 md:p-5 mb-5 border-sky-200 dark:border-sky-500/30 bg-gradient-to-br from-sky-50/50 to-transparent dark:from-sky-500/5 anim-slide">
      <div class="flex items-center gap-2 mb-3">
        <div class="w-8 h-8 rounded-alpine bg-sky-100 dark:bg-sky-500/20 text-sky-600 dark:text-sky-300 flex items-center justify-center">
          <AppIcon name="Switch" :size="16" />
        </div>
        <div>
          <h2 class="text-base font-semibold text-slate-900 dark:text-slate-100">Teslim Alınması Bekleyen Devirler</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400">Bunları onayladıktan sonra yönetici defteri günceller.</p>
        </div>
      </div>
      <ul class="space-y-2">
        <li
          v-for="t in incoming"
          :key="t.id"
          class="flex flex-col sm:flex-row sm:items-center gap-3 p-3 rounded-alpine bg-surface-light dark:bg-surface-dark border border-slate-200 dark:border-slate-700"
        >
          <div class="flex items-center gap-3 flex-1 min-w-0">
            <Avatar :user="store.getUser(t.talep_eden_id)" :size="36" />
            <AppIcon name="ArrowRight" :size="16" class="text-slate-400 shrink-0" />
            <Avatar :user="store.currentUser" :size="36" />
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">{{ store.getModel(t.model_id)?.model_adi }}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">{{ store.getItem(t.assigned_item_id)?.demirbas_no }} · {{ store.getUser(t.talep_eden_id)?.ad }}</div>
            </div>
          </div>
          <Button size="sm" icon="Check" @click="store.confirmTransferReceipt(t.id)">Teslim Aldım</Button>
        </li>
      </ul>
    </Card>

    <!-- My items -->
    <Card v-if="myItems.length === 0" class="p-0">
      <EmptyState
        icon="Backpack"
        title="Şu an üzerinizde zimmetli malzeme bulunmuyor"
        body="Bir tırmanış için ihtiyacınız olan malzemeyi katalogdan talep edebilirsiniz."
      >
        <template #action>
          <Button variant="primary" icon="Plus" @click="router.push({ name: 'equipment' })">Kataloğa Git</Button>
        </template>
      </EmptyState>
    </Card>

    <div v-else class="flex flex-col gap-3 anim-fade">
      <Card v-for="item in myItems" :key="item.id" class="p-4 md:p-5">
        <div class="flex flex-col md:flex-row md:items-center gap-4">
          <div class="flex items-center gap-4 flex-1 min-w-0">
            <div class="w-14 h-14 md:w-16 md:h-16 rounded-alpine bg-gradient-to-br from-brand-soft to-emerald-100 dark:from-brand/15 dark:to-emerald-500/10 flex items-center justify-center text-brand-dark dark:text-brand-light shrink-0">
              <AppIcon :name="store.getModel(item.model_id)?.icon || 'Box'" :size="28" :stroke="1.4" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-[11px] font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">{{ store.getModel(item.model_id)?.marka }}</div>
              <h3 class="text-base md:text-lg font-semibold text-slate-900 dark:text-slate-100 leading-tight">{{ store.getModel(item.model_id)?.model_adi }}</h3>
              <div class="flex items-center gap-2 mt-1.5 flex-wrap">
                <span class="inline-flex items-center gap-1 text-[11px] font-mono font-semibold px-2 py-1 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                  <AppIcon name="QrCode" :size="11" /> {{ item.demirbas_no }}
                </span>
                <StatusBadge :status="item.durum" size="sm" />
                <span v-if="itemInTransit.has(item.id)" class="inline-flex items-center gap-1 text-[11px] font-medium px-2 py-1 rounded-md bg-amber-50 dark:bg-amber-500/15 text-amber-700 dark:text-amber-300">
                  <AppIcon name="Switch" :size="11" /> Devir sürüyor
                </span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <div v-if="itemInTransit.has(item.id)" class="text-xs text-slate-500 dark:text-slate-400 max-w-[180px] text-right">
              {{ outgoing.find(t => t.assigned_item_id === item.id)?.b_onayli
                ? 'Yönetici onayı bekleniyor'
                : `${store.getUser(outgoing.find(t => t.assigned_item_id === item.id)?.hedef_uye_id)?.ad} onayı bekleniyor` }}
            </div>
            <template v-else>
              <Button variant="outline" size="sm" icon="Refresh" @click="store.returnItem(item.id)">İade</Button>
              <Button variant="primary" size="sm" icon="Switch" @click="openTransfer(item)">Devret</Button>
            </template>
          </div>
        </div>
      </Card>
    </div>

    <!-- Outgoing transfers -->
    <section v-if="outgoing.length > 0" class="mt-8">
      <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">Başlattığım Devirler</h2>
      <div class="flex flex-col gap-2 anim-fade">
        <Card v-for="t in outgoing" :key="t.id" class="p-3 md:p-4">
          <div class="flex items-center gap-3 flex-wrap">
            <Avatar :user="store.currentUser" :size="32" />
            <AppIcon name="ArrowRight" :size="14" class="text-slate-400" />
            <Avatar :user="store.getUser(t.hedef_uye_id)" :size="32" />
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
                {{ store.getModel(t.model_id)?.model_adi }}
                <span class="font-mono text-xs text-slate-500">{{ store.getItem(t.assigned_item_id)?.demirbas_no }}</span>
              </div>
              <div class="text-xs text-slate-500 dark:text-slate-400">→ {{ store.getUser(t.hedef_uye_id)?.ad }} · {{ formatRelative(t.created) }}</div>
            </div>
            <!-- Transfer progress -->
            <div class="flex items-center gap-1 text-[11px]">
              <span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300">
                <AppIcon name="Check" :size="11" /> Başladı
              </span>
              <span class="w-2 h-px bg-slate-200 dark:bg-slate-700" />
              <span :class="['inline-flex items-center gap-1 px-2 py-1 rounded-md', t.b_onayli ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300' : 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400']">
                <AppIcon :name="t.b_onayli ? 'Check' : 'Clock'" :size="11" /> Alıcı
              </span>
              <span class="w-2 h-px bg-slate-200 dark:bg-slate-700" />
              <span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400">
                <AppIcon name="Clock" :size="11" /> Yönetici
              </span>
            </div>
          </div>
        </Card>
      </div>
    </section>

    <!-- Transfer modal -->
    <ActionModal
      :open="transferOpen"
      title="Devir Başlat"
      subtitle="Bu malzemeyi başka bir üyeye devretmek üzeresiniz"
      icon="Switch"
      tone="sky"
      @close="transferOpen = false"
    >
      <template v-if="transferItem">
        <div class="flex items-center gap-3 p-3 rounded-alpine bg-slate-50 dark:bg-slate-800/40 mb-4">
          <div class="w-10 h-10 rounded-alpine bg-brand-soft dark:bg-brand/15 flex items-center justify-center text-brand-dark dark:text-brand-light">
            <AppIcon :name="store.getModel(transferItem.model_id)?.icon || 'Box'" :size="18" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.getModel(transferItem.model_id)?.model_adi }}</div>
            <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">{{ transferItem.demirbas_no }}</div>
          </div>
        </div>
        <label class="block text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-400 mb-2">Alıcı Üye</label>
        <div class="space-y-2 max-h-64 overflow-y-auto -mx-1 px-1">
          <label
            v-for="u in store.users.filter(u => u.id !== store.currentUserId && u.rol === 'uye')"
            :key="u.id"
            :class="[
              'flex items-center gap-3 p-3 rounded-alpine border cursor-pointer transition',
              targetUserId === u.id
                ? 'border-brand bg-brand-soft/40 dark:bg-brand/10'
                : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600',
            ]"
          >
            <input type="radio" name="target" :value="u.id" v-model="targetUserId" class="sr-only" />
            <Avatar :user="u" :size="36" />
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ u.ad }}</div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{{ u.id }}</div>
            </div>
            <AppIcon v-if="targetUserId === u.id" name="CheckCircle" :size="18" class="text-brand" />
          </label>
        </div>
        <div class="mt-4 flex items-start gap-2 text-xs text-slate-500 dark:text-slate-400 p-3 rounded-alpine bg-amber-50/50 dark:bg-amber-500/10 border border-amber-200/50 dark:border-amber-500/20">
          <AppIcon name="AlertTriangle" :size="14" class="text-amber-600 mt-0.5 shrink-0" />
          <span>Devrin tamamlanması için alıcının onayı ve ardından bir yöneticinin son onayı gerekir.</span>
        </div>
      </template>
      <template #footer>
        <Button variant="ghost" @click="transferOpen = false">Vazgeç</Button>
        <Button variant="primary" icon="Switch" :disabled="!targetUserId" @click="submitTransfer">Deviri Başlat</Button>
      </template>
    </ActionModal>
  </main>
</template>
