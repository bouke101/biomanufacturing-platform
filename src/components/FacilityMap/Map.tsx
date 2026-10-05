// src/components/FacilityMap/Map.tsx
'use client'
import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet.markercluster'
import type { Facility } from '@/types/facility'

interface MapProps {
  filtered: Facility[]
  selectedId: string | null
  setSelectedId: (id: string | null) => void
}

function makeIcon(selected: boolean) {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:14px;height:14px;border-radius:50%;
      background:${selected ? '#059669' : '#10b981'};
      border:2px solid ${selected ? '#065f46' : '#fff'};
      box-shadow:0 1px 4px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  })
}

// Named FacilityMapInner to avoid shadowing the built-in `Map` type
export default function FacilityMapInner({ filtered, selectedId, setSelectedId }: MapProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const clusterRef = useRef<L.MarkerClusterGroup | null>(null)
  const markersRef = useRef<globalThis.Map<string, L.Marker>>(new globalThis.Map<string, L.Marker>())

  // Initialise map once
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return
    const map = L.map(containerRef.current, { center: [30, 10], zoom: 2 })
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map)
    const cluster = (L as any).markerClusterGroup({ maxClusterRadius: 40 })
    map.addLayer(cluster)
    mapRef.current = map
    clusterRef.current = cluster
    return () => { map.remove(); mapRef.current = null }
  }, [])

  // Rebuild markers when filtered list changes
  useEffect(() => {
    const cluster = clusterRef.current
    if (!cluster) return
    cluster.clearLayers()
    markersRef.current.clear()
    filtered.forEach((f) => {
      const marker = L.marker([f.location.lat, f.location.lng], {
        icon: makeIcon(f.id === selectedId),
      })
      marker.bindPopup(`
        <div style="min-width:160px">
          <strong style="font-size:13px">${f.name}</strong><br/>
          <span style="color:#555;font-size:12px">${f.owner}</span><br/>
          <span style="color:#888;font-size:11px">${f.location.city}, ${f.location.country}</span><br/>
          <span style="font-size:11px;color:#059669">${f.facilityType} · ${f.modalities[0]}</span>
        </div>
      `)
      marker.on('click', () => setSelectedId(f.id === selectedId ? null : f.id))
      cluster.addLayer(marker)
      markersRef.current.set(f.id, marker)
    })
  }, [filtered, selectedId, setSelectedId])

  // Update icon when selectedId changes without rebuilding
  useEffect(() => {
    markersRef.current.forEach((marker, id) => {
      marker.setIcon(makeIcon(id === selectedId))
    })
  }, [selectedId])

  return <div ref={containerRef} className="w-full h-full" />
}
