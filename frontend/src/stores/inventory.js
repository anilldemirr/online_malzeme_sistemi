import { defineStore } from 'pinia'
import { computed } from 'vue'

const SEED_USERS = [
  { id: 'U001', ad: 'Elif Yılmaz',  rol: 'uye',      avatar: 'EY', renk: '#73B928' },
  { id: 'U002', ad: 'Mert Kaya',    rol: 'uye',      avatar: 'MK', renk: '#0EA5E9' },
  { id: 'U003', ad: 'Zeynep Aksoy', rol: 'uye',      avatar: 'ZA', renk: '#F59E0B' },
  { id: 'U004', ad: 'Ayşe Demir',   rol: 'yonetici', avatar: 'AD', renk: '#10B981' },
  { id: 'U005', ad: 'Cem Öztürk',   rol: 'yonetici', avatar: 'CÖ', renk: '#F43F5E' },
]

const SEED_MODELS = [
  { id: 'M01', model_adi: 'Vertex Vent',         marka: 'Petzl',      kategori: 'kask',     tip: 'teknik', icon: 'Helmet',    aciklama: 'Hafif havalandırmalı tırmanış kaskı' },
  { id: 'M02', model_adi: 'Volta 9.2mm',         marka: 'Petzl',      kategori: 'ip',       tip: 'teknik', icon: 'Rope',      aciklama: 'Tek ip, çok yönlü dinamik halat' },
  { id: 'M03', model_adi: 'Djinn Axess',         marka: 'Petzl',      kategori: 'karabina', tip: 'teknik', icon: 'Carabiner', aciklama: 'D tipi, vidalı karabina' },
  { id: 'M04', model_adi: 'Corax LT',            marka: 'Petzl',      kategori: 'emniyet',  tip: 'teknik', icon: 'Carabiner', aciklama: 'Ayarlanabilir emniyet kemeri' },
  { id: 'M05', model_adi: 'Quark',               marka: 'Petzl',      kategori: 'buzkazma', tip: 'teknik', icon: 'Ice',       aciklama: 'Teknik buz kazması' },
  { id: 'M06', model_adi: 'Vasak LeverLock',     marka: 'Petzl',      kategori: 'krampon',  tip: 'teknik', icon: 'Boot',      aciklama: '12 dişli klasik krampon' },
  { id: 'M07', model_adi: 'Mutant 38',           marka: 'Osprey',     kategori: 'sirt',     tip: 'teknik', icon: 'Backpack',  aciklama: 'Alpin sırt çantası, 38L' },
  { id: 'M08', model_adi: 'Hubba Hubba NX',      marka: 'MSR',        kategori: 'cadir',    tip: 'teknik', icon: 'Tent',      aciklama: 'İki kişilik üç mevsim çadır' },
  { id: 'M09', model_adi: 'Suunto MC-2',         marka: 'Suunto',     kategori: 'pusula',   tip: 'teknik', icon: 'Compass',   aciklama: 'Aynalı saha pusulası' },
  { id: 'M10', model_adi: 'Tırmanışın Esasları', marka: 'Alpin Yay.', kategori: 'kitap',    tip: 'kitap',  icon: 'Book',      aciklama: 'Kaya tırmanışı temel teknikler kitabı' },
  { id: 'M11', model_adi: 'Buzul Yürüyüşü',     marka: 'Alpin Yay.', kategori: 'kitap',    tip: 'kitap',  icon: 'Book',      aciklama: 'Glasiyer ilerleme ve yarık kurtarma' },
]

