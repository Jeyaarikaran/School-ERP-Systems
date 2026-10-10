import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useBulkImport } from './useBulkImport';

// Mock the API client
vi.mock('@/lib/api-client', () => ({
  apiClient: {
    GET: vi.fn(),
    POST: vi.fn(),
  }
}));

describe('useBulkImport', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with idle state', () => {
    const { result } = renderHook(() => useBulkImport());
    expect(result.current.state).toBe('idle');
    expect(result.current.errors).toEqual([]);
  });

  it('should transition to uploading when uploadFile is called', async () => {
    // Mock native fetch since uploadFile uses it directly for FormData
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, data: { job_id: '123' } })
    });

    const { result } = renderHook(() => useBulkImport());
    const file = new File(['dummy content'], 'test.csv', { type: 'text/csv' });
    
    await act(async () => {
      await result.current.uploadFile(file);
    });

    // state goes from uploading -> validating immediately after successful fetch
    expect(result.current.state).toBe('validating');
  });

  it('should handle fetch failure properly', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useBulkImport());
    const file = new File(['dummy content'], 'test.csv', { type: 'text/csv' });
    
    await act(async () => {
      await result.current.uploadFile(file);
    });

    expect(result.current.state).toBe('failed');
  });
});
