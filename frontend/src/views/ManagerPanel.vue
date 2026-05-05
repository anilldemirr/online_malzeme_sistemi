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

const tab = ref('assignments')
const fulfillTx = ref(null)
const selectedItemId = ref('')

const tabs = computed(() => [
  { id: 'assignments', label: 'Atamalar', icon: 'Zap', count: store.pendingAssignments.length },
  { id: 'book-requests', label: 'Kitap Talepleri', icon: 'Inbox', count: store.pendingRequests.length },
  { id: 'transfers', label: 'Devirler', icon: 'Switch', count: store.pendingTransfers.length },
  { id: 'staging', label: 'Staging', icon: 'Layers', count: store.stagedItems.length },
  { id: 'audit', label: 'Denetim', icon: 'History', count: null },
])

function openFulfill(tx) { fulfillTx.value = tx; selectedItemId.value = '' }
async function doFulfill() {
  if (!fulfillTx.value || !selectedItemId.value) return
  
  // Check if this is a technical equipment assignment (tab context)
  const isAssignment = tab.value === 'assignments'
  
  try {
    if (isAssignment) {
      // Technical equipment: Direct assignment to member
      await store.assignEquipmentToMember(selectedItemId.value, fulfillTx.value.hedef_uye_id)
    } else {
      // Books: Traditional fulfill request flow
      store.fulfillRequest(fulfillTx.value.id, selectedItemId.value)
    }
    
    fulfillTx.value = null
  } catch (error) {
    console.error('Fulfillment failed:', error)
    // Keep modal open on error so user can retry
  }
}
</script>

