import pytest
import time
from unittest.mock import patch
from src.general.PRNG import PRNG

class TestPRNGInitialization:
    
    def test_init_with_seed(self):
        seed = 12345
        prng = PRNG(seed=seed)
        assert prng.state == seed
        assert prng.a == 1103515245
        assert prng.c == 12345
        assert prng.m == 2**32
        
    @patch('time.time')
    def test_init_without_seed(self, mock_time):
        mock_time.return_value = 1234567890.123
        expected_seed = int(1234567890.123 * 1000)
        prng = PRNG()
        assert prng.state == expected_seed
        
    def test_init_with_zero_seed(self):
        prng = PRNG(seed=0)
        assert prng.state == 0
        
    def test_init_with_negative_seed(self):
        prng = PRNG(seed=-100)
        assert prng.state == -100

class TestPRNGNextInt:
    
    def test_next_int_with_fixed_seed(self):
        prng = PRNG(seed=42)
        result1 = prng.next_int(1, 10)
        prng2 = PRNG(seed=42)
        result2 = prng2.next_int(1, 10)
        assert result1 == result2
        
    def test_next_int_range_single_value(self):
        prng = PRNG(seed=100)
        result = prng.next_int(5, 5)
        assert result == 5
        
    def test_next_int_small_range(self):
        prng = PRNG(seed=500)
        results = [prng.next_int(0, 1) for _ in range(100)]
        assert all(0 <= x <= 1 for x in results)
        assert any(x == 0 for x in results)
        assert any(x == 1 for x in results)
        
    def test_next_int_large_range(self):
        prng = PRNG(seed=1000)
        low = -100
        high = 100
        results = [prng.next_int(low, high) for _ in range(1000)]
        assert all(low <= x <= high for x in results)
        assert min(results) >= low
        assert max(results) <= high
        
    def test_next_int_negative_range(self):
        prng = PRNG(seed=200)
        results = [prng.next_int(-10, -5) for _ in range(50)]
        assert all(-10 <= x <= -5 for x in results)
        
    def test_next_int_sequence_deterministic(self):
        prng = PRNG(seed=777)
        sequence1 = [prng.next_int(1, 100) for _ in range(10)]
        prng2 = PRNG(seed=777)
        sequence2 = [prng2.next_int(1, 100) for _ in range(10)]
        assert sequence1 == sequence2
        
    def test_next_int_state_updates(self):
        prng = PRNG(seed=50)
        initial_state = prng.state
        prng.next_int(1, 10)
        assert prng.state != initial_state

class TestPRNGNextFloat:
    
    def test_next_float_with_fixed_seed(self):
        prng = PRNG(seed=42)
        result1 = prng.next_float()
        prng2 = PRNG(seed=42)
        result2 = prng2.next_float()
        assert result1 == result2
        
    def test_next_float_range(self):
        prng = PRNG(seed=300)
        results = [prng.next_float() for _ in range(1000)]
        assert all(0.0 <= x < 1.0 for x in results)
        assert min(results) >= 0.0
        assert max(results) < 1.0
        
    def test_next_float_distribution(self):
        prng = PRNG(seed=400)
        results = [prng.next_float() for _ in range(10000)]
        mean_val = sum(results) / len(results)
        assert 0.49 < mean_val < 0.51
        
    def test_next_float_sequence(self):
        prng = PRNG(seed=888)
        sequence1 = [prng.next_float() for _ in range(5)]
        prng2 = PRNG(seed=888)
        sequence2 = [prng2.next_float() for _ in range(5)]
        assert sequence1 == sequence2
        
    def test_next_float_state_updates(self):
        prng = PRNG(seed=75)
        initial_state = prng.state
        prng.next_float()
        assert prng.state != initial_state
        
    def test_next_float_uses_updated_state(self):
        prng = PRNG(seed=100)
        float1 = prng.next_float()
        int1 = prng.next_int(1, 10)
        prng2 = PRNG(seed=100)
        float2 = prng2.next_float()
        int2 = prng2.next_int(1, 10)
        assert float1 == float2
        assert int1 == int2

class TestPRNGCombined:
    
    def test_mixed_operations(self):
        prng = PRNG(seed=999)
        results = []
        results.append(prng.next_int(1, 10))
        results.append(prng.next_float())
        results.append(prng.next_int(100, 200))
        results.append(prng.next_float())
        prng2 = PRNG(seed=999)
        results2 = []
        results2.append(prng2.next_int(1, 10))
        results2.append(prng2.next_float())
        results2.append(prng2.next_int(100, 200))
        results2.append(prng2.next_float())
        assert results == results2
        
    def test_large_sequence_consistency(self):
        prng = PRNG(seed=123456789)
        sequence = []
        for _ in range(100):
            sequence.append(prng.next_int(0, 1000))
            sequence.append(prng.next_float())
        prng2 = PRNG(seed=123456789)
        sequence2 = []
        for _ in range(100):
            sequence2.append(prng2.next_int(0, 1000))
            sequence2.append(prng2.next_float())
        assert sequence == sequence2
        
    def test_state_progression(self):
        prng = PRNG(seed=100)
        states = [prng.state]
        for _ in range(10):
            prng.next_int(1, 10)
            states.append(prng.state)
        for i in range(1, len(states)):
            assert states[i] != states[i-1]

class TestPRNGEdgeCases:
    
    def test_seed_max_int(self):
        prng = PRNG(seed=2**63 - 1)
        result = prng.next_int(0, 10)
        assert 0 <= result <= 10
        
    def test_seed_min_int(self):
        prng = PRNG(seed=-(2**63))
        result = prng.next_int(0, 10)
        assert 0 <= result <= 10
        
    def test_next_int_max_range(self):
        prng = PRNG(seed=100)
        low = -10**6
        high = 10**6
        result = prng.next_int(low, high)
        assert low <= result <= high
        
    def test_multiple_instances_independent(self):
        prng1 = PRNG(seed=100)
        prng2 = PRNG(seed=200)
        results1 = [prng1.next_int(1, 100) for _ in range(10)]
        results2 = [prng2.next_int(1, 100) for _ in range(10)]
        assert results1 != results2

@pytest.mark.parametrize("seed", [0, 1, 100, -100, 2**31 - 1])
def test_next_int_parametrized(seed):
    prng = PRNG(seed=seed)
    results = [prng.next_int(1, 10) for _ in range(20)]
    assert all(1 <= x <= 10 for x in results)

@pytest.mark.parametrize("seed", [0, 50, 100, 1000])
def test_next_float_parametrized(seed):
    prng = PRNG(seed=seed)
    results = [prng.next_float() for _ in range(20)]
    assert all(0.0 <= x < 1.0 for x in results)

def test_next_int_overflow_protection():
    prng = PRNG(seed=2**32 - 1)
    result = prng.next_int(0, 100)
    assert 0 <= result <= 100
    assert prng.state < prng.m

def test_negative_to_positive_state():
    prng = PRNG(seed=-1)
    result = prng.next_int(0, 10)
    assert 0 <= result <= 10
    assert prng.state >= 0