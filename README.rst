A decorator to help remind you to use select_related.

Only use this while in development. Leaving it in production is a bad idea.

.. code-block:: python
	from nolazyqueries import no_lazy_queries
	
	@no_lazy_queries()
	def myView(request):
	
		# Will raise an exception
		Foo.objects.first().bar
		
		# Will not raise an exception
		Foo.objects.select_related('bar').first().bar