const SEED_ITEMS = [
  { id: 'I001', model_id: 'M01', demirbas_no: 'KASK-001', durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I002', model_id: 'M01', demirbas_no: 'KASK-002', durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I003', model_id: 'M01', demirbas_no: 'KASK-003', durum: 'kullanimda', sahip_id: 'U001', tip: 'teknik' },
  { id: 'I004', model_id: 'M01', demirbas_no: 'KASK-004', durum: 'staging',    sahip_id: null,   tip: 'teknik' },
  { id: 'I010', model_id: 'M02', demirbas_no: 'IP-001',   durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I011', model_id: 'M02', demirbas_no: 'IP-002',   durum: 'kullanimda', sahip_id: 'U002', tip: 'teknik' },
  { id: 'I012', model_id: 'M02', demirbas_no: 'IP-003',   durum: 'staging',    sahip_id: null,   tip: 'teknik' },
  { id: 'I020', model_id: 'M03', demirbas_no: 'KRB-001',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I021', model_id: 'M03', demirbas_no: 'KRB-002',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I022', model_id: 'M03', demirbas_no: 'KRB-003',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I023', model_id: 'M03', demirbas_no: 'KRB-004',  durum: 'kullanimda', sahip_id: 'U001', tip: 'teknik' },
  { id: 'I030', model_id: 'M04', demirbas_no: 'EMN-001',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I031', model_id: 'M04', demirbas_no: 'EMN-002',  durum: 'kullanimda', sahip_id: 'U001', tip: 'teknik' },
  { id: 'I040', model_id: 'M05', demirbas_no: 'BZK-001',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I041', model_id: 'M05', demirbas_no: 'BZK-002',  durum: 'staging',    sahip_id: null,   tip: 'teknik' },
  { id: 'I050', model_id: 'M06', demirbas_no: 'KRP-001',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I051', model_id: 'M06', demirbas_no: 'KRP-002',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I060', model_id: 'M07', demirbas_no: 'SRT-001',  durum: 'kullanimda', sahip_id: 'U002', tip: 'teknik' },
  { id: 'I061', model_id: 'M07', demirbas_no: 'SRT-002',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I070', model_id: 'M08', demirbas_no: 'CDR-001',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I080', model_id: 'M09', demirbas_no: 'PSL-001',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I081', model_id: 'M09', demirbas_no: 'PSL-002',  durum: 'depoda',     sahip_id: null,   tip: 'teknik' },
  { id: 'I090', model_id: 'M10', demirbas_no: 'KTP-001',  durum: 'kullanimda', sahip_id: 'U003', tip: 'kitap' },
  { id: 'I091', model_id: 'M10', demirbas_no: 'KTP-002',  durum: 'depoda',     sahip_id: null,   tip: 'kitap' },
  { id: 'I100', model_id: 'M11', demirbas_no: 'KTP-003',  durum: 'depoda',     sahip_id: null,   tip: 'kitap' },
]

const now = Date.now()
const ago = (h) => new Date(now - h * 3600 * 1000).toISOString()

const SEED_TRANSACTIONS = [
  { id: 'T001', tip: 'talep', durum: 'beklemede', talep_eden_id: 'U002', model_id: 'M01', assigned_item_id: null, hedef_uye_id: null, b_onayli: false, created: ago(2) },
  { id: 'T002', tip: 'talep', durum: 'beklemede', talep_eden_id: 'U003', model_id: 'M03', assigned_item_id: null, hedef_uye_id: null, b_onayli: false, created: ago(5) },
  { id: 'T003', tip: 'talep', durum: 'beklemede', talep_eden_id: 'U001', model_id: 'M08', assigned_item_id: null, hedef_uye_id: null, b_onayli: false, created: ago(20) },
  { id: 'T004', tip: 'devir', durum: 'beklemede', talep_eden_id: 'U001', hedef_uye_id: 'U002', model_id: 'M01', assigned_item_id: 'I003', b_onayli: false, created: ago(1) },
  { id: 'T005', tip: 'devir', durum: 'beklemede', talep_eden_id: 'U002', hedef_uye_id: 'U003', model_id: 'M07', assigned_item_id: 'I060', b_onayli: true, created: ago(3) },
]

const SEED_AUDIT = [
  { id: 'A001', t: ago(48), aktor_id: 'U004', action: 'Sisteme giriş yapıldı', target: '—' },
  { id: 'A002', t: ago(40), aktor_id: 'U004', action: 'KRB-005 envantere eklendi (staging)', target: 'Item' },
  { id: 'A003', t: ago(20), aktor_id: 'U001', action: 'Talep oluşturuldu: Hubba Hubba NX', target: 'T003' },
  { id: 'A004', t: ago(8),  aktor_id: 'U005', action: 'Talep onaylandı: KASK-003 → Elif Yılmaz', target: 'I003' },
  { id: 'A005', t: ago(3),  aktor_id: 'U002', action: 'Devir başlatıldı: SRT-001 → Zeynep Aksoy', target: 'T005' },
  { id: 'A006', t: ago(2),  aktor_id: 'U003', action: 'Devir alındı onaylandı: SRT-001', target: 'T005' },
]

const uid = (p) => `${p}${Math.random().toString(36).slice(2, 7).toUpperCase()}`
const nowIso = () => new Date().toISOString()

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    currentUserId: 'U001',
    users: [...SEED_USERS],
    models: [...SEED_MODELS],
    items: [...SEED_ITEMS],
    transactions: [...SEED_TRANSACTIONS],
    audit: [...SEED_AUDIT],
    toasts: [],
  }),

  getters: {
    currentUser: (state) => state.users.find(u => u.id === state.currentUserId),
    isManager: (state) => state.users.find(u => u.id === state.currentUserId)?.rol === 'yonetici',
    myItems: (state) => state.items.filter(i => i.sahip_id === state.currentUserId),
    pendingRequests: (state) => state.transactions.filter(t => t.tip === 'talep' && t.durum === 'beklemede'),
    myPendingRequests: (state) => state.transactions.filter(t => t.tip === 'talep' && t.durum === 'beklemede' && t.talep_eden_id === state.currentUserId),
    pendingTransfers: (state) => state.transactions.filter(t => t.tip === 'devir' && t.durum === 'beklemede'),
    stagedItems: (state) => state.items.filter(i => i.durum === 'staging'),
  },

  actions: {
    getUser(id) { return this.users.find(u => u.id === id) },
    getModel(id) { return this.models.find(m => m.id === id) },
    getItem(id) { return this.items.find(i => i.id === id) },
    availableItemsForModel(modelId) { return this.items.filter(i => i.model_id === modelId && i.durum === 'depoda') },

    setUser(id) { this.currentUserId = id },

    toast(msg, tone = 'success') {
      const id = uid('TS')
      this.toasts.push({ id, msg, tone })
      setTimeout(() => {
        const idx = this.toasts.findIndex(t => t.id === id)
        if (idx !== -1) this.toasts.splice(idx, 1)
      }, 3500)
    },

    requestModel(model) {
      const tx = {
        id: uid('T'), tip: 'talep', durum: 'beklemede',
        talep_eden_id: this.currentUserId,
        model_id: model.id,
        assigned_item_id: null, hedef_uye_id: null, b_onayli: false,
        created: nowIso(),
      }
      this.transactions.unshift(tx)
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `Talep oluşturuldu: ${model.model_adi}`, target: tx.id })
      this.toast(`Talep oluşturuldu: ${model.model_adi}`)
    },

    fulfillRequest(transactionId, itemId) {
      const tx = this.transactions.find(t => t.id === transactionId)
      const item = this.items.find(i => i.id === itemId)
      if (!tx || !item) return
      const txIdx = this.transactions.indexOf(tx)
      this.transactions[txIdx] = { ...tx, durum: 'onaylandi', assigned_item_id: itemId }
      const itemIdx = this.items.indexOf(item)
      this.items[itemIdx] = { ...item, durum: 'kullanimda', sahip_id: tx.talep_eden_id }
      const requester = this.getUser(tx.talep_eden_id)
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `Talep onaylandı: ${item.demirbas_no} → ${requester?.ad}`, target: itemId })
      this.toast('Talep başarıyla onaylandı')
    },

    rejectRequest(transactionId) {
      const tx = this.transactions.find(t => t.id === transactionId)
      if (!tx) return
      const idx = this.transactions.indexOf(tx)
      this.transactions[idx] = { ...tx, durum: 'reddedildi' }
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: 'Talep reddedildi', target: tx.id })
      this.toast('Talep reddedildi', 'warn')
    },

    initiateTransfer(itemId, targetUserId) {
      const item = this.items.find(i => i.id === itemId)
      if (!item) return
      const tx = {
        id: uid('T'), tip: 'devir', durum: 'beklemede',
        talep_eden_id: this.currentUserId,
        hedef_uye_id: targetUserId,
        model_id: item.model_id,
        assigned_item_id: item.id,
        b_onayli: false,
        created: nowIso(),
      }
      this.transactions.unshift(tx)
      const target = this.getUser(targetUserId)
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `Devir başlatıldı: ${item.demirbas_no} → ${target?.ad}`, target: tx.id })
      this.toast('Devir başlatıldı, alıcı onayı bekleniyor')
    },

    confirmTransferReceipt(transactionId) {
      const tx = this.transactions.find(t => t.id === transactionId)
      if (!tx) return
      const idx = this.transactions.indexOf(tx)
      this.transactions[idx] = { ...tx, b_onayli: true }
      const item = this.getItem(tx.assigned_item_id)
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `Devir alındı onaylandı: ${item?.demirbas_no || ''}`, target: tx.id })
      this.toast('Teslim alındığını onayladınız')
    },

    finalizeTransfer(transactionId) {
      const tx = this.transactions.find(t => t.id === transactionId)
      if (!tx) return
      const idx = this.transactions.indexOf(tx)
      this.transactions[idx] = { ...tx, durum: 'onaylandi' }
      const itemIdx = this.items.findIndex(i => i.id === tx.assigned_item_id)
      if (itemIdx !== -1) this.items[itemIdx] = { ...this.items[itemIdx], sahip_id: tx.hedef_uye_id }
      const item = this.getItem(tx.assigned_item_id)
      const target = this.getUser(tx.hedef_uye_id)
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `Devir tamamlandı: ${item?.demirbas_no || ''} → ${target?.ad}`, target: tx.id })
      this.toast('Devir tamamlandı, defter güncellendi')
    },

    promoteFromStaging(itemId) {
      const idx = this.items.findIndex(i => i.id === itemId)
      if (idx === -1) return
      const item = this.items[idx]
      this.items[idx] = { ...item, durum: 'depoda' }
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `Staging → Depo: ${item.demirbas_no}`, target: itemId })
      this.toast('Malzeme depoya alındı')
    },

    returnItem(itemId) {
      const idx = this.items.findIndex(i => i.id === itemId)
      if (idx === -1) return
      const item = this.items[idx]
      this.items[idx] = { ...item, durum: 'depoda', sahip_id: null }
      this.audit.unshift({ id: uid('A'), t: nowIso(), aktor_id: this.currentUserId, action: `İade edildi: ${item.demirbas_no}`, target: itemId })
      this.toast('Malzeme iade edildi')
    },

    resetData() {
      this.currentUserId = 'U001'
      this.users = [...SEED_USERS]
      this.models = [...SEED_MODELS]
      this.items = [...SEED_ITEMS]
      this.transactions = [...SEED_TRANSACTIONS]
      this.audit = [...SEED_AUDIT]
      this.toasts = []
      this.toast('Demo verisi sıfırlandı', 'info')
    },
  },
})

export function formatRelative(iso) {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000
  if (diff < 60) return 'az önce'
  if (diff < 3600) return `${Math.floor(diff / 60)} dk önce`
  if (diff < 86400) return `${Math.floor(diff / 3600)} saat önce`
  return `${Math.floor(diff / 86400)} gün önce`
}
