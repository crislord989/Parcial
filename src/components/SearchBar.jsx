import { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '20px 0' }}>
      <input
        type="text"
        placeholder="Buscar canción, artista o género..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ padding: '8px', width: '300px', marginRight: '8px' }}
      />
      <button type="submit" style={{ padding: '8px 16px' }}>Buscar</button>
    </form>
  );
}

export default SearchBar;
