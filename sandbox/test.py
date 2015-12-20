def test_var_args(farg, *args, **kwargs):

    print "formal arg:", farg
    
    i = 0
    for arg in args:
        i +=1
        print "arg %i: " % i,  arg

    i = 0
    print 'kwargs: ', kwargs

test_var_args(1, "two", 3, alpha='a')