import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import useStore from '../store'

/**
 * Alert notification component
 */
const AlertNotification = ({ alert, onDismiss }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'p1': return 'border-red-500 bg-red-900/30'
      case 'p2': return 'border-yellow-500 bg-yellow-900/30'
      case 'p3': return 'border-blue-500 bg-blue-900/30'
      default: return 'border-cyan-500 bg-cyan-900/30'
    }
  }
  
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'p1': return '🚨'
      case 'p2': return '⚠️'
      case 'p3': return 'ℹ️'
      default: return '📢'
    }
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, x: 300 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 300 }}
      className={`p-4 rounded-lg border-l-4 ${getSeverityColor(alert.severity)} max-w-sm`}
    >
      <div className="flex justify-between items-start">
        <div className="flex items-center gap-2">
          <span className="text-xl">{getSeverityIcon(alert.severity)}</span>
          <span className="font-bold text-white uppercase">
            {alert.service_id}
          </span>
        </div>
        <button
          onClick={() => onDismiss(alert.id)}
          className="text-gray-400 hover:text-white"
        >
          ×
        </button>
      </div>
      
      <p className="mt-2 text-sm text-gray-300">{alert.message}</p>
      
      {alert.analysis && (
        <p className="mt-2 text-xs text-cyan-400 italic">
          "{alert.analysis}"
        </p>
      )}
      
      {alert.datadog_url && (
        <a
          href={alert.datadog_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-block text-xs text-purple-400 hover:underline"
        >
          View in Datadog →
        </a>
      )}
    </motion.div>
  )
}

/**
 * Alert list container
 */
const AlertList = () => {
  const { alerts } = useStore()
  
  const dismissAlert = (id) => {
    // For now, just log - could add remove functionality
    console.log('Dismiss alert:', id)
  }
  
  return (
    <div className="absolute top-24 right-4 space-y-2 z-50">
      <AnimatePresence>
        {alerts.slice(-5).map((alert) => (
          <AlertNotification
            key={alert.id}
            alert={alert}
            onDismiss={dismissAlert}
          />
        ))}
      </AnimatePresence>
    </div>
  )
}

export default AlertList
