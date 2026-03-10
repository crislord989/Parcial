import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import SearchBar from '../components/SearchBar';

describe('SearchBar', () => {
  it('renderiza el campo de busqueda', () => {
    render(<SearchBar onSearch={() => {}} />);
    expect(screen.getByPlaceholderText(/buscar/i)).toBeInTheDocument();
  });

  it('renderiza el boton de buscar', () => {
    render(<SearchBar onSearch={() => {}} />);
    expect(screen.getByRole('button', { name: /buscar/i })).toBeInTheDocument();
  });
});
