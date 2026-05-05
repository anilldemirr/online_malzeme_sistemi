import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { getModels, requestModel, getMyInventory } from '../services/equipment'
import { initiateTransfer, approveTransferReceipt, finalizeTransfer, assignEquipment, acceptAssignment, rejectAssignment } from '../services/transactions'

export function formatRelative(date) {
  if (!date) return ''
  const d = new Date(date)
  const now = new Date()
  const diffMs = now - d
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Az önce'
  if (diffMins < 60) return `${diffMins}dk önce`
  if (diffHours < 24) return `${diffHours}sa önce`
  if (diffDays < 7) return `${diffDays}g önce`
  return d.toLocaleDateString('tr-TR')
}

const DEMO_MODELS = [
  {
    id: 1,
    kategori: 'teknik_malzeme',
    marka_yayin_evi: 'Black Diamond',
    model_adi: 'Climbing Harness',
    require_staging: true,
    icon: 'Harness',
  },
  {
    id: 2,
    kategori: 'teknik_malzeme',
    marka_yayin_evi: 'Petzl',
    model_adi: 'ATC Carabiner',
    require_staging: true,
    icon: 'Carabiner',
  },
  {
    id: 3,
    kategori: 'kitap',
    marka_yayin_evi: 'Mountain Press',
    model_adi: 'Rock Climbing Basics',
    require_staging: false,
    icon: 'BookOpen',
  },
  {
    id: 4,
    kategori: 'kitap',
    marka_yayin_evi: 'Alpine Books',
    model_adi: 'Mountaineering Routes',
    require_staging: false,
    icon: 'BookOpen',
  },
]

const DEMO_USERS = [
  { id: 1, ad: 'Ali', rol: 'member' },
  { id: 2, ad: 'Veli', rol: 'manager' },
  { id: 3, ad: 'Ayşe', rol: 'member' },
]

const DEMO_ITEMS = [
  { id: 1, model_id: 1, demirbas_no: 'DM-001', durum: 'depoda' },
  { id: 2, model_id: 1, demirbas_no: 'DM-002', durum: 'depoda' },
  { id: 3, model_id: 2, demirbas_no: 'DM-003', durum: 'kullanimda' },
  { id: 4, model_id: 3, demirbas_no: 'DM-004', durum: 'depoda' },
  { id: 5, model_id: 4, demirbas_no: 'DM-005', durum: 'depoda' },
]

