import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './FactoryMap.css';

// Fix Leaflet icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function FactoryMap({ background }) {
  const { cauldrons, enchanted_market, network } = background;

  // Calculate center of map
  const centerLat = (Math.max(...cauldrons.map(c => c.latitude)) + Math.min(...cauldrons.map(c => c.latitude))) / 2;
  const centerLon = (Math.max(...cauldrons.map(c => c.longitude)) + Math.min(...cauldrons.map(c => c.longitude))) / 2;

  // Create custom icons
  const cauldronIcon = L.divIcon({
    className: 'custom-icon',
    html: '<div style="font-size: 24px;">🧪</div>',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
  });

  const marketIcon = L.divIcon({
    className: 'custom-icon',
    html: '<div style="font-size: 30px;">🏰</div>',
    iconSize: [40, 40],
    iconAnchor: [20, 20]
  });

  // Prepare edges for visualization
  const edges = network.edges || [];
  
  // Create a map of node positions
  const nodePositions = {};
  cauldrons.forEach(c => {
    nodePositions[c.id] = [c.latitude, c.longitude];
  });
  nodePositions[enchanted_market.id] = [enchanted_market.latitude, enchanted_market.longitude];

  return (
    <div className="map-container">
      <div className="map-header">
        <h2>🗺️ Potion Factory Network</h2>
        <div className="map-legend">
          <div className="legend-item">
            <span className="legend-icon">🧪</span>
            <span>Cauldron</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon">🏰</span>
            <span>Enchanted Market</span>
          </div>
          <div className="legend-item">
            <div className="legend-line" style={{background: '#8b5cf6'}}></div>
            <span>Travel Route</span>
          </div>
        </div>
      </div>

      <MapContainer
        center={[centerLat, centerLon]}
        zoom={14}
        style={{ height: '600px', width: '100%', borderRadius: '15px', background: '#1e1b4b' }}
        zoomControl={true}
        attributionControl={false}
      >
        {/* NO TILE LAYER - Just blank purple background! */}
        
        {/* Custom background using a rectangle */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%)',
          zIndex: -1
        }}></div>

        {/* Draw edges as polylines */}
        {edges.map((edge, index) => {
          const fromPos = nodePositions[edge.from];
          const toPos = nodePositions[edge.to];
          
          if (fromPos && toPos) {
            return (
              <Polyline
                key={index}
                positions={[fromPos, toPos]}
                color="#8b5cf6"
                weight={3}
                opacity={0.7}
              />
            );
          }
          return null;
        })}

        {/* Cauldron markers */}
        {cauldrons.map((cauldron) => (
          <React.Fragment key={cauldron.id}>
            <Circle
              center={[cauldron.latitude, cauldron.longitude]}
              radius={50}
              fillColor="#8b5cf6"
              fillOpacity={0.3}
              color="#8b5cf6"
              weight={2}
            />
            <Marker
              position={[cauldron.latitude, cauldron.longitude]}
              icon={cauldronIcon}
            >
              <Popup>
                <div className="marker-popup">
                  <h3>{cauldron.name}</h3>
                  <p><strong>ID:</strong> {cauldron.id}</p>
                  <p><strong>Max Volume:</strong> {cauldron.max_volume} units</p>
                  <p><strong>Location:</strong> {cauldron.latitude.toFixed(4)}, {cauldron.longitude.toFixed(4)}</p>
                </div>
              </Popup>
            </Marker>
          </React.Fragment>
        ))}

        {/* Market marker */}
        <Circle
          center={[enchanted_market.latitude, enchanted_market.longitude]}
          radius={100}
          fillColor="#ec4899"
          fillOpacity={0.3}
          color="#ec4899"
          weight={2}
        />
        <Marker
          position={[enchanted_market.latitude, enchanted_market.longitude]}
          icon={marketIcon}
        >
          <Popup>
            <div className="marker-popup">
              <h3>{enchanted_market.name}</h3>
              <p>{enchanted_market.description}</p>
              <p><strong>Location:</strong> {enchanted_market.latitude.toFixed(4)}, {enchanted_market.longitude.toFixed(4)}</p>
            </div>
          </Popup>
        </Marker>
      </MapContainer>

      <div className="map-stats">
        <div className="stat-box">
          <div className="stat-number">{cauldrons.length}</div>
          <div className="stat-label">Cauldrons</div>
        </div>
        <div className="stat-box">
          <div className="stat-number">{edges.length}</div>
          <div className="stat-label">Travel Routes</div>
        </div>
        <div className="stat-box">
          <div className="stat-number">{Math.round(edges.reduce((sum, e) => sum + e.travel_time_minutes, 0) / edges.length)}</div>
          <div className="stat-label">Avg Travel (min)</div>
        </div>
      </div>
    </div>
  );
}

export default FactoryMap;
