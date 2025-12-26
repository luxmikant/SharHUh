/**
 * Status to color mapping for 3D visualization
 */

export const STATUS_COLORS = {
  healthy: {
    main: '#00ff00',
    emissive: '#00ff00',
    intensity: 0.5,
    hex: 0x00ff00
  },
  warning: {
    main: '#ffaa00',
    emissive: '#ffaa00',
    intensity: 0.8,
    hex: 0xffaa00
  },
  critical: {
    main: '#ff0000',
    emissive: '#ff0000',
    intensity: 1.0,
    hex: 0xff0000
  }
}

export const getStatusColor = (status) => {
  return STATUS_COLORS[status] || STATUS_COLORS.healthy
}

export const getStatusClass = (status) => {
  return `status-${status}`
}

/**
 * Calculate color based on latency
 */
export const latencyToColor = (latencyMs) => {
  if (latencyMs < 500) return STATUS_COLORS.healthy
  if (latencyMs < 2000) return STATUS_COLORS.warning
  return STATUS_COLORS.critical
}

/**
 * Calculate color based on error rate
 */
export const errorRateToColor = (errorRate) => {
  if (errorRate < 0.05) return STATUS_COLORS.healthy
  if (errorRate < 0.15) return STATUS_COLORS.warning
  return STATUS_COLORS.critical
}

/**
 * Interpolate between two colors
 */
export const lerpColor = (color1, color2, t) => {
  const r1 = (color1 >> 16) & 0xff
  const g1 = (color1 >> 8) & 0xff
  const b1 = color1 & 0xff
  
  const r2 = (color2 >> 16) & 0xff
  const g2 = (color2 >> 8) & 0xff
  const b2 = color2 & 0xff
  
  const r = Math.round(r1 + (r2 - r1) * t)
  const g = Math.round(g1 + (g2 - g1) * t)
  const b = Math.round(b1 + (b2 - b1) * t)
  
  return (r << 16) | (g << 8) | b
}
