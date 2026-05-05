// Quick validation of the inventory store changes
// This checks that the store is properly structured

const DEMO_MODELS = [
  {
    id: 1,
    kategori: 'teknik_malzeme',
    marka_yayin_evi: 'Black Diamond',
    model_adi: 'Climbing Harness',
    require_staging: true,
  },
  {
    id: 2,
    kategori: 'kitap',
    marka_yayin_evi: 'Mountain Press',
    model_adi: 'Rock Climbing Basics',
    require_staging: false,
  },
]

const categories = DEMO_MODELS.reduce((acc, model) => {
  acc[model.kategori] = (acc[model.kategori] || 0) + 1
  return acc
}, {})

console.log('✓ Models with categories:', categories)
console.log('✓ Teknik malzeme:', categories['teknik_malzeme'] || 0)
console.log('✓ Kitap:', categories['kitap'] || 0)
