import { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');

  const handleSubmit = (e) => {
    e.preventDefault();
    const prefix = filter === 'all' ? '' : `${filter}:`;
    onSearch(prefix + query);
  };

  return (
    <form className="search-box" onSubmit={handleSubmit}>
      <select className="filter-select" value={filter} onChange={e => setFilter(e.target.value)}>
        <option value="all">Todo</option>
        <option value="artist">Artista</option>
        <option value="genre">Género</option>
        <option value="track">Canción</option>
      </select>
      <input
        type="text"
        placeholder="Buscar canción, artista o género..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button type="submit">Buscar</button>
    </form>
  );
}
export default SearchBar;
