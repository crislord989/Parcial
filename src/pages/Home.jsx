import { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import TrackCard from '../components/TrackCard';
import { getTracks, searchTracks, getCustomers, createInvoice } from '../services/api';

function Home() {
  const [tracks, setTracks] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    getTracks().then(r => setTracks(r.data));
    getCustomers().then(r => setCustomers(r.data));
  }, []);

  const handleSearch = (q) => {
    searchTracks(q).then(r => setTracks(r.data));
  };

  const handleBuy = async (track) => {
    setMessage(''); setError('');
    if (!selectedCustomer) { setError('Selecciona un cliente primero'); return; }
    try {
      const res = await createInvoice({ customer_id: parseInt(selectedCustomer), track_id: track.id });
      setMessage(`✅ Compra exitosa! Factura #${res.data.invoice_id} — Total: $${res.data.total}`);
    } catch {
      setError('❌ Error al realizar la compra');
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>🎵 Chinook Music Store</h1>

      <div style={{ margin: '16px 0' }}>
        <label>Cliente: </label>
        <select value={selectedCustomer} onChange={e => setSelectedCustomer(e.target.value)} style={{ padding: '6px', marginLeft: '8px' }}>
          <option value="">-- Seleccionar cliente --</option>
          {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      <SearchBar onSearch={handleSearch} />

      {message && <div style={{ color: 'green', margin: '8px 0' }}>{message}</div>}
      {error   && <div style={{ color: 'red',   margin: '8px 0' }}>{error}</div>}

      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {tracks.map(t => <TrackCard key={t.id} track={t} onBuy={handleBuy} />)}
      </div>
    </div>
  );
}

export default Home;
