import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { PCComponentType, CPU, GPU, Motherboard, RAM, Storage, PSU, Cooler } from '@/types/pc-components'

export const usePCComponentsStore = defineStore('pcComponents', () => {
  // State
  const components = ref<PCComponentType[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters - фильтрация по типам
  const cpus = computed(() => 
    components.value.filter(c => c.type === 'cpu') as CPU[]
  )
  
  const gpus = computed(() => 
    components.value.filter(c => c.type === 'gpu') as GPU[]
  )
  
  const motherboards = computed(() => 
    components.value.filter(c => c.type === 'motherboard') as Motherboard[]
  )
  
  const rams = computed(() => 
    components.value.filter(c => c.type === 'ram') as RAM[]
  )
  
  const storages = computed(() => 
    components.value.filter(c => c.type === 'storage') as Storage[]
  )
  
  const psus = computed(() => 
    components.value.filter(c => c.type === 'psu') as PSU[]
  )
  
  const coolers = computed(() => 
    components.value.filter(c => c.type === 'cooler') as Cooler[]
  )

  // Дополнительные геттеры
  const totalPrice = computed(() => 
    components.value.reduce((sum, component) => sum + component.price, 0)
  )
  
  const componentsCount = computed(() => components.value.length);
  
  const getComponentById = computed(() => (id: number) => 
    components.value.find(c => c.id === id)
  )
  
  const getComponentsByBrand = computed(() => (brand: string) => 
    components.value.filter(c => c.brand.toLowerCase() === brand.toLowerCase())
  )

  const getComponentsByPriceRange = computed(() => (min: number, max: number) => 
    components.value.filter(c => c.price >= min && c.price <= max)
  )

  // Actions - загрузка данных
  async function fetchAllComponents() {
    isLoading.value = true
    error.value = null
    
    try {
      // Имитация API запросов
      const [cpusData, gpusData, motherboardsData, ramsData, storagesData, psusData, coolersData] = await Promise.all([
        fetchCPUs(),
        fetchGPUs(),
        fetchMotherboards(),
        fetchRAMs(),
        fetchStorages(),
        fetchPSUs(),
        fetchCoolers()
      ])
      
      // Добавляем свойство type к каждой сущности
      const allComponents: PCComponentType[] = [
        ...cpusData.map(item => ({ ...item, type: 'cpu' as const })),
        ...gpusData.map(item => ({ ...item, type: 'gpu' as const })),
        ...motherboardsData.map(item => ({ ...item, type: 'motherboard' as const })),
        ...ramsData.map(item => ({ ...item, type: 'ram' as const })),
        ...storagesData.map(item => ({ ...item, type: 'storage' as const })),
        ...psusData.map(item => ({ ...item, type: 'psu' as const })),
        ...coolersData.map(item => ({ ...item, type: 'cooler' as const }))
      ]
      
      components.value = allComponents
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки комплектующих'
      console.error('Ошибка загрузки:', err)
    } finally {
      isLoading.value = false
    }
  }

  // API функции 
  async function fetchCPUs(): Promise<Omit<CPU, 'type'>[]> {
    // Имитация задержки сети
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 1,
        name: 'Intel Core i9-13900K',
        price: 58990,
        brand: 'Intel',
        cores: 24,
        threads: 32,
        frequency: 3.0,
        socket: 'LGA1700'
      },
      {
        id: 2,
        name: 'AMD Ryzen 9 7950X',
        price: 65990,
        brand: 'AMD',
        cores: 16,
        threads: 32,
        frequency: 4.5,
        socket: 'AM5'
      },
      {
        id: 3,
        name: 'Intel Core i5-13600K',
        price: 29990,
        brand: 'Intel',
        cores: 14,
        threads: 20,
        frequency: 2.6,
        socket: 'LGA1700'
      }
    ]
  }

  async function fetchGPUs(): Promise<Omit<GPU, 'type'>[]> {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 4,
        name: 'NVIDIA RTX 4090',
        price: 159990,
        brand: 'NVIDIA',
        vram: 24,
        chipset: 'AD102',
        tdp: 450
      },
      {
        id: 5,
        name: 'AMD Radeon RX 7900 XTX',
        price: 119990,
        brand: 'AMD',
        vram: 24,
        chipset: 'Navi 31',
        tdp: 355
      },
      {
        id: 6,
        name: 'NVIDIA RTX 4070 Ti',
        price: 79990,
        brand: 'NVIDIA',
        vram: 12,
        chipset: 'AD104',
        tdp: 285
      }
    ]
  }

  async function fetchMotherboards(): Promise<Omit<Motherboard, 'type'>[]> {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 7,
        name: 'ASUS ROG Maximus Z790 Hero',
        price: 49990,
        brand: 'ASUS',
        socket: 'LGA1700',
        ramSlots: 4,
        formFactor: 'ATX'
      },
      {
        id: 8,
        name: 'MSI B650 Tomahawk',
        price: 19990,
        brand: 'MSI',
        socket: 'AM5',
        ramSlots: 4,
        formFactor: 'ATX'
      }
    ]
  }

  async function fetchRAMs(): Promise<Omit<RAM, 'type'>[]> {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 9,
        name: 'Corsair Vengeance DDR5 32GB',
        price: 13990,
        brand: 'Corsair',
        capacity: 32,
        frequency: 5600,
        typeRam: 'DDR5'
      },
      {
        id: 10,
        name: 'Kingston Fury DDR4 16GB',
        price: 4990,
        brand: 'Kingston',
        capacity: 16,
        frequency: 3200,
        typeRam: 'DDR4'
      }
    ]
  }

  async function fetchStorages(): Promise<Omit<Storage, 'type'>[]> {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 11,
        name: 'Samsung 980 Pro 1TB',
        price: 10990,
        brand: 'Samsung',
        capacity: 1000,
        interface: 'NVMe',
        formFactor: 'M.2'
      },
      {
        id: 12,
        name: 'WD Blue 2TB',
        price: 7990,
        brand: 'Western Digital',
        capacity: 2000,
        interface: 'SATA',
        formFactor: '2.5"'
      }
    ]
  }

  async function fetchPSUs(): Promise<Omit<PSU, 'type'>[]> {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 13,
        name: 'Corsair RM850x',
        price: 14990,
        brand: 'Corsair',
        wattage: 850,
        efficiency: 'Gold'
      },
      {
        id: 14,
        name: 'Be Quiet! Pure Power 12M 750W',
        price: 11990,
        brand: 'Be Quiet!',
        wattage: 750,
        efficiency: 'Gold'
      }
    ]
  }

  async function fetchCoolers(): Promise<Omit<Cooler, 'type'>[]> {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 15,
        name: 'Noctua NH-D15',
        price: 8990,
        brand: 'Noctua',
        typeCooler: 'air',
        tdp: 250
      },
      {
        id: 16,
        name: 'Arctic Liquid Freezer II 360',
        price: 11990,
        brand: 'Arctic',
        typeCooler: 'liquid',
        tdp: 300
      }
    ]
  }

  // CRUD операции
  function addComponent(component: PCComponentType) {
    components.value.push(component)
  }

  function removeComponent(id: number) {
    components.value = components.value.filter(c => c.id !== id)
  }

  function updateComponent(id: number, updatedData: Partial<PCComponentType>) {
    const index = components.value.findIndex(c => c.id === id)
    if (index !== -1) {
        components.value[index] = { 
            ...components.value[index], 
            ...updatedData 
        } as PCComponentType
    }
  }

  function clearComponents() {
    components.value = []
  }

  return {
    // State
    components,
    isLoading,
    error,
    
    // Getters
    cpus,
    gpus,
    motherboards,
    rams,
    storages,
    psus,
    coolers,
    totalPrice,
    componentsCount,
    getComponentById,
    getComponentsByBrand,
    getComponentsByPriceRange,
    
    // Actions
    fetchAllComponents,
    addComponent,
    removeComponent,
    updateComponent,
    clearComponents
  }
})