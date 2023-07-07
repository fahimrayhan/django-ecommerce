from .forms import NewItem
from .models import Item
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def details(req, pk):
    item = get_object_or_404(Item, pk=pk)
    
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    return render(req, 'item/detail.html',{
        'item':item,
        'r_items':related_items,
    })
    
@login_required
def new(req):
    if req.method == "POST":
        form = NewItem(req.POST, req.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = req.user
            item.save
            
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItem()
    
    return render(req, 'item/form.html',{
        'form':form,
        "title":'New Item',
    })
