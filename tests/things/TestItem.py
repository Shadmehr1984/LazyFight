import pytest
from src.things.Item import Item

class TestItem:
    def test_initial_item(self):
        item = Item('iron', 10)
        
        assert item is not None
    def test_item_name_and_count_initial(self):
        item = Item('silver', 45)
        
        assert 'silver' == item.name
        assert 45 == item.count
    def test_when_count_is_negative_or_zero_raise_err(self):
        with pytest.raises(ValueError):
            item = Item('goh', -1)
        
        with pytest.raises(ValueError):
            item = Item('goh', 0)
    
    def test_get(self):
        item = Item('coin', 12)
        
        assert item.get() == {'name': 'coin', 'count': 12}
    
    def test_eq(self):
        item = Item('chip', 66)
        
        assert item == Item('chip', 66)
        assert item == Item('chip', 55)
        assert item != Item('ship', 66)
        assert item != Item('silver', 10)
    
    def test_str(self):
        item = Item('sword', 1)
        
        assert item.__str__() == 'name:sword, count:1'

    def test_get_returns_a_new_dictionary_each_time(self):
        item = Item('potion', 3)

        first = item.get()
        second = item.get()

        assert first == {'name': 'potion', 'count': 3}
        assert second == {'name': 'potion', 'count': 3}
        assert first is not second

    def test_changing_get_result_does_not_change_item(self):
        item = Item('potion', 3)
        result = item.get()

        result['name'] = 'poison'
        result['count'] = 99

        assert item.name == 'potion'
        assert item.count == 3
