import { useEffect, useRef, useCallback } from 'react'
import useStore from '../store'

/**
 * WebSocket hook for real-time connection to backend
 */
const useWebSocket = (url = 'ws://localhost:8000/ws/nexus') => {
  const wsRef = useRef(null)
  const reconnectAttempts = useRef(0)
  const maxReconnectAttempts = 5
  
  const { 
    setConnected, 
    updateSystemState, 
    addAlert 
  } = useStore()
  
  const connect = useCallback(() => {
    try {
      console.log('🔌 Connecting to NEXUS WebSocket...')
      wsRef.current = new WebSocket(url)
      
      wsRef.current.onopen = () => {
        console.log('✅ WebSocket connected')
        reconnectAttempts.current = 0
      }
      
      wsRef.current.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          
          switch (message.type) {
            case 'connection_ack':
              console.log(`🤝 Connected as client: ${message.client_id}`)
              setConnected(true, message.client_id)
              break
              
            case 'state_update':
              updateSystemState(message)
              break
              
            case 'alert':
              console.log('🚨 Alert received:', message)
              addAlert(message)
              break
              
            case 'remediation_result':
              console.log('🔧 Remediation result:', message)
              addAlert({
                severity: message.success ? 'info' : 'error',
                message: message.message,
                service_id: message.service_id
              })
              break
              
            default:
              console.log('📨 Unknown message type:', message.type)
          }
        } catch (e) {
          // Handle ping/pong text messages
          if (event.data === 'ping') {
            wsRef.current?.send('pong')
          }
        }
      }
      
      wsRef.current.onclose = (event) => {
        console.log('🔌 WebSocket disconnected:', event.code)
        setConnected(false, null)
        
        // Attempt reconnection
        if (reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current++
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000)
          console.log(`🔄 Reconnecting in ${delay}ms (attempt ${reconnectAttempts.current})`)
          setTimeout(connect, delay)
        } else {
          console.error('❌ Max reconnection attempts reached')
        }
      }
      
      wsRef.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }
      
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
    }
  }, [url, setConnected, updateSystemState, addAlert])
  
  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [])
  
  const send = useCallback((data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }, [])
  
  useEffect(() => {
    connect()
    
    return () => {
      disconnect()
    }
  }, [connect, disconnect])
  
  return { send, disconnect, reconnect: connect }
}

export default useWebSocket
