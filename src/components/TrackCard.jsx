function TrackCard({ track, onBuy }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '12px', margin: '8px', borderRadius: '8px' }}>
      <h4>{track.name}</h4>
      <p>Precio: ${track.price}</p>
      <button onClick={() => onBuy(track)} style={{ padding: '6px 12px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
        Comprar
      </button>
    </div>
  );
}

export default TrackCard;
