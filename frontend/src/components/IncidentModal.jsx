import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import useStore from '../store'

/**
 * Modal for service details and remediation
 */
const IncidentModal = () => {
  const { showModal, modalContent, closeModal, selectedService } = useStore()
  
  if (!showModal || !modalContent) return null
  
  const service = modalContent.data
  
  const handleRemediate = async (action) => {
    try {
      const response = await fetch('/api/remediate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_id: service.service_id,
          action: action
        })
      })
      
      const result = await response.json()
      console.log('Remediation result:', result)
      
      if (result.success) {
        closeModal()
      }
    } catch (error) {
      console.error('Remediation failed:', error)
    }
  }
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy': return '🟢'
      case 'warning': return '🟡'
      case 'critical': return '🔴'
      default: return '⚪'
    }
  }
  
  return (
    <AnimatePresence>
      {showModal && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="modal-backdrop"
          onClick={closeModal}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-nexus-primary font-lcars">
                {getStatusIcon(service.status)} {service.service_id.toUpperCase()}
              </h2>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-white text-2xl"
              >
                ×
              </button>
            </div>
            
            {/* Status indicator */}
            <div className={`text-center p-4 rounded-lg mb-6 ${
              service.status === 'critical' ? 'bg-red-900/30 border border-red-500' :
              service.status === 'warning' ? 'bg-yellow-900/30 border border-yellow-500' :
              'bg-green-900/30 border border-green-500'
            }`}>
              <div className={`text-3xl font-bold status-${service.status}`}>
                {service.status.toUpperCase()}
              </div>
            </div>
            
            {/* Metrics grid */}
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="text-center p-3 bg-black/30 rounded-lg">
                <div className="text-xs text-gray-400">LATENCY</div>
                <div className={`text-xl font-mono ${
                  service.latency_ms > 2000 ? 'text-red-500' :
                  service.latency_ms > 1000 ? 'text-yellow-500' :
                  'text-green-500'
                }`}>
                  {service.latency_ms}ms
                </div>
              </div>
              
              <div className="text-center p-3 bg-black/30 rounded-lg">
                <div className="text-xs text-gray-400">ERROR RATE</div>
                <div className={`text-xl font-mono ${
                  service.error_rate > 0.15 ? 'text-red-500' :
                  service.error_rate > 0.05 ? 'text-yellow-500' :
                  'text-green-500'
                }`}>
                  {(service.error_rate * 100).toFixed(1)}%
                </div>
              </div>
              
              <div className="text-center p-3 bg-black/30 rounded-lg">
                <div className="text-xs text-gray-400">TRAFFIC</div>
                <div className="text-xl font-mono text-nexus-primary">
                  {service.traffic_volume}
                </div>
              </div>
            </div>
            
            {/* Remediation actions */}
            {service.status !== 'healthy' && (
              <div className="space-y-3">
                <div className="text-sm text-gray-400 mb-2">REMEDIATION ACTIONS</div>
                
                <button
                  onClick={() => handleRemediate('reset_context')}
                  className="lcars-button w-full"
                >
                  🔄 Reset Context
                </button>
                
                <button
                  onClick={() => handleRemediate('scale_up')}
                  className="lcars-button w-full"
                >
                  📈 Scale Up
                </button>
                
                <button
                  onClick={() => handleRemediate('failover')}
                  className="lcars-button warning w-full"
                >
                  🔀 Failover
                </button>
                
                <button
                  onClick={() => handleRemediate('rate_limit')}
                  className="lcars-button danger w-full"
                >
                  ⏸️ Rate Limit
                </button>
              </div>
            )}
            
            {/* Close button */}
            <button
              onClick={closeModal}
              className="mt-6 w-full py-2 border border-gray-600 rounded text-gray-400 hover:border-nexus-primary hover:text-nexus-primary transition-colors"
            >
              Close
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default IncidentModal
