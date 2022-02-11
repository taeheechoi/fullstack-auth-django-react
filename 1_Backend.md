### Django

1. Current version is 4.0.2
2. Q?
```py
from django.db import models
from django.db.models import Q
objects = Test.objects.get(Q(field1__startswith='Test'),  Q(field2='Yes') | Q(field3=False))
= SELECT * FROM Test WHERE field1 like 'Test%' AND (field2='Yes' OR field3=False)
```
3. selected_related vs prefetch_related

select_related uses a foreign key relationship using join on the query itself

prefetch_related separate lookup and joining on python
```py
from django.db import models
class Country(models.Model):
    country_name = models.CharField(max_length=5)
class State(models.Model):
    state_name = models.CharField(max_length=5)
    country = model.ForeignKey(Country)

states = State.objects.select_related(‘country’).all()
= SELECT state_id, state_name, country_name FROM State INNER JOIN Country ON (State.country_id = Country.id)

country = Country.objects.prefetch_related(‘state’).get(id=1)
SELECT id, country_name FROM country WHERE id=1
SELECT state_id, state_name WHERE State WHERE country_id IN (1)
```

4. SQL query: print(queryset.query)

5. Chaining multiple querysets: list(chain(list1, list2, list3))

6. OneToOneField: Model only, ForeignKey: Model and on_delete

7. file-based session
```py
SESSION_ENGINE=[
    "django.contrib.sessions.backends.file"
]
```

8. Middleware: executes between request and response

9. Lifecycle: httprequest object including request metadata -> load view -> httprequest to view -> view returns httpresponse 
```
First of the Django settings.py file is loaded which also contain various middleware classes (MIDDLEWARES)
The middlewares are also executed in the order in which they are mentioned in the MIDDLEWAREST
From here on the request is now moved to the URL Router, who simply gets the URL path from the request and tries to map with our given URL paths in the urls.py. 
As soon as it has mapped, it will call the equivalent view function, from where an equivalent response is generated
The response also passes through the response middlewares and send back to the client/browser.
```

10. Caching strategies: Memcached, Filesystem Caching, Local-memory caching: default, Database caching


### References

https://www.interviewbit.com/django-interview-questions/