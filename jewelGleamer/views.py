from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Review, Images, Product, Blogs
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from actions.models import Action
import openai
import random
import logging

openai.api_key = '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'


# Navigation to the home page when the user did not login to the page
def home(request):
    return render(request, "jewelGleamer/jewelry/index.html")


# Navigation to the home page when the user is logged in
def logged_user_home(request):
    image_list = Images.objects.all()
    actions = Action.objects.all().order_by('-created')
    return render(request, "jewelGleamer/jewelry/alternate.html",
                  {"images": image_list, "actions": actions})


# List of items in the item page
def jewelry_items_list(request):
    product_list = Product.objects.all().order_by('id')
    return render(request, "jewelGleamer/jewelry/category.html",
                  {"rings": product_list})


# Every item detail page
def jewelry_item_detail(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    review_list = list(Review.objects.filter(item=item_id).order_by('-date_posted'))
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        content = request.POST.get('content', '')
        title = request.POST.get('title', '')
        review = Review.objects.create(author=user, title=title, content=content, item=item)
        review_title = review.title
        review_list.append(review)
        # log the action
        action = Action(
            user=user,
            verb="created a review " + review_title + " for the product ",
            target=item
        )
        action.save()

    review_list = Review.objects.filter(item=item_id).order_by('-date_posted')
    return render(request, "jewelGleamer/jewelry/item.html",
                  {"reviews": review_list, "item": item})


def edit_review(request, review_id, item_id):
    review = get_object_or_404(Review, id=review_id)
    review_title = review.title
    user = User.objects.get(username=request.session.get('username'))
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            # log the action
            action = Action(
                user=user,
                verb="edited a review with title " + review.title + " for the product",
                target=review
            )
            action.save()
            return redirect('jewelGleamer:item_detail', item_id=review.item.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "jewelGleamer/jewelry/edit_review.html", {"form": form, "review": review})


def delete_review(request, review_id, item_id):
    user = User.objects.get(username=request.session.get('username'))
    review = get_object_or_404(Review, id=review_id)
    review_title = review.title
    if request.session.get('username') == review.author.username or request.session.get('role') == 'Admin':
        # log the action
        action = Action(
            user=user,
            verb="deleted a review " + review_title,
            target=review
        )
        action.save()
        review.delete()
    return JsonResponse({'success': True, 'deleted_review_id': review_id})


# Adding an item to the category page of a product
def add_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('item_price')
        item_url = request.FILES['item_url'] if 'item_url' in request.FILES else None
        item_details = request.POST.get('item_details')
        item_description = request.POST.get('item_description')
        item_materials = request.POST.get('item_materials')
        user = User.objects.get(username=request.session.get('username'))
        new_product = Product(
            name=item_name,
            price=item_price,
            author=request.session.get('username'),
            details=item_details,
            description=item_description,
            materials=item_materials
        )
        product_name = new_product.name
        if item_url:
            new_product.url = item_url
        new_product.save()
        # log the action
        action = Action(
            user=user,
            verb="created a new product "+product_name+" : Link - ",
            target=new_product
        )
        action.save()
        messages.add_message(request, messages.SUCCESS, "You have successfully added product: %s" % new_product.name)
        return redirect('jewelGleamer:item_detail', item_id=new_product.id)
    product_list = Product.objects.all()
    return render(request, 'jewelGleamer/jewelry/category.html', {'rings': product_list})


# Deleting an item from the category page of a product
def delete_ring(request, ring_id):
    try:
        user = User.objects.get(username=request.session.get('username'))
        item_to_delete = Product.objects.get(id=ring_id)
        # log the action
        action = Action(
            user=user,
            verb="deleted the product : " + item_to_delete.name,
            target=item_to_delete
        )
        action.save()
        item_to_delete.delete()
        messages.add_message(request, messages.WARNING,
                             "You have successfully deleted product: %s" % item_to_delete.name)
    except Product.DoesNotExist:
        pass
    return redirect('jewelGleamer:items_list')


# Blog page view of the page where user can find other users blog
def blog(request):
    blogs_list = Blogs.objects.all()
    return render(request, "jewelGleamer/jewelry/blog.html", {"blogs": blogs_list})


# Searching the search bar on the header to navigate to the respective page
def search(request):
    search_input = request.GET.get('search-input', '').lower()
    product_list = Product.objects.all()
    blogs_list = Blogs.objects.all()
    if search_input == 'rings':
        return render(request, 'jewelGleamer/jewelry/category.html', {"rings": product_list})
    elif search_input == 'blogs':
        return render(request, 'jewelGleamer/jewelry/blog.html', {"blogs": blogs_list})
    else:
        return render(request, 'jewelGleamer/jewelry/search.html')


# Edit view to change item name and price on the category page for the product
def edit_ring(request, ring_id):
    product_list = Product.objects.get(id=ring_id)
    user = User.objects.get(username=request.session.get('username'))
    if request.method == 'POST':
        old_name = product_list.name
        old_price = product_list.price
        new_name = request.POST.get('new_name')
        new_price = request.POST.get('new_price')
        new_details = request.POST.get('new_details')
        new_description = request.POST.get('new_description')
        new_materials = request.POST.get('new_materials')
        if old_name != new_name:
            action_title = f"edited the title from '{old_name}' to '{new_name}': Link - "
            product_list.name = new_name
            action_title_instance = Action(
                user=user,
                verb=action_title,
                target=product_list
            )
            action_title_instance.save()
        if int(old_price) != int(new_price):
            action_price = f"edited the price from {old_price} to {new_price} : Link - "
            product_list.price = new_price
            action_price_instance = Action(
                user=user,
                verb=action_price,
                target=product_list
            )
            action_price_instance.save()
        product_list.name = new_name
        product_list.price = new_price
        product_list.details = new_details
        product_list.description = new_description
        product_list.materials = new_materials
        product_list.save()
        messages.add_message(request, messages.INFO, "You have successfully edited product: %s" % old_name)
        item_detail_url = reverse('jewelGleamer:item_detail', kwargs={'item_id': ring_id})
        return HttpResponseRedirect(item_detail_url)
    return render(request, 'jewelGleamer/jewelry/edit_product.html', {'product': product_list})


# Retrieving other blog posts in the blog page
def other_blogs(request):
    blogs = Blogs.objects.all()
    other_blog = [{'description': b.description} for b in blogs]
    return JsonResponse({'blogs': other_blog})


# Adding new item in the category page
def add_new_item(request):
    return render(request, 'jewelGleamer/jewelry/add_item.html')


# Generating AI related description for a product using description and materials.
def generate_description(request, item_id):
    try:
        item = get_object_or_404(Product, id=item_id)
        current_description = item.description
        item_details = item.details
        item_materials = item.materials
        prompt = request.POST.get('prompt', f"Provide an interesting description of the product: {current_description} using details: {item_details} and consider the item materials: {item_materials}. Limit the enhanced description to 2 lines please.")
        if not prompt:
            raise ValueError("Prompt cannot be empty.")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        if 'choices' not in response or not response['choices']:
            raise ValueError("Failed to generate a description. Please try again.")
        choices = response['choices']
        random_number = random.randint(0, len(choices) - 1)
        enhanced_description = response['choices'][random_number]['message']['content']
        item.description = enhanced_description
        item.save()
        return JsonResponse({'success': True, 'enhanced_description': enhanced_description})
    except ValueError as v:
        logging.error(f"ValueError in generate_description: {v}")
        return JsonResponse({'success': False, 'error': str(v)})
    except openai.error.RateLimitError:
        return JsonResponse({'success': False, 'error': 'Rate limit reached. Please try again after a short wait.'},
                            status=429)
    except Exception as e:
        logging.exception("An unexpected error occurred in generate_description")
        return JsonResponse({'success': False, 'error': "An unexpected error occurred. Please try again later."})


# Save description once the user confirms it with AI generated description
def save_description(request, item_id):
    try:
        item = get_object_or_404(Product, id=item_id)
        current_description = request.POST.get('edited_description', '')
        if not current_description:
            raise ValueError("Description cannot be empty.")
        print(current_description)
        item.description = current_description
        item.save()
        return JsonResponse({'success': True, 'enhanced_description': current_description})
    except ValueError as v:
        return JsonResponse({'success': False, 'error': str(v)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': "An unexpected error occurred. Please try again later."})
