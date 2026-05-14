<template>
    <header class="header">
        <img src="/LOGO.png" alt="logo" class="header-logo">
        <h2>PCPriceTracker</h2>
    </header>


    <div class="pc-builder">
    <h1>🖥️ Конфигуратор ПК</h1>
    
    <!-- Состояние загрузки -->
    <div v-if="pcComponents.isLoading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка комплектующих...</p>
    </div>
    
    <!-- Ошибка -->
    <div v-else-if="pcComponents.error" class="error">
      <p>❌ {{ pcComponents.error }}</p>
      <button @click="pcComponents.fetchAllComponents">Повторить загрузку</button>
    </div>
    
    <!-- Основной контент -->
    <div v-else>
      <!-- Статистика -->
      <div class="stats">
        <div class="stat-card">
          <span class="stat-label">Всего компонентов</span>
          <span class="stat-value">{{ pcComponents.componentsCount }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Общая стоимость</span>
          <span class="stat-value">{{ formatPrice(pcComponents.totalPrice) }} ₽</span>
        </div>
      </div>
      
      <!-- Фильтр по типу -->
      <div class="filters">
        <button 
          v-for="tab in tabs" 
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="{ active: activeTab === tab.value }"
        >
          {{ tab.label }}
          <span class="count">{{ getComponentCount(tab.value) }}</span>
        </button>
      </div>
      
      <!-- Список компонентов -->
      <div class="components-grid">
        <div 
          v-for="component in filteredComponents" 
          :key="component.id"
          class="component-card"
          :class="component.type"
        >
          <div class="component-header">
            <h3>{{ component.name }}</h3>
            <span class="brand">{{ component.brand }}</span>
          </div>
          
          <div class="component-specs">
            <!-- CPU спецификации -->
            <template v-if="component.type === 'cpu'">
              <div class="spec">⚡ {{ component.cores }} ядер / {{ component.threads }} потоков</div>
              <div class="spec">🚀 {{ component.frequency }} GHz</div>
              <div class="spec">🔌 {{ component.socket }}</div>
            </template>
            
            <!-- GPU спецификации -->
            <template v-else-if="component.type === 'gpu'">
              <div class="spec">🎮 {{ component.vram }} GB VRAM</div>
              <div class="spec">💪 TDP: {{ component.tdp }}W</div>
              <div class="spec">🔧 {{ component.chipset }}</div>
            </template>
            
            <!-- Материнская плата -->
            <template v-else-if="component.type === 'motherboard'">
              <div class="spec">🔌 {{ component.socket }}</div>
              <div class="spec">💾 {{ component.ramSlots }} слота RAM</div>
              <div class="spec">📏 {{ component.formFactor }}</div>
            </template>
            
            <!-- RAM -->
            <template v-else-if="component.type === 'ram'">
              <div class="spec">💾 {{ component.capacity }} GB</div>
              <div class="spec">⚡ {{ component.frequency }} MHz</div>
              <div class="spec">🔧 {{ component.type }}</div>
            </template>
            
            <!-- Накопитель -->
            <template v-else-if="component.type === 'storage'">
              <div class="spec">💿 {{ component.capacity }} GB</div>
              <div class="spec">🔌 {{ component.interface }}</div>
              <div class="spec">📐 {{ component.formFactor }}</div>
            </template>
            
            <!-- Блок питания -->
            <template v-else-if="component.type === 'psu'">
              <div class="spec">⚡ {{ component.wattage }}W</div>
              <div class="spec">✨ 80+ {{ component.efficiency }}</div>
            </template>
            
            <!-- Охлаждение -->
            <template v-else-if="component.type === 'cooler'">
              <div class="spec">🌀 {{ component.typeCooler === 'air' ? 'Воздушное' : 'Жидкостное' }}</div>
              <div class="spec">💨 TDP: {{ component.tdp }}W</div>
            </template>
          </div>
          
          <div class="component-footer">
            <span class="price">{{ formatPrice(component.price) }} ₽</span>
            <button @click="pcComponents.removeComponent(component.id)" class="remove-btn">
              🗑️ Удалить
            </button>
          </div>
        </div>
      </div>
      
      <!-- Кнопка обновления -->
      <button @click="pcComponents.fetchAllComponents" class="refresh-btn">
        🔄 Обновить данные
      </button>
    </div>
  </div>

</template>

<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';
    import { usePCComponentsStore } from '@/stores/PcComponents';

    const pcComponents = usePCComponentsStore()
    const activeTab = ref('all')

    const tabs = [
  { label: 'Все', value: 'all' },
  { label: 'Процессоры', value: 'cpu' },
  { label: 'Видеокарты', value: 'gpu' },
  { label: 'Материнские платы', value: 'motherboard' },
  { label: 'Оперативная память', value: 'ram' },
  { label: 'Накопители', value: 'storage' },
  { label: 'Блоки питания', value: 'psu' },
  { label: 'Охлаждение', value: 'cooler' }
];

    const filteredComponents = computed(() => {
  if (activeTab.value === 'all') return pcComponents.components;
  
  switch (activeTab.value) {
    case 'cpu': return pcComponents.cpus;
    case 'gpu': return pcComponents.gpus;
    case 'motherboard': return pcComponents.motherboards;
    case 'ram': return pcComponents.rams;
    case 'storage': return pcComponents.storages;
    case 'psu': return pcComponents.psus;
    case 'cooler': return pcComponents.coolers;
    default: return pcComponents.components;
  }
});

    const getComponentCount = (type: string) => {
  switch (type) {
    case 'cpu': return pcComponents.cpus.length;
    case 'gpu': return pcComponents.gpus.length;
    case 'motherboard': return pcComponents.motherboards.length;
    case 'ram': return pcComponents.rams.length;
    case 'storage': return pcComponents.storages.length;
    case 'psu': return pcComponents.psus.length;
    case 'cooler': return pcComponents.coolers.length;
    default: return pcComponents.componentsCount;
  }
};

    const formatPrice = (price: number) => {
  return price.toLocaleString('ru-RU');
};

onMounted(() => {
  pcComponents.fetchAllComponents();
});

</script>
    
<style scoped>

.header{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}
.header-logo{
    max-width: 150px;
    margin-right: 10px;
    border-radius: 15px;
}

header h2{
  font-size: 70px;
  font-weight: 600;
  background-image: url(/Tittle.jpg);
  background-size: 250px;
  background-repeat: repeat;
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  font-family: Arial, Helvetica, sans-serif;
}


.pc-builder {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.stats {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 10px;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: bold;
}

.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.filters button {
  padding: 10px 20px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  position: relative;
}

.filters button:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.filters button.active {
  background: #42b983;
  color: white;
}

.count {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 6px;
  background: rgba(0,0,0,0.1);
  border-radius: 10px;
  font-size: 12px;
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.component-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  border-left: 4px solid;
}

.component-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.component-card.cpu { border-left-color: #2196f3; }
.component-card.gpu { border-left-color: #4caf50; }
.component-card.motherboard { border-left-color: #ff9800; }
.component-card.ram { border-left-color: #9c27b0; }
.component-card.storage { border-left-color: #00bcd4; }
.component-card.psu { border-left-color: #f44336; }
.component-card.cooler { border-left-color: #795548; }

.component-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.component-header h3 {
  margin: 0;
  font-size: 18px;
}

.brand {
  padding: 2px 8px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 12px;
}

.component-specs {
  margin: 15px 0;
}

.spec {
  font-size: 14px;
  color: #666;
  margin: 5px 0;
}

.component-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.price {
  font-size: 20px;
  font-weight: bold;
  color: #42b983;
}

.remove-btn {
  padding: 6px 12px;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.remove-btn:hover {
  background: #cc0000;
}

.refresh-btn {
  display: block;
  width: 200px;
  margin: 0 auto;
  padding: 12px 24px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
}

.refresh-btn:hover {
  background: #369f6e;
}

.loading {
  text-align: center;
  padding: 60px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #42b983;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 60px;
  background: #ffebee;
  border-radius: 12px;
  color: #c62828;
}

.error button {
  margin-top: 20px;
  padding: 10px 20px;
  background: #c62828;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

</style>
