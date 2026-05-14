// Базовый тип для всех комплектующих
export interface PCComponent {
  id: number
  type: string // добавляемое свойство
  name: string
  price: number
  brand: string
}

// Процессор
export interface CPU extends PCComponent {
  type: 'cpu'
  cores: number
  threads: number
  frequency: number // GHz
  socket: string
}

// Видеокарта
export interface GPU extends PCComponent {
  type: 'gpu'
  vram: number // GB
  chipset: string
  tdp: number // Watts
}

// Материнская плата
export interface Motherboard extends PCComponent {
  type: 'motherboard'
  socket: string
  ramSlots: number
  formFactor: 'ATX' | 'Micro-ATX' | 'Mini-ITX'
}

// Оперативная память
export interface RAM extends PCComponent {
  type: 'ram'
  capacity: number // GB
  frequency: number // MHz
  typeRam: 'DDR4' | 'DDR5'
}

// Накопитель
export interface Storage extends PCComponent {
  type: 'storage'
  capacity: number // GB
  interface: 'SATA' | 'NVMe'
  formFactor: '2.5"' | 'M.2'
}

// Блок питания
export interface PSU extends PCComponent {
  type: 'psu'
  wattage: number
  efficiency: 'Bronze' | 'Silver' | 'Gold' | 'Platinum'
}

// Охлаждение
export interface Cooler extends PCComponent {
  type: 'cooler'
  typeCooler: 'air' | 'liquid'
  tdp: number
}

// Объединённый тип
export type PCComponentType = CPU | GPU | Motherboard | RAM | Storage | PSU | Cooler