import { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import TrackCard from '../components/TrackCard';
import { getTracks, searchTracks, getCustomers, createInvoice } from '../services/api';

function Home() {
  const [tracks, setTracks]                     = useState([]);
  const [customers, setCustomers]               = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [message, setMessage]                   = useState('');
  const [error, setError]                       = useState('');
  const [cart, setCart]                         = useState([]);
  const [cartOpen, setCartOpen]                 = useState(false);

  useEffect(() => {
    getTracks().then(r => setTracks(r.data)).catch(() => {});
    getCustomers().then(r => setCustomers(r.data)).catch(() => {});
  }, []);

  const handleSearch = (q) => {
    if (!q.trim()) getTracks().then(r => setTracks(r.data));
    else searchTracks(q).then(r => setTracks(r.data));
  };

  const addToCart    = (track) => { if (!cart.find(t => t.id === track.id)) setCart(p => [...p, track]); };
  const removeFromCart = (id) => setCart(p => p.filter(t => t.id !== id));
  const total = cart.reduce((s, t) => s + t.price, 0);

  const handleBuy = async () => {
    setMessage(''); setError('');
    if (!selectedCustomer) { setError('Selecciona un cliente primero'); return; }
    if (cart.length === 0)  { setError('El carrito está vacío'); return; }
    try {
      const res = await createInvoice({
        customer_id: parseInt(selectedCustomer),
        items: cart.map(t => ({ track_id: t.id, unit_price: t.price, quantity: 1 }))
      });
      setMessage(`✅ Compra exitosa! Factura #${res.data.invoice_id} — Total: $${res.data.total}`);
      setTracks(p => p.filter(t => !cart.find(c => c.id === t.id)));
      setCart([]);
      setCartOpen(false);
    } catch {
      setError('❌ Error al realizar la compra');
    }
    setTimeout(() => { setMessage(''); setError(''); }, 4000);
  };

  return (
    <div className="app">
      {/* NAVBAR */}
      <nav className="navbar">
        <span className="brand">🎵 Chinook Music Store</span>
        <button className="cart-btn" onClick={() => setCartOpen(o => !o)}>
          🛒 Carrito {cart.length > 0 && <span className="badge">{cart.length}</span>}
        </button>
      </nav>

      {/* MENSAJES */}
      {message && <div className="msg success">{message}</div>}
      {error   && <div className="msg error">{error}</div>}

      {/* PANEL CARRITO */}
      {cartOpen && (
        <div className="cart-panel">
          <h3>🛒 Tu carrito</h3>
          {cart.length === 0
            ? <p className="empty">Sin canciones aún.</p>
            : <>
                {cart.map(t => (
                  <div key={t.id} className="cart-item">
                    <span className="cart-track-name">{t.name}</span>
                    <span>${t.price.toFixed(2)}</span>
                    <button className="remove-btn" onClick={() => removeFromCart(t.id)}>✕</button>
                  </div>
                ))}
                <div className="cart-total">Total: <strong>${total.toFixed(2)}</strong></div>
                <button className="buy-btn full-width" onClick={handleBuy}>Comprar</button>
              </>
          }
        </div>
      )}

      {/* CONTENIDO */}
      <main className="main">

        {/* SELECTOR DE CLIENTE — visible siempre */}
        <div className="customer-bar">
          <label>👤 Cliente:</label>
          <select value={selectedCustomer} onChange={e => setSelectedCustomer(e.target.value)}>
            <option value="">-- Seleccionar cliente --</option>
            {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          {selectedCustomer && (
            <span className="customer-selected">
              ✓ {customers.find(c => c.id == selectedCustomer)?.name}
            </span>
          )}
        </div>

        <div className="top-bar">
          <SearchBar onSearch={handleSearch} />
        </div>

        <div className="tracks-grid">
          {tracks.map(t => (
            <TrackCard key={t.id} track={t} onAddToCart={addToCart}
              inCart={!!cart.find(c => c.id === t.id)} />
          ))}
        </div>
        {tracks.length === 0 &&
          <p className="empty">Busca una canción, artista o género para comenzar.</p>}
      </main>
    </div>
  );
}
export default Home;
