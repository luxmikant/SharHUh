import React, { useEffect } from 'react'
import NexusScene from './components/NexusScene'
import HUD from './components/HUD'
import IncidentModal from './components/IncidentModal'
import AlertList from './components/AlertList'
import useWebSocket from './hooks/useWebSocket'
import useAudioPlayer from './hooks/useAudioPlayer'
import useStore from './store'

/**
 * NEXUS PROTOCOL - Main App Component
 * 3D Observability Holodeck for LLM Systems
 */
function App() {
  // Initialize WebSocket connection
  useWebSocket()
  
  // Initialize audio player
  const { playAlert } = useAudioPlayer()
  
  // Subscribe to alerts for audio playback
  const alerts = useStore(state => state.alerts)
  
  useEffect(() => {
    if (alerts.length > 0) {
      const latestAlert = alerts[alerts.length - 1]
      playAlert(latestAlert.severity)
    }
  }, [alerts.length, playAlert])
  
  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+1/2/3 for chaos modes
      if (e.ctrlKey) {
        const modes = {
          '1': 'steady_state',
          '2': 'latency_spike',
          '3': 'cascading_failure',
          '4': 'recovery'
        }
        
        if (modes[e.key]) {
          e.preventDefault()
          fetch(`/api/chaos/mode/${modes[e.key]}`, { method: 'POST' })
            .then(r => r.json())
            .then(d => console.log('Chaos mode:', d))
            .catch(console.error)
        }
      }
      
      // Escape to close modal
      if (e.key === 'Escape') {
        useStore.getState().closeModal()
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])
  
  return (
    <div className="w-full h-full relative">
      {/* 3D Scene */}
      <NexusScene />
      
      {/* HUD Overlay */}
      <HUD />
      
      {/* Alert Notifications */}
      <AlertList />
      
      {/* Service Detail Modal */}
      <IncidentModal />
      
      {/* Loading overlay for initial connection */}
      <ConnectionOverlay />
    </div>
  )
}

/**
 * Connection status overlay
 */
function ConnectionOverlay() {
  const connected = useStore(state => state.connected)
  const [showOverlay, setShowOverlay] = React.useState(true)
  
  useEffect(() => {
    if (connected) {
      // Hide overlay after brief delay
      const timer = setTimeout(() => setShowOverlay(false), 1000)
      return () => clearTimeout(timer)
    } else {
      setShowOverlay(true)
    }
  }, [connected])
  
  if (!showOverlay) return null
  
  return (
    <div className="fixed inset-0 bg-nexus-dark flex items-center justify-center z-50 transition-opacity duration-500"
         style={{ opacity: connected ? 0 : 1, pointerEvents: connected ? 'none' : 'auto' }}>
      <div className="text-center">
        <div className="spinner mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-nexus-primary font-lcars mb-2">
          NEXUS PROTOCOL
        </h2>
        <p className="text-gray-400">
          {connected ? 'Connected!' : 'Establishing connection...'}
        </p>
      </div>
    </div>
  )
}

export default App
