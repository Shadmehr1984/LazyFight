import pytest
from src.things.Inventory import Inventory
from src.things.Item import Item

@pytest.fixture()
def i():
    i: Inventory = Inventory()
        
    i.add_item(Item('gold', 10))
    i.add_item(Item('silver', 12))
    
    yield i

class TestInventory:
    def test_initial_inventory(self):
        i = Inventory()
        
        assert i is not None
    
    def test_initialed_inventory_items_len_is_zero(self):
        i = Inventory()
        
        assert len(i.items) == 0
    
    def test_add_item_increases_len(self):
        i = Inventory()
        
        i.add_item(Item('silver', 10))
        
        assert len(i.items) == 1
        
        i.add_item(Item('gold', 70))
        
        assert len(i.items) == 2
    
    def test_add_item_with_duplicate_name_not_increases_len(self):
        i = Inventory()
        
        i.add_item(Item('gold', 10))
        i.add_item(Item('gold', 12))
        
        assert len(i.items) == 1
    
    def test_add_duplicate_item_must_increase_item_count(self):
        i = Inventory()
        
        i.add_item(Item('gold', 10))
        i.add_item(Item('gold', 12))
        
        assert i.items['gold'].count == 22
    
    def test_exist_item_method(self, i):
        assert i.exist_item('gold')
        assert i.exist_item('silver')
        assert not i.exist_item('coin')
    
    def test_exist_items_method(self, i):
        assert i.exist_items(['gold', 'silver'])
        
        assert not i.exist_items(['coin', 'gold'])
    
    def test_when_item_count_is_zero_or_less_enough_item_method_raise_err(self, i):
        with pytest.raises(ValueError):
            i.enough_item('gold', 0)
        with pytest.raises(ValueError):
            i.enough_item('gold', -4)
    
    def test_when_item_not_exist_enough_item_raise_err(self, i):
        with pytest.raises(IndexError):
            i.enough_item('coin', 1)
    
    def test_enough_item_method(self, i):
        assert i.enough_item('gold', 5)
        assert i.enough_item('gold', 10)
        assert not i.enough_item('gold', 20)
        assert i.enough_item('silver', 6)
        assert i.enough_item('silver', 12)
        assert not i.enough_item('silver', 30)
    
    def test_when_item_count_is_zero_or_less_enough_items_method_raise_err(self, i):
        with pytest.raises(ValueError):
            i.enough_items({'gold': 0, 'silver': 5})
        with pytest.raises(ValueError):
            i.enough_items({'gold': 6, 'silver': -1})
    
    def test_when_item_not_exist_enough_items_raise_err(self, i):
        with pytest.raises(IndexError):
            i.enough_items({'coin': 45, 'silver': 1})
    
    def test_enough_items_method(self, i):
        assert i.enough_items({'gold': 10, 'silver': 6})
        assert not i.enough_items({'gold': 15, 'silver': 3})
        assert not i.enough_items({'gold': 1, 'silver': 30})
    
    def test_when_item_count_is_zero_or_less_raise_err(self, i):
        with pytest.raises(ValueError):
            i.pick_item('gold', 0)
        with pytest.raises(ValueError):
            i.pick_item('silver', -777)
    
    def test_when_item_not_exist_pick_item_method_raise_err(self, i):
        with pytest.raises(IndexError):
            i.pick_item('coin', 14)
    
    def test_when_item_not_enough_pick_item_method_raise_err(self, i):
        with pytest.raises(ValueError):
            i.pick_item('gold', 20)
    
    def test_pick_item_method(self, i):
        i.pick_item('gold', 8)
        
        assert i.items['gold'].count == 2
    
    def test_when_item_count_become_zero_item_deleted(self, i):
        i.pick_item('silver', 12)
        
        assert 'silver' not in i.items.keys()