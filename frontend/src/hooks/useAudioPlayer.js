import { useRef, useCallback, useEffect } from 'react'
import useStore from '../store'

/**
 * Audio player hook for voice alerts
 */
const useAudioPlayer = () => {
  const audioRef = useRef(null)
  const { volume, muted } = useStore()
  
  // Initialize audio element
  useEffect(() => {
    if (!audioRef.current) {
      audioRef.current = new Audio()
      audioRef.current.volume = volume
    }
    
    return () => {
      if (audioRef.current) {
        audioRef.current.pause()
        audioRef.current = null
      }
    }
  }, [])
  
  // Update volume when it changes
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = muted ? 0 : volume
    }
  }, [volume, muted])
  
  const play = useCallback((url) => {
    if (!audioRef.current || muted) return
    
    // Stop current audio
    audioRef.current.pause()
    audioRef.current.currentTime = 0
    
    // Play new audio
    audioRef.current.src = url
    audioRef.current.play().catch(err => {
      console.warn('Audio playback failed:', err)
    })
  }, [muted])
  
  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.currentTime = 0
    }
  }, [])
  
  const playAlert = useCallback((severity) => {
    const alertSounds = {
      p1: '/audio/alert_cascading.mp3',
      p2: '/audio/alert_latency.mp3',
      p3: '/audio/alert_latency.mp3',
      info: '/audio/system_healthy.mp3'
    }
    
    const url = alertSounds[severity] || alertSounds.p2
    play(url)
  }, [play])
  
  return { play, stop, playAlert }
}

export default useAudioPlayer
