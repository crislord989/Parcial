function TrackCard({ track, onAddToCart, inCart }) {
  return (
    <div className="track-card">
      <div className="track-info">
        <span className="track-name">{track.name}</span>
        <span className="track-price">${track.price.toFixed(2)}</span>
      </div>
      <button
        className={`add-btn ${inCart ? 'added' : ''}`}
        onClick={() => onAddToCart(track)}
        disabled={inCart}
      >
        {inCart ? '✓ En carrito' : '+ Agregar'}
      </button>
    </div>
  );
}
export default TrackCard;
