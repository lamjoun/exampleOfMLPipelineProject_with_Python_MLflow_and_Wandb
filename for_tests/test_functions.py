from src.functions import function1, function2

 
 #---------- Test------------#
def test_function1(_function1):
  print('Ici Test_Function1!!')
  vv=_function1
  vv=function1()+vv
  assert (vv==8)
  
  
def test_function2(_function2):
  print('Ici Test_Function2!!')
  vv=function2(_function2)
  assert (vv==13)
