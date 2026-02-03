/**
 * Frontend Component Tests - Jest + React Testing Library
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Simple component for testing
const Button: React.FC<{ label: string; onClick?: () => void }> = ({ label, onClick }) => (
  <button onClick={onClick} data-testid="test-button">
    {label}
  </button>
);

const Card: React.FC<{ title: string; children?: React.ReactNode }> = ({ title, children }) => (
  <div data-testid="test-card">
    <h2>{title}</h2>
    {children && <div>{children}</div>}
  </div>
);

describe('React Components', () => {
  describe('Button Component', () => {
    it('should render button with label', () => {
      render(<Button label="Click Me" />);
      const button = screen.getByTestId('test-button');
      expect(button).toBeInTheDocument();
      expect(button).toHaveTextContent('Click Me');
    });

    it('should handle click events', () => {
      const handleClick = jest.fn();
      render(<Button label="Click Me" onClick={handleClick} />);
      const button = screen.getByTestId('test-button');
      button.click();
      expect(handleClick).toHaveBeenCalledTimes(1);
    });
  });

  describe('Card Component', () => {
    it('should render card with title', () => {
      render(<Card title="Test Card" />);
      expect(screen.getByTestId('test-card')).toBeInTheDocument();
      expect(screen.getByText('Test Card')).toBeInTheDocument();
    });

    it('should render card with children', () => {
      render(
        <Card title="Test Card">
          <p>Card content</p>
        </Card>
      );
      expect(screen.getByText('Card content')).toBeInTheDocument();
    });
  });
});
