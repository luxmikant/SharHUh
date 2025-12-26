import React, { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Box, Text, Html } from '@react-three/drei'
import * as THREE from 'three'
import { getStatusColor } from '../utils/colorMapping'
import useStore from '../store'

/**
 * Individual service monolith component
 */
const Monolith = ({ 
  serviceId, 
  position = [0, 0, 0], 
  status = 'healthy',
  latency = 500,
  errorRate = 0.02,
  trafficVolume = 75
}) => {
  const meshRef = useRef()
  const glowRef = useRef()
  const selectService = useStore(state => state.selectService)
  
  const statusColor = useMemo(() => getStatusColor(status), [status])
  
  // Animation state
  const pulseSpeed = status === 'critical' ? 8 : status === 'warning' ? 4 : 2
  
  useFrame((state) => {
    if (!meshRef.current) return
    
    const time = state.clock.getElapsedTime()
    
    // Pulse animation
    const pulse = Math.sin(time * pulseSpeed) * 0.1 + 1
    meshRef.current.scale.set(1, pulse, 1)
    
    // Emissive intensity pulse
    if (meshRef.current.material) {
      meshRef.current.material.emissiveIntensity = 
        statusColor.intensity * (0.5 + Math.sin(time * pulseSpeed) * 0.5)
    }
    
    // Glitch effect for critical status
    if (status === 'critical') {
      const glitch = Math.random() > 0.95
      if (glitch) {
        meshRef.current.position.x = position[0] + (Math.random() - 0.5) * 0.1
        meshRef.current.position.z = position[2] + (Math.random() - 0.5) * 0.1
      } else {
        meshRef.current.position.x = position[0]
        meshRef.current.position.z = position[2]
      }
    }
    
    // Glow ring rotation
    if (glowRef.current) {
      glowRef.current.rotation.y += 0.01
    }
  })
  
  const handleClick = (e) => {
    e.stopPropagation()
    selectService(serviceId)
  }
  
  return (
    <group position={position}>
      {/* Main monolith */}
      <Box
        ref={meshRef}
        args={[1, 3, 1]}
        position={[0, 1.5, 0]}
        onClick={handleClick}
        onPointerOver={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'pointer'
        }}
        onPointerOut={() => {
          document.body.style.cursor = 'default'
        }}
      >
        <meshStandardMaterial
          color={statusColor.main}
          emissive={statusColor.emissive}
          emissiveIntensity={statusColor.intensity}
          metalness={0.8}
          roughness={0.2}
          transparent
          opacity={0.9}
        />
      </Box>
      
      {/* Base glow ring */}
      <mesh ref={glowRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
        <ringGeometry args={[0.8, 1.2, 32]} />
        <meshBasicMaterial 
          color={statusColor.main} 
          transparent 
          opacity={0.5}
          side={THREE.DoubleSide}
        />
      </mesh>
      
      {/* Service label */}
      <Text
        position={[0, 3.5, 0]}
        fontSize={0.3}
        color="#00ffff"
        anchorX="center"
        anchorY="middle"
        font="/fonts/JetBrainsMono-Bold.woff"
      >
        {serviceId.toUpperCase()}
      </Text>
      
      {/* Metrics display */}
      <Html
        position={[0, 4.2, 0]}
        center
        distanceFactor={10}
        style={{ pointerEvents: 'none' }}
      >
        <div className="text-xs text-center opacity-80 whitespace-nowrap">
          <div className={`font-mono ${status === 'critical' ? 'text-red-500' : status === 'warning' ? 'text-yellow-500' : 'text-green-500'}`}>
            {latency}ms | {(errorRate * 100).toFixed(1)}%
          </div>
        </div>
      </Html>
      
      {/* Point light for glow effect */}
      <pointLight
        position={[0, 1.5, 0]}
        color={statusColor.main}
        intensity={status === 'critical' ? 2 : status === 'warning' ? 1 : 0.5}
        distance={5}
      />
    </group>
  )
}

export default Monolith
