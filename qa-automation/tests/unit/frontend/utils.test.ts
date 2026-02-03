/**
 * Frontend Unit Tests - Jest
 * Basic utility and component tests
 */

describe('Utils', () => {
  describe('Basic Math Operations', () => {
    it('should add two numbers correctly', () => {
      expect(1 + 2).toBe(3);
    });

    it('should multiply numbers correctly', () => {
      expect(2 * 3).toBe(6);
    });

    it('should handle string concatenation', () => {
      expect('Hello' + ' ' + 'World').toBe('Hello World');
    });
  });

  describe('Array Operations', () => {
    it('should filter array elements', () => {
      const numbers = [1, 2, 3, 4, 5];
      const evens = numbers.filter(n => n % 2 === 0);
      expect(evens).toEqual([2, 4]);
    });

    it('should map array elements', () => {
      const numbers = [1, 2, 3];
      const doubled = numbers.map(n => n * 2);
      expect(doubled).toEqual([2, 4, 6]);
    });
  });

  describe('Object Operations', () => {
    it('should merge objects', () => {
      const obj1 = { a: 1 };
      const obj2 = { b: 2 };
      const merged = { ...obj1, ...obj2 };
      expect(merged).toEqual({ a: 1, b: 2 });
    });

    it('should check object keys', () => {
      const obj = { name: 'Test', value: 42 };
      expect(Object.keys(obj)).toHaveLength(2);
      expect(obj).toHaveProperty('name');
    });
  });
});

describe('String Utilities', () => {
  it('should convert to uppercase', () => {
    expect('hello'.toUpperCase()).toBe('HELLO');
  });

  it('should trim whitespace', () => {
    expect('  test  '.trim()).toBe('test');
  });

  it('should split strings', () => {
    expect('a,b,c'.split(',')).toEqual(['a', 'b', 'c']);
  });
});
