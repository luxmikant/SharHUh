import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import useStore from '../store'

/**
 * Heads-Up Display overlay with system info
 */
const HUD = () => {
  const { 
    connected, 
    systemIntegrity, 
    activeIncidents, 
    uptimeSeconds,
    services,
    volume,
    muted,
    setVolume,
    toggleMute,
    toggleChaosControls,
    showChaosControls
  } = useStore()
  
  // Format uptime
  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  
  // Get integrity status
  const getIntegrityStatus = () => {
    if (systemIntegrity >= 80) return 'healthy'
    if (systemIntegrity >= 50) return 'warning'
    return 'critical'
  }
  
  // Count services by status
  const statusCounts = services.reduce((acc, s) => {
    acc[s.status] = (acc[s.status] || 0) + 1
    return acc
  }, {})
  
  return (
    <div className="hud-overlay">
      {/* Top header bar */}
      <div className="absolute top-0 left-0 right-0 flex justify-between items-start p-4">
        {/* Left: Title and connection status */}
        <div className="lcars-panel p-4">
          <h1 className="text-2xl font-bold text-nexus-primary font-lcars tracking-wider">
            NEXUS PROTOCOL
          </h1>
          <div className="flex items-center gap-2 mt-2">
            <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
            <span className="text-sm text-gray-400">
              {connected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>
        </div>
        
        {/* Right: System metrics */}
        <div className="lcars-panel p-4 text-right">
          <div className="text-sm text-gray-400 mb-1">SYSTEM INTEGRITY</div>
          <div className={`text-3xl font-bold status-${getIntegrityStatus()}`}>
            {systemIntegrity.toFixed(1)}%
          </div>
          <div className="integrity-bar mt-2 w-48">
            <div 
              className={`integrity-bar-fill ${getIntegrityStatus()}`}
              style={{ width: `${systemIntegrity}%` }}
            />
          </div>
        </div>
      </div>
      
      {/* Left sidebar: Service status */}
      <div className="absolute left-4 top-1/2 -translate-y-1/2">
        <div className="lcars-panel p-4 space-y-3">
          <div className="text-sm text-gray-400 mb-2">SERVICE STATUS</div>
          
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-green-500" />
            <span className="text-green-500">{statusCounts.healthy || 0} Healthy</span>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-yellow-500" />
            <span className="text-yellow-500">{statusCounts.warning || 0} Warning</span>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-red-500" />
            <span className="text-red-500">{statusCounts.critical || 0} Critical</span>
          </div>
        </div>
      </div>
      
      {/* Bottom bar: Controls and info */}
      <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end">
        {/* Left: Uptime and incidents */}
        <div className="lcars-panel p-4">
          <div className="flex gap-8">
            <div>
              <div className="text-xs text-gray-400">UPTIME</div>
              <div className="text-xl font-mono text-nexus-primary">
                {formatUptime(uptimeSeconds)}
              </div>
            </div>
            <div>
              <div className="text-xs text-gray-400">INCIDENTS</div>
              <div className={`text-xl font-mono ${activeIncidents > 0 ? 'text-red-500' : 'text-green-500'}`}>
                {activeIncidents}
              </div>
            </div>
          </div>
        </div>
        
        {/* Right: Audio controls */}
        <div className="lcars-panel p-4 flex items-center gap-4">
          {/* Volume slider */}
          <div className="flex items-center gap-2">
            <button
              onClick={toggleMute}
              className="text-nexus-primary hover:text-white transition-colors"
            >
              {muted ? '🔇' : '🔊'}
            </button>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={volume}
              onChange={(e) => setVolume(parseFloat(e.target.value))}
              className="w-24 accent-nexus-primary"
            />
          </div>
          
          {/* Chaos controls toggle */}
          <button
            onClick={toggleChaosControls}
            className={`lcars-button ${showChaosControls ? 'bg-nexus-secondary' : ''}`}
          >
            ⚡ CHAOS
          </button>
        </div>
      </div>
      
      {/* Chaos controls panel */}
      <AnimatePresence>
        {showChaosControls && (
          <motion.div
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            className="absolute right-4 top-1/2 -translate-y-1/2"
          >
            <ChaosControls />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

/**
 * Chaos mode control buttons
 */
const ChaosControls = () => {
  const triggerChaos = async (mode) => {
    try {
      const response = await fetch(`/api/chaos/mode/${mode}`, {
        method: 'POST'
      })
      const data = await response.json()
      console.log(`Chaos mode set to: ${mode}`, data)
    } catch (error) {
      console.error('Failed to set chaos mode:', error)
    }
  }
  
  return (
    <div className="lcars-panel p-4 space-y-3">
      <div className="text-sm text-gray-400 mb-2">CHAOS CONTROLS</div>
      
      <button
        onClick={() => triggerChaos('steady_state')}
        className="lcars-button w-full"
      >
        🟢 STEADY STATE
      </button>
      
      <button
        onClick={() => triggerChaos('latency_spike')}
        className="lcars-button warning w-full"
      >
        🟡 LATENCY SPIKE
      </button>
      
      <button
        onClick={() => triggerChaos('cascading_failure')}
        className="lcars-button danger w-full"
      >
        🔴 CASCADE FAILURE
      </button>
      
      <button
        onClick={() => triggerChaos('recovery')}
        className="lcars-button w-full"
      >
        🔧 RECOVERY
      </button>
    </div>
  )
}

export default HUD
