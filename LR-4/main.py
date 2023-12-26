

def fib(n):
  fib1 = fib2 = 1
  n = int(n) - 2
  
  while n > 0:
    fib1, fib2 = fib2, fib1 + fib2
    n -= 1
  
  return fib2


class FibonacchiLst:
  def __init__(self, instance):
      self.instance = instance
      self.idx = 0
      self.prev, self.curr = 0, 1

  def __iter__(self):
      self.idx = 0
      return self

  def __next__(self):
      while self.idx < len(self.instance):
          value = self.instance[self.idx]
          self.idx += 1

          if value == self.curr:
              result = self.curr
              self.prev, self.curr = self.curr, self.prev + self.curr
              return result

      raise StopIteration
    

def fib_iter(iterable):
  fib_values = []  
  prev, curr = 0, 1

  for num in iterable:
      while curr <= num:
          fib_values.append(curr) 
          prev, curr = curr, prev + curr

  return fib_values


def test_fib():
  assert fib(1) == 1

  assert fib(2) == 1

  assert fib(3) == 2

  assert fib(5) == 5

  assert fib(8) == 21

  assert fib(12) == 144

  assert fib(0) == 1

  print("Все тесты прошли успешно!")




def test_fib_iter():
  assert fib_iter(range(14)) == [1, 1, 2, 3, 5, 8, 13]

  assert fib_iter(range(8)) == [1, 1, 2, 3, 5]

  assert fib_iter(range(1)) == []

  assert fib_iter([]) == []

  print("Все тесты прошли успешно!")



if __name__ == '__main__':
  test_fib_iter()
  test_fib()

