from shop_app.models import Variation
from django.db.models import Avg, Count


class ProductFilterMixin:
    price_ranges = {
        'price-1': (0, 99.99),
        'price-2': (100, 199.99),
        'price-3': (200, 299.99),
        'price-4': (300, 399.99),
        'price-5': (400, 499.99),
        'price-6': (500, 100000),
    }

    def apply_price_filter(self, queryset, price_filter):
        price_range = self.price_ranges.get(price_filter)
        if price_range:
            queryset = queryset.filter(discounted_price_db__range=price_range)
        return queryset

    def apply_variation_filter(self, queryset, filter_value, variation_category):
        if filter_value:
            if filter_value == f'{variation_category}-all':
                pass
            else:
                queryset = queryset.filter(
                    variation__variation_category=variation_category,
                    variation__variation_value=filter_value
                )
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        price_filter = self.request.GET.get('price')
        color_filter = self.request.GET.get('color')
        size_filter = self.request.GET.get('size')
        sort_filter = self.request.GET.get('sort')

        queryset = self.apply_price_filter(queryset, price_filter)
        queryset = self.apply_variation_filter(queryset, color_filter, 'color')
        queryset = self.apply_variation_filter(queryset, size_filter, 'size')

        if sort_filter == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort_filter == 'reviews':
            queryset = queryset.annotate(review_count=Count('reviewrating')).order_by('-review_count')
        elif sort_filter == 'rating':
            queryset = queryset.annotate(average_rating=Avg('reviewrating__rating')).order_by('-average_rating')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_price = self.request.GET.get('price')
        selected_color = self.request.GET.get('color')
        selected_size = self.request.GET.get('size')
        context['selected_price'] = selected_price
        context['selected_color'] = selected_color
        context['selected_size'] = selected_size

        context['available_colors'] = Variation.objects.filter(
            variation_category='color',
            is_active=True
        ).values_list('variation_value', flat=True).distinct()


        context['available_sizes'] = Variation.objects.filter(
            variation_category='size',
            is_active=True
        ).values_list('variation_value', flat=True).distinct()

        context['available_colors'] = sorted(context['available_colors'])
        context['available_sizes'] = sorted(context['available_sizes'])

        context['price_ranges'] = [
            {'label': '$0 - $99.99', 'value': 'price-1'},
            {'label': '$100 - $199.99', 'value': 'price-2'},
            {'label': '$200 - $299.99', 'value': 'price-3'},
            {'label': '$300 - $399.99', 'value': 'price-4'},
            {'label': '$400 - $499.99', 'value': 'price-5'},
            {'label': '$500+', 'value': 'price-6'},
        ]

        return context

