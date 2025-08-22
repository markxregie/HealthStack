# Stock Management Change: Stock Qty to Unit Qty Implementation

## Overview
This task implements the change from Stock Qty to Unit Qty based stock management for the pharmacy system.

## Implementation Steps

### Phase 1: Analysis and Planning ✅
- [x] Analyzed current pharmacy structure
- [x] Identified key files and components
- [x] Created comprehensive plan

### Phase 2: Model Updates
- [ ] Update Medicine model to use Unit Qty as primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### Phase 3: View Updates
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### Phase 4: Template Updates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### Phase 5: Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### Phase 6: Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Details

### 1. Model Updates
```python
# pharmacy/models.py - Update Medicine model
class Medicine(models.Model):
    # Existing fields...
    quantity = models.IntegerField(default=50)  # Unit Qty
    stock_quantity = models.IntegerField(default=1)  # Stock Qty for reset
    
    def get_available_units(self):
        """Return available units based on unit quantity"""
        return self.quantity
    
    def can_add_to_cart(self, requested_quantity):
        """Check if requested quantity is available"""
        return self.quantity >= requested_quantity
```

### 2. View Updates
```python
# pharmacy/views.py - Update add_to_cart view
def add_to_cart(request, pk):
    item = get_object_or_404(Medicine, pk=pk)
    
    # Check unit quantity instead of stock_quantity
    if item.quantity <= 0:
        messages.error(request, f"{item.name} is out of stock.")
        return redirect('pharmacy-shop')
    
    # Check if adding one more would exceed unit quantity
    if item.quantity < 1:
        messages.error(request, f"Cannot add {item.name}. Only {item.quantity} units left.")
        return redirect('pharmacy-cart')
    
    # Proceed with cart addition
    # ... rest of the logic
```

### 3. Template Updates
```html
<!-- templates/Pharmacy/cart.html - Update availability display -->
<div class="cart-item-card">
    <div class="cart-item-details">
        <h3>{{ cart.item.name }}</h3>
        <p>{{ cart.item.description }}</p>
        <p>Available: {{ cart.item.quantity }} units</p>
    </div>
    <div class="quantity-selector">
        <a href="{% url 'decrease-item' pk=cart.item.pk %}">
            <button type="button" class="quantity-btn"><i class="icon-minus"></i></button>
        </a>
        <input type="text" name="quantity" class="quantity-input" value="{{ cart.quantity }}" readonly>
        <a href="{% url 'increase-item' pk=cart.item.pk %}">
            <button type="button" class="quantity-btn"><i class="icon-plus"></i></button>
        </a>
    </div>
    <div class="cart-item-price">
        {{ cart.get_total }} Pesos
    </div>
</div>
```

### 4. Reset Logic Updates
```python
# pharmacy/utils.py - Update reset logic
def reset_unit_quantity_and_update_stock(medicine):
    """Reset Unit Qty to 50 and reduce Stock Qty by 1 when Unit Qty hits 0"""
    if medicine.quantity <= 0:
        if medicine.stock_quantity >= 1:
            medicine.quantity = 50
            medicine.stock_quantity -= 1
            medicine.save()
            return True
    return False
```

### 5. Testing Plan
- Test cart functionality with unit quantity
- Test checkout process with unit quantity
- Test reset logic with unit quantity

## Implementation Steps

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Details

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Steps

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Steps

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Steps

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Steps

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data

## Implementation Steps

### 1. Update Medicine Model
- [ ] Ensure unit quantity is the primary stock indicator
- [ ] Ensure stock_quantity is used as backup/reset mechanism

### 2. Update Cart Views
- [ ] Update add_to_cart view to use unit quantity
- [ ] Update increase_cart view to use unit quantity
- [ ] Update decrease_cart view to use unit quantity
- [ ] Update checkout process to use unit quantity

### 3. Update Templates
- [ ] Update cart.html to display unit-based availability
- [ ] Update shop.html to show unit-based stock
- [ ] Update product-single.html to show unit-based stock

### 4. Testing and Validation
- [ ] Test cart functionality with unit quantity
- [ ] Test checkout process with unit quantity
- [ ] Test reset logic with unit quantity

### 5. Documentation
- [ ] Update documentation for new stock management system
- [ ] Create migration guide for existing data
