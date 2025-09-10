# gunicorn.conf.py

# Socket to bind to.
# '0.0.0.0:8000' মানে হলো সব নেটওয়ার্ক ইন্টারফেসের 8000 পোর্টে সার্ভার চলবে।
bind = "ngrok http --url=giving-sacred-minnow.ngrok-free.app 8000"

# Number of worker processes.
# সাধারণত CPU কোরের সংখ্যার দ্বিগুণ + ১ রাখা হয়।
# import multiprocessing
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 3  # আপাতত আমরা ৩ দিয়ে শুরু করতে পারি

# The user to run as.
# user = "www-data"  # প্রোডাকশন সার্ভারে নির্দিষ্ট ইউজার সেট করা ভালো অভ্যাস

# The group to run as.
# group = "www-data" # প্রোডাকশন সার্ভারে নির্দিষ্ট গ্রুপ সেট করা ভালো অভ্যাস

# Logging
# Access log - records incoming requests
accesslog = "gunicorn_access.log"

# Error log - records Gunicorn errors
errorlog = "gunicorn_error.log"

# Log level
loglevel = "info"