import api from './api'

export async function getPendingTransactions() {
  const { data } = await api.get('/transactions/pending')
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

export async function approveTransfer(transactionId) {
  const { data } = await api.post('/transactions/devir-nihai-malzemeci-onayi', {
    transaction_id: transactionId,
  })
  return data
}