<template>
  <main :class="store.isManager ? 'max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8' : 'max-w-3xl mx-auto px-4 md:px-8 py-16'">
    <!-- 403 guard -->
    <template v-if="!store.isManager">
      <Card class="p-8 text-center anim-fade">
        <div class="w-16 h-16 rounded-2xl bg-rose-50 dark:bg-rose-500/15 text-rose-600 dark:text-rose-300 flex items-center justify-center mx-auto mb-4">
          <AppIcon name="Shield" :size="28" />
        </div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-50">Erişim Engellendi · 403</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-2 max-w-sm mx-auto">
          Yönetici paneline yalnızca yönetici rolündeki kullanıcılar erişebilir. Test için sağ üstten kullanıcı değiştirin.
        </p>
        <div class="mt-6">
          <Button variant="primary" icon="Home" @click="router.push({ name: 'dashboard' })">Genel Bakışa Dön</Button>
        </div>
      </Card>
    </template>

    <template v-else>
    <header class="mb-6 anim-fade flex items-start justify-between gap-4 flex-wrap">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <AppIcon name="Shield" :size="14" class="text-brand" />
          <span class="text-xs font-semibold uppercase tracking-wider text-brand-dark dark:text-brand-light">Yönetici Paneli</span>
        </div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-50">İşlem Kuyruğu</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Talepleri karşılayın, devirleri sonlandırın, envanteri sahaya alın.</p>
      </div>
    </header>

    <!-- Tabs -->
    <div class="border-b border-slate-200 dark:border-slate-700 mb-6 overflow-x-auto">
      <div class="flex items-center gap-1 min-w-max">
        <button
          v-for="t in tabs"
          :key="t.id"
          @click="tab = t.id"
          :class="[
            'relative inline-flex items-center gap-2 h-12 px-4 text-sm font-medium transition-colors',
            tab === t.id
              ? 'text-brand-dark dark:text-brand-light'
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100',
          ]"
          :aria-current="tab === t.id ? 'page' : undefined"
        >
          <AppIcon :name="t.icon" :size="16" />
          {{ t.label }}
          <span
            v-if="t.count !== null && t.count > 0"
            :class="[
              'inline-flex items-center justify-center min-w-[20px] h-5 px-1.5 text-[11px] font-bold rounded-full',
              tab === t.id ? 'bg-brand text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300',
            ]"
          >{{ t.count }}</span>
          <span v-if="tab === t.id" class="absolute bottom-0 left-2 right-2 h-0.5 bg-brand rounded-t-full" />
        </button>
      </div>
    </div>

    <!-- Assignments tab (Technical Equipment) -->
    <div v-if="tab === 'assignments'" class="anim-fade">
      <Card v-if="store.pendingAssignments.length === 0" class="p-0">
        <EmptyState icon="Zap" title="Teknik malzeme atama yok" body="Tüm atamalar tamamlanmış veya beklemede." />
      </Card>
      <div v-else class="flex flex-col gap-3">
        <Card v-for="t in store.pendingAssignments" :key="t.id" class="p-4">
          <div class="flex flex-col md:flex-row md:items-center gap-4">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <div class="w-10 h-10 rounded-alpine bg-brand-soft dark:bg-brand/15 text-brand-dark dark:text-brand-light flex items-center justify-center shrink-0">
                <AppIcon :name="store.getModel(t.requested_model_id)?.icon || 'Box'" :size="18" />
              </div>
              <div class="min-w-0">
                <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.getModel(t.requested_model_id)?.model_adi }}</div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400">→ {{ store.getUser(t.hedef_uye_id)?.ad }}</div>
              </div>
            </div>
            <div class="flex items-center gap-3 shrink-0">
              <div class="text-right hidden sm:block">
                <div class="text-[11px] text-slate-500 dark:text-slate-400">{{ formatRelative(t.tarih) }}</div>
                <div :class="['text-[11px] font-semibold', store.availableItemsForModel(t.requested_model_id).length > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400']">
                  {{ store.availableItemsForModel(t.requested_model_id).length }} depoda
                </div>
              </div>
              <Button
                variant="primary"
                size="sm"
                icon="Check"
                :disabled="store.availableItemsForModel(t.requested_model_id).length === 0"
                @click="openFulfill(t)"
              >Ata</Button>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- Book Requests tab -->
    <div v-if="tab === 'book-requests'" class="anim-fade">
      <Card v-if="store.pendingRequests.length === 0" class="p-0">
        <EmptyState icon="Inbox" title="Kitap talebi yok" body="Tüm talepler işlendi." />
      </Card>
      <div v-else class="flex flex-col gap-3">
        <Card v-for="t in store.pendingRequests" :key="t.id" class="p-4">
          <div class="flex flex-col md:flex-row md:items-center gap-4">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <Avatar :user="store.getUser(t.talep_eden_id)" :size="40" />
              <div class="min-w-0">
                <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.getUser(t.talep_eden_id)?.ad }}</div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{{ t.talep_eden_id }}</div>
              </div>
              <AppIcon name="ArrowRight" :size="14" class="text-slate-400 mx-1 hidden md:block" />
              <div class="hidden md:flex items-center gap-2.5 min-w-0">
                <div class="w-10 h-10 rounded-alpine bg-brand-soft dark:bg-brand/15 text-brand-dark dark:text-brand-light flex items-center justify-center shrink-0">
                  <AppIcon :name="store.getModel(t.requested_model_id)?.icon || 'Box'" :size="18" />
                </div>
                <div class="min-w-0">
                  <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">{{ store.getModel(t.requested_model_id)?.model_adi }}</div>
                  <div class="text-[11px] text-slate-500 dark:text-slate-400">{{ store.getModel(t.requested_model_id)?.marka_yayin_evi }}</div>
                </div>
              </div>
            </div>
            <!-- Mobile model -->
            <div class="md:hidden flex items-center gap-2.5">
              <div class="w-10 h-10 rounded-alpine bg-brand-soft dark:bg-brand/15 text-brand-dark dark:text-brand-light flex items-center justify-center shrink-0">
                <AppIcon :name="store.getModel(t.requested_model_id)?.icon || 'Box'" :size="18" />
              </div>
              <div>
                <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.getModel(t.requested_model_id)?.model_adi }}</div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400">{{ store.getModel(t.requested_model_id)?.marka_yayin_evi }}</div>
              </div>
            </div>
            <div class="flex items-center gap-3 shrink-0">
              <div class="text-right hidden sm:block">
                <div class="text-[11px] text-slate-500 dark:text-slate-400">{{ formatRelative(t.tarih) }}</div>
                <div :class="['text-[11px] font-semibold', store.availableItemsForModel(t.requested_model_id).length > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400']">
                  {{ store.availableItemsForModel(t.requested_model_id).length }} depoda
                </div>
              </div>
              <Button variant="outline" size="sm" @click="store.rejectRequest(t.id)">Reddet</Button>
              <Button
                variant="primary"
                size="sm"
                icon="Check"
                :disabled="t.talep_eden_id === store.currentUserId || store.availableItemsForModel(t.requested_model_id).length === 0"
                @click="openFulfill(t)"
              >Onayla</Button>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- Transfers tab -->
    <div v-if="tab === 'transfers'" class="anim-fade">
      <Card v-if="store.pendingTransfers.length === 0" class="p-0">
        <EmptyState icon="Switch" title="Bekleyen devir işlemi yok" body="Üyeler arası devirler buradan sonlandırılır." />
      </Card>
      <div v-else class="flex flex-col gap-3">
        <Card v-for="t in store.pendingTransfers" :key="t.id" class="p-4">
          <div class="flex flex-col lg:flex-row lg:items-center gap-4">
            <!-- Three-way visual -->
            <div class="flex items-center gap-2 flex-1 min-w-0">
              <div class="flex flex-col items-center gap-1 shrink-0">
                <Avatar :user="store.getUser(t.talep_eden_id)" :size="40" />
                <span class="text-[10px] text-slate-500 dark:text-slate-400 font-medium">{{ store.getUser(t.talep_eden_id)?.ad?.split(' ')[0] }}</span>
              </div>
              <div class="flex flex-col items-center gap-0.5 px-1">
                <AppIcon name="ArrowRight" :size="14" class="text-emerald-500" />
                <span class="text-[9px] text-emerald-600 dark:text-emerald-400 font-bold uppercase">Başlattı</span>
              </div>
              <div class="flex flex-col items-center gap-1 shrink-0">
                <Avatar :user="store.getUser(t.hedef_uye_id)" :size="40" />
                <span class="text-[10px] text-slate-500 dark:text-slate-400 font-medium">{{ store.getUser(t.hedef_uye_id)?.ad?.split(' ')[0] }}</span>
              </div>
              <div class="flex flex-col items-center gap-0.5 px-1">
                <AppIcon name="ArrowRight" :size="14" :class="t.islem_durumu === 'malzemeci_onayi_bekliyor' || t.islem_durumu === 'onaylandi' ? 'text-emerald-500' : 'text-slate-300 dark:text-slate-600'" />
                <span :class="['text-[9px] font-bold uppercase', t.islem_durumu === 'malzemeci_onayi_bekliyor' || t.islem_durumu === 'onaylandi' ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400']">{{ t.islem_durumu === 'malzemeci_onayi_bekliyor' || t.islem_durumu === 'onaylandi' ? 'Onayladı' : 'Bekliyor' }}</span>
              </div>
              <div class="flex flex-col items-center gap-1 shrink-0">
                <div class="w-10 h-10 rounded-full bg-brand-soft dark:bg-brand/15 text-brand-dark dark:text-brand-light flex items-center justify-center">
                  <AppIcon name="Shield" :size="18" />
                </div>
                <span class="text-[10px] text-slate-500 dark:text-slate-400 font-medium">Yönetici</span>
              </div>
            </div>
            <!-- Item details -->
            <div class="flex items-center gap-3 lg:w-64 lg:shrink-0">
              <div class="w-10 h-10 rounded-alpine bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center shrink-0">
                <AppIcon :name="store.getModel(t.requested_model_id)?.icon || 'Box'" :size="18" />
              </div>
              <div class="min-w-0">
                <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">{{ store.getModel(t.requested_model_id)?.model_adi }}</div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{{ store.getItem(t.assigned_item_id)?.demirbas_no }}</div>
              </div>
            </div>
            <!-- Action -->
            <div class="flex items-center gap-2 shrink-0">
              <Button
                variant="primary"
                size="sm"
                icon="CheckCircle"
                :disabled="(t.talep_eden_id === store.currentUserId || t.hedef_uye_id === store.currentUserId) || t.islem_durumu !== 'malzemeci_onayi_bekliyor'"
                @click="store.finalizeTransfer(t.id)"
              >Devri Sonlandır</Button>
            </div>
          </div>
          <!-- SoD or waiting notice -->
          <div
            v-if="t.talep_eden_id === store.currentUserId || t.hedef_uye_id === store.currentUserId"
            class="mt-3 flex items-start gap-2 text-xs p-2.5 rounded-md bg-rose-50 dark:bg-rose-500/10 text-rose-700 dark:text-rose-300 border border-rose-200/50 dark:border-rose-500/20"
          >
            <AppIcon name="AlertTriangle" :size="14" class="mt-0.5 shrink-0" />
            <span><strong>Görev Ayrılığı (SoD):</strong> Bu devirin tarafısınız, başka bir yönetici tamamlamalı.</span>
          </div>
          <div
            v-else-if="t.islem_durumu !== 'malzemeci_onayi_bekliyor'"
            class="mt-3 flex items-start gap-2 text-xs p-2.5 rounded-md bg-amber-50 dark:bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-200/50 dark:border-amber-500/20"
          >
            <AppIcon name="Clock" :size="14" class="mt-0.5 shrink-0" />
            <span>Alıcı henüz teslim aldığını onaylamadı. Onayladıktan sonra sonlandırabilirsiniz.</span>
          </div>
        </Card>
      </div>
    </div>

    <!-- Staging tab -->
    <div v-if="tab === 'staging'" class="anim-fade">
      <Card v-if="store.stagedItems.length === 0" class="p-0">
        <EmptyState icon="Layers" title="Staging alanında bekleyen ürün yok" body="Yeni teknik malzemeler kayıt sırasında buraya düşer ve yıllık denetim sonrası dolaşıma alınır." />
      </Card>
      <div v-else>
        <div class="mb-4 p-3 rounded-alpine bg-violet-50/50 dark:bg-violet-500/10 border border-violet-200/50 dark:border-violet-500/20 text-xs text-violet-700 dark:text-violet-300 flex items-start gap-2">
          <AppIcon name="Layers" :size="14" class="mt-0.5" />
          <span><strong>Staging mantığı:</strong> Teknik malzemeler önce burada bekler. Yıllık denetim sonrası "Depoda" durumuna alınır. Yayınlar bu adımı atlar.</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <Card v-for="it in store.stagedItems" :key="it.id" class="p-4 flex items-center gap-3">
            <div class="w-12 h-12 rounded-alpine bg-violet-100 dark:bg-violet-500/15 text-violet-700 dark:text-violet-300 flex items-center justify-center shrink-0">
              <AppIcon :name="store.getModel(it.model_id)?.icon || 'Box'" :size="22" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">{{ store.getModel(it.model_id)?.model_adi }}</div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{{ it.demirbas_no }}</div>
            </div>
            <Button size="sm" icon="Check" @click="store.promoteFromStaging(it.id)">Sahaya Al</Button>
          </Card>
        </div>
      </div>
    </div>

    <!-- Audit tab -->
    <div v-if="tab === 'audit'" class="anim-fade">
      <Card class="p-0 overflow-hidden">
        <div class="px-5 py-3 border-b border-slate-200 dark:border-slate-700 flex items-center gap-2 bg-slate-50/50 dark:bg-slate-900/30">
          <AppIcon name="Shield" :size="14" class="text-brand" />
          <span class="text-xs font-semibold text-slate-700 dark:text-slate-300">Değiştirilemez Kayıt · {{ store.audit.length }} kayıt</span>
        </div>
        <ol class="divide-y divide-slate-100 dark:divide-slate-800">
          <li v-for="a in store.audit" :key="a.id" class="flex items-start gap-3 px-5 py-3.5">
            <Avatar :user="store.getUser(a.aktor_id)" :size="32" />
            <div class="flex-1 min-w-0">
              <div class="text-sm text-slate-700 dark:text-slate-200">
                <span class="font-semibold">{{ store.getUser(a.aktor_id)?.ad }}</span> · {{ a.action }}
              </div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 flex items-center gap-2">
                <span>{{ formatRelative(a.t) }}</span>
                <span class="font-mono">· {{ a.target }}</span>
                <span class="font-mono">· {{ a.id }}</span>
              </div>
            </div>
          </li>
        </ol>
      </Card>
    </div>

    <!-- Fulfill modal -->
    <ActionModal
      :open="!!fulfillTx"
      :title="tab === 'assignments' ? 'Malzeme Ata' : 'Talebi Karşıla'"
      :subtitle="tab === 'assignments' ? 'Bu üyeye teknik malzeme atayın' : 'Bu talebe bir fiziksel demirbaş atayın'"
      icon="CheckCircle"
      tone="brand"
      @close="fulfillTx = null"
    >
      <template v-if="fulfillTx">
        <div class="flex items-center gap-3 p-3 rounded-alpine bg-slate-50 dark:bg-slate-800/40 mb-4">
          <Avatar :user="store.getUser(tab === 'assignments' ? fulfillTx.hedef_uye_id : fulfillTx.talep_eden_id)" :size="36" />
          <AppIcon name="ArrowRight" :size="14" class="text-slate-400" />
          <div class="flex-1 min-w-0">
            <div class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ store.getModel(fulfillTx.requested_model_id)?.model_adi }}</div>
            <div class="text-xs text-slate-500 dark:text-slate-400">{{ store.getUser(tab === 'assignments' ? fulfillTx.hedef_uye_id : fulfillTx.talep_eden_id)?.ad }} için</div>
          </div>
        </div>
        <label class="block text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-400 mb-2">
          Atanacak Demirbaş ({{ store.availableItemsForModel(fulfillTx.requested_model_id).length }} kullanılabilir)
        </label>
        <div v-if="store.availableItemsForModel(fulfillTx.requested_model_id).length === 0" class="text-sm text-slate-500 dark:text-slate-400 p-3 rounded-md bg-rose-50/50 dark:bg-rose-500/10 border border-rose-200/50 dark:border-rose-500/20">
          Bu model için depoda kullanılabilir demirbaş yok.
        </div>
        <div v-else class="grid grid-cols-2 gap-2 max-h-64 overflow-y-auto">
          <label
            v-for="it in store.availableItemsForModel(fulfillTx.requested_model_id)"
            :key="it.id"
            :class="[
              'flex items-center gap-2 p-2.5 rounded-alpine border cursor-pointer transition',
              selectedItemId === it.id
                ? 'border-brand bg-brand-soft/40 dark:bg-brand/10'
                : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600',
            ]"
          >
            <input type="radio" name="item" :value="it.id" v-model="selectedItemId" class="sr-only" />
            <AppIcon name="QrCode" :size="16" class="text-slate-400" />
            <span class="text-sm font-mono font-semibold text-slate-900 dark:text-slate-100">{{ it.demirbas_no }}</span>
            <AppIcon v-if="selectedItemId === it.id" name="Check" :size="14" class="ml-auto text-brand" />
          </label>
        </div>
      </template>
      <template #footer>
        <Button variant="ghost" @click="fulfillTx = null">Vazgeç</Button>
        <Button variant="primary" icon="Check" :disabled="!selectedItemId" @click="doFulfill">Onayla & Zimmetle</Button>
      </template>
    </ActionModal>
    </template>
  </main>
</template>
