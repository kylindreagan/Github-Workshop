from src.general import is_div_8, get_count, get_degrees, might_be_prime
import pytest

class TestMathFunctions:
    class TestIsDiv8:
        
        def test_divisible_by_8(self):
            assert is_div_8(8) == True
            assert is_div_8(16) == True
            assert is_div_8(0) == True 
            assert is_div_8(24) == True
            assert is_div_8(-16) == True 
            
        def test_not_divisible_by_8(self):
            assert is_div_8(1) == False
            assert is_div_8(7) == False
            assert is_div_8(9) == False
            assert is_div_8(15) == False
            assert is_div_8(-7) == False
            
        def test_large_numbers(self):
            assert is_div_8(1000) == True
            assert is_div_8(1001) == False
            
    # Tests for get_count
    class TestGetCount:
        
        def test_positive_numbers(self):
            assert get_count(0) == 0
            assert get_count(1) == 1
            assert get_count(5) == 5
            assert get_count(10) == 10
            
        def test_negative_numbers(self):
            assert get_count(-1) == 1
            assert get_count(-5) == 5
            assert get_count(-10) == 10
            
        def test_edge_cases(self):
            assert get_count(0) == 0
            
    # Tests for get_degrees
    class TestGetDegrees:
        
        def test_valid_polygons(self):
            assert get_degrees(3) == 180  
            assert get_degrees(4) == 360  
            assert get_degrees(5) == 540  
            assert get_degrees(6) == 720  
            assert get_degrees(8) == 1080 
            
        def test_invalid_shapes(self):
            with pytest.raises(ValueError, match="Invalid shape"):
                get_degrees(2)
            
            with pytest.raises(ValueError, match="Invalid shape"):
                get_degrees(1)
                
            with pytest.raises(ValueError, match="Invalid shape"):
                get_degrees(0)
                
            with pytest.raises(ValueError, match="Invalid shape"):
                get_degrees(-1)
                
            with pytest.raises(ValueError, match="Invalid shape"):
                get_degrees(-5)
                
        def test_large_number_of_sides(self):
            assert get_degrees(100) == (100-2)*180
            

    class TestMightBePrime:
        
        def test_always_returns_true(self):

            assert might_be_prime(2) == True
            assert might_be_prime(3) == True
            assert might_be_prime(5) == True
            assert might_be_prime(7) == True
            assert might_be_prime(11) == True
            

            assert might_be_prime(1) == True
            assert might_be_prime(4) == True
            assert might_be_prime(6) == True
            assert might_be_prime(8) == True
            assert might_be_prime(9) == True
            assert might_be_prime(10) == True
            

            assert might_be_prime(0) == True
            assert might_be_prime(-1) == True
            assert might_be_prime(-5) == True


class TestParameterized:
    @pytest.mark.parametrize("number,expected", [
        (0, True),
        (8, True),
        (16, True),
        (24, True),
        (32, True),
        (40, True),
        (1, False),
        (2, False),
        (7, False),
        (9, False),
        (15, False),
    ])
    def test_is_div_8_param(self, number, expected):
        assert is_div_8(number) == expected
        
    @pytest.mark.parametrize("input_value,expected", [
        (0, 0),
        (1, 1),
        (5, 5),
        (10, 10),
        (-1, 1),
        (-5, 5),
        (-10, 10),
    ])
    def test_get_count_param(self, input_value, expected):
        assert get_count(input_value) == expected
        
    @pytest.mark.parametrize("sides,expected", [
        (3, 180),
        (4, 360),
        (5, 540),
        (6, 720),
        (7, 900),
        (8, 1080),
    ])
    def test_get_degrees_param(self, sides, expected):
        """Parameterized test for get_degrees with valid inputs"""
        assert get_degrees(sides) == expected
        
    @pytest.mark.parametrize("sides", [0, 1, 2, -1, -5])
    def test_get_degrees_invalid_param(self, sides):
        with pytest.raises(ValueError):
            get_degrees(sides)

class TestFunctionAnalysis:
    
    def test_get_count_inefficiency(self):
        for i in range(0, 10):
            assert get_count(i) == i
        
    def test_is_div_8_with_floats(self):
        assert is_div_8(8.0) == True
        assert is_div_8(16.0) == True

@pytest.fixture
def divisible_by_8_numbers():
    return [0, 8, 16, 24, 32, 40, -8, -16, -24]

@pytest.fixture
def not_divisible_by_8_numbers():
    return [1, 2, 3, 4, 5, 6, 7, 9, 10, -1, -2, -3]

def test_is_div_8_with_fixtures(divisible_by_8_numbers, not_divisible_by_8_numbers):
    for num in divisible_by_8_numbers:
        assert is_div_8(num) == True
        
    for num in not_divisible_by_8_numbers:
        assert is_div_8(num) == False