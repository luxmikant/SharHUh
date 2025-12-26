import React, { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Particle stream visualization - data flowing between services
 */
const ParticleStream = ({ 
  startPosition = [0, 0, 0], 
  endPosition = [0, 0, 5],
  particleCount = 50,
  speed = 1,
  color = '#00ffff',
  active = true
}) => {
  const pointsRef = useRef()
  
  // Generate particle positions along the path
  const { positions, velocities } = useMemo(() => {
    const positions = new Float32Array(particleCount * 3)
    const velocities = new Float32Array(particleCount)
    
    for (let i = 0; i < particleCount; i++) {
      // Random position along the path
      const t = Math.random()
      positions[i * 3] = startPosition[0] + (endPosition[0] - startPosition[0]) * t
      positions[i * 3 + 1] = startPosition[1] + (endPosition[1] - startPosition[1]) * t + Math.random() * 0.5
      positions[i * 3 + 2] = startPosition[2] + (endPosition[2] - startPosition[2]) * t
      
      // Random velocity
      velocities[i] = 0.5 + Math.random() * 0.5
    }
    
    return { positions, velocities }
  }, [startPosition, endPosition, particleCount])
  
  useFrame((state, delta) => {
    if (!pointsRef.current || !active) return
    
    const positionArray = pointsRef.current.geometry.attributes.position.array
    
    for (let i = 0; i < particleCount; i++) {
      // Move particles along the path
      const idx = i * 3
      
      // Calculate direction
      const dx = endPosition[0] - startPosition[0]
      const dy = endPosition[1] - startPosition[1]
      const dz = endPosition[2] - startPosition[2]
      const length = Math.sqrt(dx * dx + dy * dy + dz * dz)
      
      // Move particle
      positionArray[idx] += (dx / length) * delta * speed * velocities[i]
      positionArray[idx + 1] += (dy / length) * delta * speed * velocities[i]
      positionArray[idx + 2] += (dz / length) * delta * speed * velocities[i]
      
      // Reset if past end
      const progress = (
        (positionArray[idx] - startPosition[0]) / dx +
        (positionArray[idx + 2] - startPosition[2]) / dz
      ) / 2
      
      if (progress > 1 || progress < 0) {
        positionArray[idx] = startPosition[0] + Math.random() * 0.1
        positionArray[idx + 1] = startPosition[1] + Math.random() * 0.5
        positionArray[idx + 2] = startPosition[2] + Math.random() * 0.1
      }
    }
    
    pointsRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={0.1}
        transparent
        opacity={0.8}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}

export default ParticleStream
