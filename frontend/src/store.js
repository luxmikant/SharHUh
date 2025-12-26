import { create } from 'zustand'

/**
 * Global state store for NEXUS PROTOCOL
 */
const useStore = create((set, get) => ({
  // Connection state
  connected: false,
  clientId: null,
  
  // System state
  systemIntegrity: 100,
  services: [],
  activeIncidents: 0,
  uptimeSeconds: 0,
  
  // UI state
  selectedService: null,
  showModal: false,
  modalContent: null,
  volume: 0.7,
  muted: false,
  showChaosControls: false,
  
  // Alerts
  alerts: [],
  
  // Actions
  setConnected: (connected, clientId = null) => set({ connected, clientId }),
  
  updateSystemState: (state) => set({
    systemIntegrity: state.system_integrity,
    services: state.services,
    activeIncidents: state.active_incidents,
    uptimeSeconds: state.uptime_seconds,
  }),
  
  selectService: (serviceId) => {
    const { services } = get()
    const service = services.find(s => s.service_id === serviceId)
    set({ 
      selectedService: service,
      showModal: true,
      modalContent: { type: 'service', data: service }
    })
  },
  
  closeModal: () => set({ 
    showModal: false, 
    modalContent: null,
    selectedService: null 
  }),
  
  addAlert: (alert) => set((state) => ({
    alerts: [...state.alerts.slice(-9), { ...alert, id: Date.now() }]
  })),
  
  clearAlerts: () => set({ alerts: [] }),
  
  setVolume: (volume) => set({ volume }),
  toggleMute: () => set((state) => ({ muted: !state.muted })),
  
  toggleChaosControls: () => set((state) => ({ 
    showChaosControls: !state.showChaosControls 
  })),
  
  // Get service by ID
  getService: (serviceId) => {
    const { services } = get()
    return services.find(s => s.service_id === serviceId)
  },
  
  // Get integrity status class
  getIntegrityStatus: () => {
    const { systemIntegrity } = get()
    if (systemIntegrity >= 80) return 'healthy'
    if (systemIntegrity >= 50) return 'warning'
    return 'critical'
  }
}))

export default useStore
