def factor(num:int)->list:
  result = [];
  for i in range(1, num+1):
    if num%i == 0:
      result.append(i);
  return result;

print(factor(int(input("Enter a number:"))));
