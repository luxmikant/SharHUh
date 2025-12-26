import React from 'react'
import { Canvas } from '@react-three/fiber'
import { 
  OrbitControls, 
  Environment, 
  Stars, 
  Grid,
  PerspectiveCamera
} from '@react-three/drei'
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing'
import Monolith from './Monolith'
import ParticleStream from './ParticleStream'
import useStore from '../store'

// Service positions in a circle
const SERVICE_POSITIONS = {
  'gateway': [0, 0, 5],
  'auth': [4.76, 0, 1.55],
  'payment': [2.94, 0, -4.05],
  'ai-brain': [-2.94, 0, -4.05],
  'database': [-4.76, 0, 1.55]
}

/**
 * Main 3D scene with all monoliths
 */
const Scene = () => {
  const services = useStore(state => state.services)
  
  // Create particle streams from gateway to other services
  const gatewayPos = SERVICE_POSITIONS['gateway']
  const otherServices = Object.entries(SERVICE_POSITIONS)
    .filter(([id]) => id !== 'gateway')
  
  return (
    <>
      {/* Camera */}
      <PerspectiveCamera makeDefault position={[0, 8, 12]} fov={60} />
      
      {/* Lighting */}
      <ambientLight intensity={0.2} />
      <directionalLight position={[10, 10, 5]} intensity={0.5} />
      <pointLight position={[0, 5, 0]} color="#00ffff" intensity={0.5} />
      
      {/* Environment */}
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} />
      
      {/* Ground grid */}
      <Grid
        position={[0, -0.01, 0]}
        args={[20, 20]}
        cellSize={1}
        cellThickness={0.5}
        cellColor="#1a1a2e"
        sectionSize={5}
        sectionThickness={1}
        sectionColor="#00ffff"
        fadeDistance={30}
        fadeStrength={1}
        followCamera={false}
      />
      
      {/* Service Monoliths */}
      {services.length > 0 ? (
        services.map(service => (
          <Monolith
            key={service.service_id}
            serviceId={service.service_id}
            position={SERVICE_POSITIONS[service.service_id] || [0, 0, 0]}
            status={service.status}
            latency={service.latency_ms}
            errorRate={service.error_rate}
            trafficVolume={service.traffic_volume}
          />
        ))
      ) : (
        // Default monoliths when no data
        Object.entries(SERVICE_POSITIONS).map(([id, pos]) => (
          <Monolith
            key={id}
            serviceId={id}
            position={pos}
            status="healthy"
            latency={500}
            errorRate={0.02}
            trafficVolume={75}
          />
        ))
      )}
      
      {/* Particle streams from gateway */}
      {otherServices.map(([id, pos]) => (
        <ParticleStream
          key={`stream-${id}`}
          startPosition={gatewayPos}
          endPosition={pos}
          particleCount={30}
          speed={2}
          color="#00ffff"
        />
      ))}
      
      {/* Central core */}
      <mesh position={[0, 0.5, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial
          color="#00ffff"
          emissive="#00ffff"
          emissiveIntensity={0.5}
          transparent
          opacity={0.7}
        />
      </mesh>
      
      {/* Post-processing effects */}
      <EffectComposer>
        <Bloom
          intensity={1}
          luminanceThreshold={0.2}
          luminanceSmoothing={0.9}
        />
        <Vignette
          offset={0.5}
          darkness={0.5}
        />
      </EffectComposer>
      
      {/* Controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={5}
        maxDistance={30}
        maxPolarAngle={Math.PI / 2.2}
      />
    </>
  )
}

/**
 * Main scene container with Canvas
 */
const NexusScene = () => {
  return (
    <div className="canvas-container">
      <Canvas
        gl={{ 
          antialias: true,
          alpha: false,
          powerPreference: 'high-performance'
        }}
        dpr={[1, 2]}
      >
        <color attach="background" args={['#0a0a0f']} />
        <fog attach="fog" args={['#0a0a0f', 20, 50]} />
        <Scene />
      </Canvas>
    </div>
  )
}

export default NexusScene
