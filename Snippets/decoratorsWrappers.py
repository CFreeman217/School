

# Decorators - Logging

# This lets us stack wrappers

from functools import wraps

def my_logger(orig_func):

	# Here, orig_func is the name of the function called by placing the wrapper above
	# the function definition
	
	import logging
	
	# Create a file with the name of the calling function, or open such file if it exists
	
	logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)
	
	# This tag preserves the original function call when my_logger is used with another 
	# wrapper.
	
	@wraps(orig_func)
	def wrapper(*args, **kwargs):
		
		# The *args and **kwargs let this function get called for any number of input
		# or keyword arguments. 
		# - Possibly useful if you don't know how many arguments will be passed in
		
		logging.info(
		
			# List out the arguments imported by the original calling function
		
			'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
		
		# Since we looked at the arguments and keyword arguments, we need to put
		# them back into the original function This calls the original function
		
		return orig_func(*args, **kwargs)
		
	# So this is the command that initiates the wrapper function above
	
	return wrapper
	
def my_timer(orig_func):
	
	import time
	
	@wraps(orig_func)
	
	def wrapper(*args, **kwargs):
	
		t1 = time.time()
		result = orig_func(*args, **kwargs)
		t2 = time.time() - t1
		print('{} ran in: {} sec'.format(orig_func.__name__, t2))
		return result
	
	return wrapper
	
import time
	
@my_logger
@my_timer
def display_info(name,age):
	time.sleep(1)
	print('Original calling function ran with arguments ( {}, {} )'.format(name,age))
	
display_info('Tom',22)
