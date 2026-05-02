import api from './api'

export async function getModels() {
  const { data } = await api.get('/equipment/models')
  return data
}

export async function requestModel(modelId) {
  const { data } = await api.post('/equipment/talepler', {
    requested_model_id: modelId,
  })
  return data
}

export async function getMyInventory() {
  const { data } = await api.get('/equipment/my-inventory')
  return data
}
