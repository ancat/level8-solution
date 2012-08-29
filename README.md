level8-solution
===============

My solution to Level 8 of Stripe CTF.
Benchmarky is a small static class that makes benchmarking multiple
To use the script, you'll need to edit it first, and replace my hosts and
username with your information. Then simply run the script for the first three
chunks. For the final chunk, you can just brute force the endpoint like you
would regularly.

First chunk: (With the brute forced chunk masked out)
    python chunky.py 31337 1 XXX000000000

Second chunk:
    python chunky.py 31337 2 000XXX000000

Third chunk:
    python chunky.py 31337 3 000000XXX000

