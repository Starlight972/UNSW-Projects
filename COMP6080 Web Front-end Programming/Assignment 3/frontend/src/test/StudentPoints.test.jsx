import React from 'react';
import { render, screen } from '@testing-library/react';

// own component
import StudentPoints from '../components/StudentPoints';

test('renders text elements', () => {
  const name = 'Hayden';
  const points = 100;
  render(<StudentPoints name={name} points={points} />);
  const nameElement = screen.getByText(name);
  const pointsElement = screen.getByText('100 Points');
  expect(nameElement).toBeInTheDocument();
  expect(pointsElement).toBeInTheDocument();
});
