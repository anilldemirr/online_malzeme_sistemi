import api from './api'

export async function getPendingTransactions() {
  const { data } = await api.get('/transactions/pending')
  return data
}

export async function assignEquipment(itemId, targetUserId) {
  const { data } = await api.post('/transactions/dogrudan-zimmetle', {
    equipment_item_id: itemId,
    hedef_uye_id: targetUserId,
  })
  return data
}

export async function acceptAssignment(transactionId) {
  const { data } = await api.post('/transactions/dogrudan-zimmet-onayla', {
    transaction_id: transactionId,
  })
  return data
}

export async function rejectAssignment(transactionId) {
  const { data } = await api.post('/transactions/dogrudan-zimmet-reddet', {
    transaction_id: transactionId,
  })
  return data
}

export async function approveRequest(transactionId, assignedItemId) {
  const { data } = await api.post('/equipment/talepler/onayla-ve-ata', {
    transaction_id: transactionId,
    assigned_item_id: assignedItemId,
  })
  return data
}

export async function initiateTransfer(itemId, targetUserId) {
  const { data } = await api.post('/transactions/devir-talebi-baslat', {
    equipment_item_id: itemId,
    hedef_uye_id: targetUserId,
  })
  return data
}

export async function approveTransferReceipt(transactionId) {
  const { data } = await api.post('/transactions/devir-alici-onayi', {
    transaction_id: transactionId,
  })
  return data
}

export async function finalizeTransfer(transactionId) {
  const { data } = await api.post('/transactions/devir-nihai-malzemeci-onayi', {
    transaction_id: transactionId,
  })
  return data
}