const DEMO_TRANSACTIONS = [
  {
    id: 1,
    requested_model_id: 1,
    assigned_item_id: null,
    talep_eden_id: 1,
    hedef_uye_id: null,
    islem_turu: 'depodan_alma',
    islem_durumu: 'beklemede',
    tarih: new Date(Date.now() - 3600000),
  },
  {
    id: 2,
    requested_model_id: 3,
    assigned_item_id: null,
    talep_eden_id: 3,
    hedef_uye_id: null,
    islem_turu: 'depodan_alma',
    islem_durumu: 'beklemede',
    tarih: new Date(Date.now() - 1800000),
  },
]

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    models: DEMO_MODELS,
    items: DEMO_ITEMS,
    transactions: DEMO_TRANSACTIONS,
    users: DEMO_USERS,
    audit: [
      {
        id: 1,
        aktor_id: 2,
        action: 'Created equipment',
        target: 'DM-001',
        t: new Date(Date.now() - 86400000),
      },
    ],
  }),
  getters: {
    currentUser: (state) => {
      const authStore = useAuthStore()
      return state.users.find(u => u.id === authStore.user?.id) || state.users[0]
    },
    currentUserId: (state) => {
      const authStore = useAuthStore()
      return authStore.user?.id || 1
    },
    isManager: (state) => {
      const authStore = useAuthStore()
      return authStore.user?.rol === 'manager'
    },
    myItems: (state) => {
      const currentUserId = (() => {
        const authStore = useAuthStore()
        return authStore.user?.id || 1
      })()
      return state.items.filter(item => {
        const lastTransaction = (state.transactions || [])
          .filter(
            t =>
              t.assigned_item_id === item.id &&
              t.hedef_uye_id === currentUserId &&
              t.islem_durumu === 'onaylandi'
          )
          .sort((a, b) => new Date(b.tarih) - new Date(a.tarih))[0]
        return lastTransaction && item.durum === 'kullanimda'
      })
    },
    myPendingRequests: (state) => {
      const currentUserId = (() => {
        const authStore = useAuthStore()
        return authStore.user?.id || 1
      })()
      return (state.transactions || []).filter(
        t => t.talep_eden_id === currentUserId && t.islem_turu === 'depodan_alma' && t.islem_durumu === 'beklemede'
      )
    },
    pendingRequests: (state) => {
      return (state.transactions || []).filter(
        t =>
          t.islem_turu === 'depodan_alma' &&
          t.islem_durumu === 'beklemede' &&
          !t.assigned_item_id
      )
    },
    pendingAssignments: (state) => {
      return (state.transactions || []).filter(
        t =>
          t.islem_turu === 'dogrudan_zimmet' &&
          t.islem_durumu === 'beklemede' &&
          !t.assigned_item_id
      )
    },
    pendingTransfers: (state) => {
      return (state.transactions || []).filter(t => t.islem_turu === 'devir' && (t.islem_durumu === 'alici_onayi_bekliyor' || t.islem_durumu === 'malzemeci_onayi_bekliyor'))
    },
    incomingAssignments: (state) => {
      const currentUserId = (() => {
        const authStore = useAuthStore()
        return authStore.user?.id || 1
      })()
      return (state.transactions || []).filter(
        t => t.islem_turu === 'dogrudan_zimmet' && t.islem_durumu === 'beklemede' && t.hedef_uye_id === currentUserId
      )
    },
    stagedItems: (state) => {
      return []
    },
  },
  actions: {
    getUser(userId) {
      return this.users.find(u => u.id === userId)
    },
    getModel(modelId) {
      return this.models.find(m => m.id === modelId)
    },
    getItem(itemId) {
      return this.items.find(i => i.id === itemId)
    },
    availableItemsForModel(modelId) {
      return this.items.filter(i => i.model_id === modelId && i.durum === 'depoda')
    },
    async requestModel(model) {
      try {
        const response = await requestModel(model.id)
        const tx = {
          id: Math.max(...this.transactions.map(t => t.id), 0) + 1,
          requested_model_id: model.id,
          assigned_item_id: null,
          talep_eden_id: this.currentUserId,
          hedef_uye_id: null,
          islem_turu: 'depodan_alma',
          islem_durumu: 'beklemede',
          tarih: new Date(),
        }
        this.transactions.push(tx)
      } catch (error) {
        console.error('Request failed:', error)
      }
    },
    fulfillRequest(transactionId, itemId) {
      const tx = this.transactions.find(t => t.id === transactionId)
      if (!tx) return
      const item = this.items.find(i => i.id === parseInt(itemId))
      if (!item) return
      tx.assigned_item_id = item.id
      tx.hedef_uye_id = tx.talep_eden_id
      tx.islem_durumu = 'onaylandi'
      item.durum = 'kullanimda'
    },
    rejectRequest(transactionId) {
      const tx = this.transactions.find(t => t.id === transactionId)
      if (tx) {
        tx.islem_durumu = 'reddedildi'
      }
    },
    async initiateTransfer(itemId, targetUserId) {
      try {
        const response = await initiateTransfer(itemId, targetUserId)
        const tx = {
          id: response.id || Math.max(...this.transactions.map(t => t.id), 0) + 1,
          requested_model_id: response.requested_model_id,
          assigned_item_id: response.assigned_item_id,
          talep_eden_id: response.talep_eden_id,
          hedef_uye_id: response.hedef_uye_id,
          islem_turu: 'devir',
          islem_durumu: response.islem_durumu,
          tarih: new Date(response.tarih),
        }
        this.transactions.push(tx)
      } catch (error) {
        console.error('Transfer initiation failed:', error)
      }
    },
    async confirmTransferReceipt(transactionId) {
      try {
        const response = await approveTransferReceipt(transactionId)
        const tx = this.transactions.find(t => t.id === transactionId)
        if (tx) {
          tx.islem_durumu = response.islem_durumu
        }
      } catch (error) {
        console.error('Transfer receipt approval failed:', error)
      }
    },
    async finalizeTransfer(transactionId) {
      try {
        const response = await finalizeTransfer(transactionId)
        const tx = this.transactions.find(t => t.id === transactionId)
        if (tx) {
          tx.islem_durumu = response.islem_durumu
        }
      } catch (error) {
        console.error('Transfer finalization failed:', error)
      }
    },
    returnItem(itemId) {
      const item = this.items.find(i => i.id === itemId)
      if (item) {
        item.durum = 'depoda'
      }
    },
    promoteFromStaging(stagedItemId) {
    },
    async assignEquipmentToMember(itemId, targetUserId) {
      try {
        const response = await assignEquipment(itemId, targetUserId)
        if (!response || !response.id) throw new Error('Invalid response from server')
        
        const tx = {
          id: response.id,
          requested_model_id: response.requested_model_id,
          assigned_item_id: response.assigned_item_id,
          talep_eden_id: response.talep_eden_id,
          hedef_uye_id: response.hedef_uye_id,
          onaylayan_malzemeci_id: response.onaylayan_malzemeci_id,
          islem_turu: response.islem_turu,
          islem_durumu: response.islem_durumu,
          tarih: response.tarih ? new Date(response.tarih) : new Date(),
        }
        this.transactions.push(tx)
      } catch (error) {
        console.error('Assignment failed:', error)
        throw error
      }
    },
    async acceptEquipmentAssignment(transactionId) {
      try {
        const response = await acceptAssignment(transactionId)
        const tx = this.transactions.find(t => t.id === transactionId)
        if (tx) {
          tx.islem_durumu = 'onaylandi'
          const item = this.items.find(i => i.id === tx.assigned_item_id)
          if (item) item.durum = 'kullanimda'
        }
      } catch (error) {
        console.error('Assignment acceptance failed:', error)
      }
    },
    async rejectEquipmentAssignment(transactionId) {
      try {
        const response = await rejectAssignment(transactionId)
        const tx = this.transactions.find(t => t.id === transactionId)
        if (tx) {
          tx.islem_durumu = 'reddedildi'
        }
      } catch (error) {
        console.error('Assignment rejection failed:', error)
      }
    },
    setUser(userId) {
      const authStore = useAuthStore()
      const user = this.users.find(u => u.id === userId)
      if (user) {
        const role = user.rol === 'manager' ? 'manager' : 'member'
        authStore.login(userId, role)
      }
    },
    initializeApp() {
      const authStore = useAuthStore()
      if (!authStore.user) {
        this.setUser(1)
      }
    },
  },
})
